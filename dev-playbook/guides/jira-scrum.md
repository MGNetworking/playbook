# Guide Jira Scrum — Backlog depuis checklist-implementation.md

> Ce guide documente le raisonnement derrière la décomposition du backlog Jira.
> Source unique : `docs/backend/livrable/checklist-implementation.md`
>
> **Fichiers concernés :**
>
> - `playbook/tools/import_jira.py` — moteur d'import partagé (ne pas modifier)
> - `playbook/tools/jira_backlog_template.py` — template vide des données — à copier dans `docs/backend/livrable/` et remplir
> - `playbook/tools/.env.example` — template credentials — à copier dans `docs/backend/livrable/.env` et remplir
> - `docs/jira-registry.json` — registre Jira centralisé — mis à jour automatiquement après chaque import

---

## Index — navigation rapide

> Pour une IA : lire l'index, puis charger uniquement la plage de lignes dont tu as besoin.
> Pour un humain : repérer la section et y sauter directement.

| Section                         | Lignes    | Usage                              |
| ------------------------------- | --------- | ---------------------------------- |
| Pourquoi cette phase existe     | 37 – 42   | Comprendre le contexte             |
| Correspondance checklist → Jira | 43 – 74   | Comprendre Epic / Story / Sub-task |
| Règles de décomposition         | 65 – 74   | Règles à appliquer                 |
| Extraction depuis checklist     | 75 – 122  | Démarche IA + prompt type          |
| Créer le projet Jira            | 123 – 138 | Type Scrum + clé projet            |
| Prérequis environnement         | 139 – 155 | Vérifier Python + requests         |
| Configurer le fichier .env      | 156 – 175 | Credentials Jira                   |
| Lancer le script                | 176 – 200 | Commande d'exécution + registre    |
| Ajouter une feature             | 201 – 215 | Après le premier import            |
| Structure des fichiers          | 216 – 240 | Où se trouvent les fichiers        |

---

## Pourquoi cette phase existe

La checklist d'implémentation organise le travail par couche technique. Le backlog Jira organise le même travail pour une équipe Scrum : chaque item doit être estimable, assignable et traçable. Ce guide explique comment passer de l'un à l'autre sans perdre d'information.

---

## Correspondance checklist → Jira

| Niveau checklist                                          | Type Jira    | Règle de découpage                                                       |
| --------------------------------------------------------- | ------------ | ------------------------------------------------------------------------ |
| Couche architecturale (Domain, Application…)              | **Epic**     | 1 Epic = 1 couche = 1 grand axe de travail livrable en plusieurs sprints |
| Fonctionnalité ou service (UserService, UsersController…) | **Story**    | 1 Story = 1 concept cohérent développable en 1 à 3 jours                 |
| Item technique atomique (endpoint, configuration, test)   | **Sub-task** | 1 Sub-task = 1 tâche codable en moins de 2h                              |

### Pourquoi couche = Epic

La couche est la frontière d'indépendance naturelle : on peut livrer le Domain sans l'Infrastructure, l'Application sans l'API. Chaque Epic représente une étape de livraison cohérente qui peut être démontrée seule.

### Pourquoi service = Story

Un service regroupe des opérations qui partagent le même contexte métier (UserService gère tout ce qui concerne le User). Les Stories à ce niveau permettent une estimation raisonnable (3 à 8 points) et un sprint planning clair.

### Pourquoi item technique = Sub-task

Les items de la checklist sont déjà des tâches atomiques : créer un endpoint, implémenter une configuration EF Core, écrire un test. Chaque Sub-task est assignable à un développeur individuellement.

---

## Règles de décomposition

- **1 Epic par couche** : Domain / Application / Infrastructure / API / Tests
- **1 Story par service ou contrôleur** (pas un par méthode)
- **1 Sub-task par item de la checklist** — si un item est trop gros (ex : job import OFF), le découper en sous-tâches techniques
- **Labels par couche** : `domain`, `application`, `infrastructure`, `api`, `tests`
- **Priorité par défaut** : Medium — ajuster en sprint planning selon les dépendances

---

## Extraction depuis checklist-implementation.md

La checklist est organisée en sections numérotées qui mappent directement vers les types Jira. Voici comment lire le fichier pour alimenter le script :

### 1. Epics — depuis les titres de section

Chaque titre de section de niveau 2 (`##`) devient un Epic :

```
## 1. Couche Domain          → Epic "Domain Layer"
## 2. Couche Application     → Epic "Application Layer"
## 3. Couche Infrastructure  → Epic "Infrastructure Layer"
## 4. Couche API             → Epic "API Layer"
## 6. Tests                  → Epic "Tests"
```

### 2. Stories — depuis les sous-sections

Chaque titre de niveau 3 (`###`) devient une Story rattachée à l'Epic de sa section :

```
### UserService              → Story "UserService"          (Epic: Application Layer)
### DietPlanService          → Story "DietPlanService"      (Epic: Application Layer)
### UsersController          → Story "UsersController"      (Epic: API Layer)
```

### 3. Sub-tasks — depuis les items `🔲`

Chaque ligne commençant par `🔲` devient une Sub-task rattachée à la Story de sa sous-section :

```
🔲 `GET /users/me`  →  Sub-task "Implémenter GET /users/me"  (Story: UsersController)
🔲 Implémenter entité User  →  Sub-task  (Story: Aggregate Roots)
```

### Démarche de génération IA

```
checklist-implementation.md
        ↓ étape 1 — IA lit et décompose
jira-backlog-decomposition.md   ← tu valides ici (Markdown lisible, facile à corriger)
        ↓ étape 2 — IA traduit en Python
jira_backlog.py                 ← données prêtes pour le script
        ↓ étape 3 — script exécuté
Tickets créés dans Jira
```

**Pourquoi l'étape intermédiaire ?**
Corriger une erreur dans le Markdown est simple. Corriger dans le Python puis relancer le script risque de créer des doublons dans Jira.

**Étape 1 — Générer `jira-backlog-decomposition.md`**

Prompt à donner à l'IA :

> "Lis `checklist-implementation.md` et génère `docs/backend/livrable/jira-backlog-decomposition.md` : décomposition lisible Epic / Story / Sub-task. 1 Epic par section ##, 1 Story par sous-section ###, 1 Sub-task par item 🔲. Pas encore de Python."

Valider le fichier produit : vérifier que chaque item de la checklist est couvert.

**Étape 2 — Générer `jira_backlog.py`**

Prompt à donner à l'IA :

> "Depuis `jira-backlog-decomposition.md`, génère les listes Python EPICS, STORIES et SUBTASKS dans `docs/backend/livrable/jira_backlog.py`. Copier d'abord `playbook/tools/jira_backlog_template.py`. Labels par couche, priorité Medium par défaut."

---

## Créer le projet Jira

> ⚠️ **Important — type de projet obligatoire**
>
> Le projet Jira doit être de type **Scrum** et **Géré par l'entreprise** (Company-managed).
> Un projet Géré par l'équipe (Team-managed) ne supporte pas les Sub-tasks ni le champ Epic Link — l'import échouera.
>
> **Créer le projet :**
> Jira → Créer un projet → Sélectionner **Scrum** → Choisir **Géré par l'entreprise**.
>
> **Récupérer la clé du projet :**
> Une fois le projet créé, la clé s'affiche dans les paramètres du projet (ex : `NUT`, `NUTRI`).
> C'est cette valeur à renseigner dans `.env` pour la propriété `JIRA_PROJECT_KEY`.

---

## Prérequis — vérifier l'environnement avant le premier lancement

Exécuter ces commandes dans WSL pour vérifier que tout est en place :

```bash
# 1. Vérifier Python 3
python3 --version
# Attendu : Python 3.x.x

# 2. Vérifier que requests est disponible
python3 -c "import requests; print('requests OK')"
# Si erreur → installer avec :
pip3 install requests --break-system-packages
```

---

## Configurer le fichier .env

```bash
cp playbook/tools/.env.example docs/backend/livrable/.env
```

Remplir `docs/backend/livrable/.env` :

```
JIRA_URL=https://ton-domaine.atlassian.net
JIRA_EMAIL=ton@email.com
JIRA_TOKEN=ton_api_token
JIRA_PROJECT_KEY=CLE_PROJET
```

> **Token API Jira :** Account Settings → Security → API tokens → Create API token.
> Ce n'est pas ton mot de passe — c'est un token dédié à l'API.

---

## Lancer le script

Depuis la racine du workspace :

```bash
python3 playbook/tools/import_jira.py docs/backend/livrable/jira_backlog.py
```

Le script :

1. Vérifie la connexion Jira et affiche ton nom si OK
2. Détecte automatiquement le type Sub-task de ton projet
3. Importe les données depuis le fichier backlog passé en argument
4. Crée les Epics, puis les Stories, puis les Sub-tasks (300ms entre chaque appel)
5. Affiche un résumé final du nombre de tickets créés
6. **Met à jour `docs/jira-registry.json` automatiquement** (last_import, max refs, jira_ids des Epics)

---

## Ajouter une feature après l'import

Pour ajouter une nouvelle fonctionnalité après le premier import :

- Consulter `docs/jira-registry.json` pour les IDs Jira des Epics existants et les refs disponibles
- Utiliser `MODE = "add"` dans le fichier backlog + renseigner `EXISTING_EPICS` depuis le registre
- Lancer l'import — `docs/jira-registry.json` est mis à jour automatiquement

**Guide complet :** `playbook/feature-playbook/guides/add-feature.md`

> Ne pas relancer le script en MODE "create" sur un module déjà importé — cela créerait des doublons.
> Jira est la source de vérité dès le premier import.

---

## Structure des fichiers

```
playbook/tools/                        ← kit Jira partagé entre tous les playbooks
├── import_jira.py                     ← moteur d'import (ne pas modifier)
├── jira_backlog_template.py           ← template générique — à copier et renommer par module
└── .env.example                       ← template credentials — à copier dans docs/backend/livrable/.env

docs/
├── backend/livrable/                  ← livrables dev-playbook
│   ├── jira_backlog.py                ← données backend (copié + rempli depuis le template)
│   └── .env                           ← credentials réels — ne JAMAIS commiter (partagé entre modules)
├── frontend/livrable/                 ← livrables frontend-playbook (si activé)
│   └── jira_backlog_frontend.py
└── sdk/livrable/                      ← livrables sdk-playbook (si activé)
    └── jira_backlog_sdk.py
```

> Le moteur `import_jira.py` s'appelle toujours depuis la racine du workspace.
> Le fichier backlog (données) est passé en argument — jamais codé en dur dans le moteur.
