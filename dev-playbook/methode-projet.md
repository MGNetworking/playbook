# Méthode projet — Dev Playbook

> Objectif : être efficace sur un nouveau projet en sachant par où commencer et comment organiser la documentation.
> Approche : **Spec-Driven Development** — concevoir avant de coder.
> Périmètre : de la conception jusqu'au backlog Jira importé (Phases 0 → 6.5).

---

## Contenu de ce dev-playbook

```
dev-playbook/
├── README.md                        ← point d'entrée — lire en premier
├── methode-projet.md                ← ce fichier — méthode pas-à-pas (Phases 0 → 6.5)
├── guides/
│   ├── specs-frontend.md            ← démarche identification des écrans (Phase 5)
│   └── jira-scrum.md                ← méthodologie backlog Jira Scrum — Epic/Story/Sub-task (Phase 6.5)
├── templates/
│   └── suivi-projet.md              ← gabarit suivi de projet à copier en Phase 0
└── references/
    └── references-ddd.md            ← glossaire DDD, architecture 4 couches, template CLAUDE.md, format Mermaid
```

> `methode-projet.md` est le seul fichier de process à la racine — c'est le seul que l'IA charge par défaut.
> `guides/` contient les guides spécifiques à certaines phases — chargés à la demande.
> `templates/` contient les gabarits à copier une fois au démarrage — jamais relus ensuite.
> `references/` contient des documents consultables ponctuellement, hors du flux de la méthode.
> **Import Jira :** outil partagé dans `playbook/tools/` — voir `playbook/README.md`.

---

## Index — navigation rapide

> Pour une IA : lire l'index (cette section), puis charger uniquement la plage de lignes dont tu as besoin.
> Pour un humain : repérer la section et y sauter directement.

| Section                                | Lignes                         | Usage                                               |
| -------------------------------------- | ------------------------------ | --------------------------------------------------- |
| Règle synchronisation documentation    | 65 – 77                        | Consulter en fin de phase                           |
| Règle de retour en arrière             | 78 – 93                        | Consulter quand on corrige une phase passée         |
| Structure du workspace                 | 94 – 144                       | Copier au démarrage d'un projet                     |
| **Phase 0** — Initialisation           | 145 – 178                      | Démarrage projet                                    |
| **Phase 1** — Cadrage métier           | 179 – 227                      | Cas d'usage + acteurs + MVP                         |
| **Phase 2** — Conception fonctionnelle | 228 – 259                      | Specs fonctionnelles + règles métier                |
| **Phase 3** — Modélisation domaine     | 260 – 311                      | Entités, Value Objects, invariants                  |
| **Phase 4** — Workflows                | 312 – 349                      | Diagrammes de séquence Mermaid                      |
| **Phase 5** — Specs Frontend           | 350 – 408                      | Contrats API par écran                              |
| **Phase 6** — Validation cohérence     | 409 – 451                      | Checklist d'implémentation                          |
| **Phase 6.5** — Backlog Jira Scrum     | 452 – 497                      | Import Epic/Story/Sub-task                          |
| Résumé ordre de démarrage              | 498 – 516                      | Vue d'ensemble en 30 secondes                       |
| Glossaire DDD + TDD + Architecture + Mermaid | `references/references-ddd.md` | Consulter ponctuellement                      |

---

## Principe fondamental

> Les cas d'usage sont le point de départ de tout.
> Ils font émerger les agrégats, les types de données et les besoins métier naturellement.
> Ne pas chercher à modéliser sans avoir écrit les cas d'usage.

---

## Règle de synchronisation documentation

**À la fin de chaque phase, avant de passer à la suivante :**

- [ ] Tous les fichiers de documentation sont à jour
- [ ] Les décisions prises sont tracées (SUIVI-PROJET.md)
- [ ] Aucune contradiction entre les fichiers
- [ ] Le fichier de suivi reflète l'état réel

> Cette règle évite de se retrouver avec une documentation qui décrit une version du projet qui n'existe plus.

---

## Règle de retour en arrière

La modélisation est un processus itératif. Découvrir en Phase 4 que le modèle domaine de Phase 3 est faux est **normal**, pas un échec.

**Quoi faire :**

1. Revenir à la phase concernée et corriger
2. Propager la correction dans tous les fichiers impactés (modèle → diagramme → règles métier → workflows)
3. Tracer la décision révisée dans `SUIVI-PROJET.md` avec la raison du changement
4. Mettre à jour `CLAUDE.md` si le modèle domaine a changé
5. Reprendre la phase en cours depuis le début de l'étape où la correction a été faite

> **Règle clé :** ne jamais laisser une correction partielle. Si on corrige le modèle domaine, le diagramme de classes doit refléter la correction le jour même — pas "plus tard".

---

## Structure du workspace à créer dès le départ

Le workspace est la **racine globale** — il contient deux dossiers frères : la documentation (`docs/`) et le toolkit méthodologie (`dev-playbook/`). Les fichiers de suivi sont à la racine.

```
[workspace]/                         ← racine globale (ex: nutrition-api, blog, crm)
├── SUIVI-PROJET.md                  ← rempli depuis dev-playbook/templates/suivi-projet.md
├── CLAUDE.md                        ← créé depuis le template CLAUDE.md (si IA utilisée)
│
├── dev-playbook/                    ← toolkit méthodologie — copié tel quel, ne pas modifier
│   ├── README.md
│   ├── methode-projet.md
│   ├── guides/
│   │   ├── specs-frontend.md
│   │   └── jira-scrum.md
│   ├── templates/
│   │   └── suivi-projet.md
│   └── references/
│
├── docs/                            ← documentation organisée par playbook
│   ├── backend/                     ← livrables dev-playbook (Phase 0 → 6.5)
│   │   ├── 1.[projet]-introduction.md           ← présentation du projet — Phase 0
│   │   ├── 2.[projet]-cas-usage.md              ← cas d'usage (UC01...) — Phase 1
│   │   ├── 3.[projet]-specs-fonctionnelles.md   ← règles métier détaillées — Phase 2
│   │   ├── 4.[projet]-specs-techniques.md       ← stack + architecture — Phase 2
│   │   ├── 5.[projet]-contraintes.md            ← exigences non-fonctionnelles — Phase 2
│   │   ├── 6.[projet]-livrables-planning.md     ← livrables + planning détaillé — Phase 6
│   │   ├── domaine/
│   │   │   ├── modele-domaine.md                ← modèle domaine + décisions — Phase 3
│   │   │   ├── diagramme-classes.md             ← diagramme Mermaid — Phase 3
│   │   │   └── regles-metier.md                 ← invariants + formules — Phase 3
│   │   ├── annexes/
│   │   │   └── workflow_[nom].mermaid           ← un fichier par flux clé — Phase 4
│   │   └── livrable/
│   │       ├── specs-frontend.md                ← contrats API par écran — Phase 5
│   │       ├── checklist-implementation.md      ← pont conception → code — Phase 6
│   │       ├── jira-backlog-decomposition.md    ← décomposition Epic/Story/Sub-task — Phase 6.5
│   │       ├── jira_backlog.py                  ← données backlog (EPICS, STORIES, SUBTASKS) — Phase 6.5
│   │       └── .env                             ← credentials Jira — ne JAMAIS commiter
│   ├── frontend/                    ← livrables frontend-playbook (si utilisé)
│   │   └── livrable/
│   ├── sdk/                         ← livrables sdk-playbook (si utilisé)
│   │   └── livrable/
│   └── devops/                      ← livrables devops-playbook (si utilisé)
│       └── livrable/
```

> Remplacer `[workspace]` par le nom global du projet (ex: `nutrition-api`, `blog`, `crm`).
> Remplacer `[projet]` dans `docs/backend/` par le nom court (ex: `nutrition`, `blog`, `crm`).
> Les fichiers numérotés (1 à 6) se créent progressivement — ne pas tous les créer vides dès le départ.
> Les sous-dossiers `domaine/`, `annexes/`, `livrable/` peuvent être créés dès la Phase 0.
> Les dossiers `frontend/`, `sdk/`, `devops/` ne sont créés que si les playbooks correspondants sont activés.

---

## Phase 0 — Initialisation

**Durée estimée :** 1 heure

### Ce qu'on fait

**Les 3 fichiers de base sont déjà à la racine** (copiés depuis le dev-playbook). Il reste à :

1. Remplir l'en-tête de `SUIVI-PROJET.md` — nom du projet, stack, date
2. Créer `CLAUDE.md` depuis le template dans **Références rapides → CLAUDE.md** ci-dessus
3. Créer `docs/backend/` avec les sous-dossiers `domaine/`, `annexes/`, `livrable/` — vides pour l'instant
4. Créer `docs/backend/1.[projet]-introduction.md` — présentation du projet en quelques phrases (besoin, acteurs, stack)

### Pourquoi c'est important

Démarrer sans structure oblige à réorganiser en cours de route — perte de temps et risque d'oublier des fichiers. Un tracker de progression visible à tout moment évite de se perdre.

### Ce qu'on produit

- `SUIVI-PROJET.md` initialisé — en-tête rempli, toutes les phases à `🔲`
- `CLAUDE.md` créé — contexte projet + stack + prochaine étape = Phase 1
- Dossier `docs/backend/` créé avec ses 3 sous-dossiers (`domaine/`, `annexes/`, `livrable/`)
- `docs/backend/1.[projet]-introduction.md` créé — présentation initiale du projet

### Comment savoir qu'on a terminé

Les 2 fichiers racine sont remplis. Le dossier `docs/backend/` existe. On sait où ira chaque fichier avant de l'écrire.

---

## Phase 1 — Cadrage métier

**Durée estimée :** 2 à 4 heures

### Ce qu'on fait

1. Écrire en prose le **besoin métier** — quel problème résout le projet, pour qui
2. Identifier les **acteurs** — qui utilise le système et avec quels objectifs
3. Rédiger les **cas d'usage** (UC01, UC02...) — ce que l'utilisateur fait concrètement
4. Définir le **MVP** — ce qui est indispensable pour une première version utilisable
5. Lister la **vision future** — ce qui peut attendre

### Pourquoi c'est important

Les cas d'usage sont le point de départ de la modélisation. Ils font émerger :

- Les **agrégats** (les noms dans les actions utilisateur)
- Les **types de données** nécessaires
- Les **règles métier** implicites
- Les **besoins d'infrastructure** (auth, services externes...)

Sans cas d'usage, la modélisation repose sur des suppositions.

### Format d'un cas d'usage

```
UCxx — [Titre court]
Acteur    : [qui]
Déclencheur : [qu'est-ce qui déclenche l'action]
Flux      : [ce que l'utilisateur fait]
Résultat  : [ce qu'il obtient]
Règles    : [conditions de succès / d'échec]
```

### Ce qu'on produit

- `docs/backend/livrable/cas-usage.md` — liste complète UC01 à UCxx + MVP + vision future

### Comment savoir qu'on a terminé

Chaque cas d'usage tient en une phrase : _"L'utilisateur [action] afin de [résultat]."_
Le MVP est clairement séparé de la vision future.

### ✅ Checkpoint documentation

Mettre à jour `SUIVI-PROJET.md` — Phase 1 → ✅

---

## Phase 2 — Conception fonctionnelle

**Durée estimée :** 2 à 6 heures (selon complexité)

### Ce qu'on fait

1. Rédiger les **specs fonctionnelles** — règles métier détaillées par fonctionnalité
2. Définir les **formules et calculs** si applicable
3. Lister les **contraintes non-fonctionnelles** (performance, sécurité, scalabilité)
4. Identifier les **services externes** nécessaires (APIs, auth, cache...)

### Pourquoi c'est important

Les specs fonctionnelles transforment les cas d'usage en règles précises. C'est ici qu'on tranche les ambiguïtés avant de modéliser — pas pendant le codage.

### Ce qu'on produit

- `docs/backend/3.[projet]-specs-fonctionnelles.md`
- `docs/backend/4.[projet]-specs-techniques.md` — doit inclure :
  - **Section DDD** : paradigme architectural, vocabulaire (Aggregate Root, Value Object...), architecture 4 couches
  - **Section TDD** : cycle Red→Green→Refactor, ordre par couche, convention de nommage, structure des projets de test
- `docs/backend/5.[projet]-contraintes.md`

> Les définitions complètes DDD et TDD sont dans `references/references-ddd.md` — à copier/adapter dans les specs-techniques du projet.

### Comment savoir qu'on a terminé

Chaque cas d'usage a ses règles métier correspondantes dans les specs.
Aucune règle n'est ambiguë — si deux lectures sont possibles, trancher ici.
La section TDD de `4.[projet]-specs-techniques.md` est renseignée avec les outils du projet (pas de générique).

### ✅ Checkpoint documentation

Mettre à jour `SUIVI-PROJET.md` — Phase 2 → ✅

---

## Phase 3 — Modélisation domaine

**Durée estimée :** 4 à 8 heures

### Ce qu'on fait

Extraire les concepts métier depuis les cas d'usage et les specs, en cherchant les **noms** (pas les verbes).

> Les définitions de chaque type (Aggregate Root, Value Object, etc.) sont dans `references/references-ddd.md → Concepts DDD`.

**Ordre de travail :**

1. Lister les concepts candidats (tous les noms des specs)
2. Qualifier chaque concept : Aggregate Root / Entité enfant / Value Object / Enum / Service
3. Définir les attributs de chaque classe (types précis)
4. Identifier les invariants (règles toujours vraies sur un objet)
5. Identifier les Domain Services (règles qui impliquent plusieurs agrégats)
6. Tracer les décisions dans `SUIVI-PROJET.md`
7. Produire le diagramme de classes

### Pourquoi c'est important

Un bon modèle domaine évite de découvrir en codant que deux concepts ont été confondus ou qu'un invariant ne peut pas être placé correctement. Chaque décision tranchée ici évite une refactorisation coûteuse plus tard.

### Questions clés par concept

- _"Le métier parle-t-il de cet objet directement ?"_
- _"Peut-il exister de manière indépendante dans le système ?"_
- _"Si le parent est supprimé, a-t-il encore un sens ?"_
- _"Pour appliquer cette règle, ai-je besoin d'autre chose que l'objet lui-même ?"_

### Ce qu'on produit

- `docs/backend/domaine/Modele-domaine.md` — classes + attributs + décisions + invariants
- `docs/backend/domaine/Diagramme-classes.md` — diagramme Mermaid
- `docs/backend/domaine/Regles-metier.md` — invariants + formules

### Comment savoir qu'on a terminé

- Chaque concept a un type clair (AR / Entity / VO / Enum)
- Chaque attribut a un type précis (adapté au langage du projet)
- Chaque invariant est placé (dans l'objet ou dans un service)
- Le diagramme de classes correspond au modèle domaine sans contradiction

### ✅ Checkpoint documentation

- Mettre à jour `SUIVI-PROJET.md` — Phase 3 → ✅ + décisions tracées
- Vérifier cohérence avec les specs fonctionnelles
- Mettre à jour `CLAUDE.md` — section "Modèle domaine — état actuel" + "Prochaine étape"

---

## Phase 4 — Workflows

**Durée estimée :** 4 à 8 heures

### Ce qu'on fait

Documenter les **flux clés** du système — un workflow par cas d'usage principal ou par mécanisme technique complexe.

**Identifier les workflows nécessaires :**

- Un workflow par cas d'usage avec plusieurs acteurs (Device / API / DB / service externe)
- Un workflow par mécanisme d'infrastructure non trivial (auth, cache, job planifié...)
- Un workflow par contrainte légale ou de sécurité (RGPD, tokens...)

**Format :** diagramme de séquence Mermaid (`sequenceDiagram`) — voir exemple dans `references/references-ddd.md → Format workflow Mermaid`.

### Pourquoi c'est important

Les workflows révèlent les **gaps** — des cas non couverts par les specs ou le modèle domaine. Ils forcent à répondre à des questions concrètes : _"Que se passe-t-il si X n'existe pas ?"_, _"Qui appelle qui et dans quel ordre ?"_

### Ce qu'on produit

- `docs/backend/annexes/workflow_[nom].mermaid` — un fichier par flux

### Comment savoir qu'on a terminé

- Chaque cas d'usage principal a son workflow
- Chaque workflow couvre les cas nominaux ET les cas d'erreur (alt/else)
- Aucun endpoint du modèle domaine n'est sans workflow correspondant

### ✅ Checkpoint documentation

- Mettre à jour `SUIVI-PROJET.md` — Phase 4 → ✅
- Lister les gaps identifiés
- Mettre à jour `CLAUDE.md` — section "Fichiers clés" si de nouveaux workflows ont été ajoutés + "Prochaine étape"

---

## Phase 5 — Specs Frontend

> **Pourquoi cette phase vient AVANT la checklist (Phase 6) :**
> La checklist définit les endpoints de la couche API. Si on la crée avant les specs Frontend, les endpoints sont dérivés depuis l'intérieur — depuis ce que le Domain expose. Le Frontend révèle ensuite des endpoints manquants ou mal nommés, et la checklist doit être corrigée rétroactivement.
> En faisant les specs Frontend d'abord, on valide les contrats API depuis les besoins réels du Frontend. La checklist capture alors un état déjà validé, sans aller-retour.
> **Règle :** les sections Domain / Application / Infrastructure de la checklist peuvent être rédigées à partir du modèle domaine seul. La section API se remplit uniquement après cette phase.

**Durée estimée :** 2 à 4 heures

### Ce qu'on fait

Documenter les besoins de chaque écran — données à afficher et appels API nécessaires — **avant de coder la couche API**.

> **Démarche d'identification des écrans :** voir `dev-playbook/guides/specs-frontend.md` — comment transformer une liste de cas d'usage en liste d'écrans cohérente (4 étapes : candidats → regroupement → UCs embarqués → élimination).

> **Principe clé :** on valide les contrats API depuis les besoins réels du frontend.
> Un endpoint mal dimensionné découvert après le code implique de modifier le controller, le workflow, et potentiellement le modèle domaine.

**Format d'un écran :**

```
## Écran : [Nom]

**But :** [Ce que l'utilisateur fait sur cet écran]

**Données affichées**
- [Donnée 1]
- [Donnée 2]

**Appels API**
- [MÉTHODE] /endpoint  →  { champs retournés }

**Actions disponibles**
- [Action 1 — appel API correspondant]
```

**Ce format est agnostique du support** (web, mobile, desktop) — il ne décrit pas le layout visuel, uniquement les données et les contrats API.

### Pourquoi c'est important

Les specs Frontend révèlent ce que chaque endpoint doit réellement retourner. Sans cette étape, les contrats API sont définis depuis l'intérieur (ce que le Domain expose) plutôt que depuis l'extérieur (ce que le Frontend a besoin). Le risque : découvrir en codant l'API que trois appels séparés sont nécessaires là où un seul endpoint bien conçu suffirait.

### Ce qu'on produit

- `docs/backend/livrable/specs-frontend.md` — un bloc par écran, données + appels API

### Comment savoir qu'on a terminé

- Chaque écran identifié a son bloc documenté
- Chaque appel API listé existe (ou sera ajouté) dans la checklist Phase 6
- Aucun endpoint n'est ambigu sur ce qu'il doit retourner

### ✅ Checkpoint documentation

- Mettre à jour `SUIVI-PROJET.md` — Phase 5 → ✅
- Mettre à jour `CLAUDE.md` — section "Fichiers clés" + "Prochaine étape = Phase 6"

---

## Phase 6 — Validation de cohérence

> **Note :** Rédiger les sections Domain / Application / Infrastructure de la checklist depuis le modèle domaine et les workflows. Renseigner la section API en dernier — depuis `specs-frontend.md` (Phase 5). Les routes sont ainsi validées depuis les besoins réels du Frontend avant d'être formalisées ici.

**Durée estimée :** 2 à 4 heures

### Ce qu'on fait

Vérifier que le diagramme de classes, les workflows et les specs sont **cohérents entre eux** — aucun endpoint manquant, aucune règle métier sans implémentation prévue.

**Méthode :**

1. Créer `docs/backend/livrable/checklist-implementation.md` — sections Domain / Application / Infrastructure (depuis modèle domaine + workflows)
2. Compléter la section API — depuis `specs-frontend.md` (Phase 5)
3. Identifier les gaps restants et les résoudre
4. Valider les décisions en attente (questions ouvertes)
5. **Auditer les mémoires IA (si applicable)** — les fichiers doc sont maintenant complets et stables. Supprimer les mémoires qui dupliquent leur contenu, conserver uniquement ce qui n'est pas dérivable des fichiers projet (invariants non-évidents, corrections d'endpoints, profil utilisateur)

### Pourquoi c'est important

C'est le dernier filet avant le code. Un gap identifié ici se corrige en 30 minutes. Le même gap découvert en codant peut coûter une refactorisation de plusieurs heures.

### Ce qu'on produit

- `docs/backend/livrable/checklist-implementation.md` — tous les items à coder, organisés par couche

### Comment savoir qu'on a terminé

- Tous les gaps sont résolus (aucun ⚠️ restant)
- La checklist est complète — chaque item est à implémenter (`🔲`), pas en attente de décision
- Les décisions en attente sont toutes tranchées

### ✅ Checkpoint documentation

- Mettre à jour `SUIVI-PROJET.md` — Phase 6 → ✅
- Mettre à jour tous les fichiers impactés par les décisions prises durant cette phase
- Mettre à jour `CLAUDE.md` — toutes les sections (modèle final, fichiers clés complets, prochaine étape = Phase 6.5)
- **Nettoyer les mémoires IA** — auditer `MEMORY.md` et supprimer/réduire tout ce qui est redondant avec les docs finalisés

---

## Phase 6.5 — Backlog Jira Scrum

> **Pourquoi cette phase vient AVANT la création du repository git :**
> Le backlog est dérivé directement de `checklist-implementation.md` — complet et validé à ce stade. Générer le backlog maintenant permet à l'équipe de démarrer le sprint planning avant même que le repo soit créé.

**Durée estimée :** 1 à 2 heures

### Ce qu'on fait

Transformer la checklist d'implémentation en backlog Jira et l'importer directement via l'API Jira.

**Correspondance checklist → Jira :**

| Checklist                     | Type Jira    | Règle                                                                   |
| ----------------------------- | ------------ | ----------------------------------------------------------------------- |
| Couche (`##`)                 | **Epic**     | 1 Epic par couche : Domain / Application / Infrastructure / API / Tests |
| Service ou contrôleur (`###`) | **Story**    | 1 Story par concept cohérent                                            |
| Item `🔲`                     | **Sub-task** | 1 Sub-task par item atomique (codable en < 2h)                          |

**Démarche IA → script :**

1. Fournir `checklist-implementation.md` à l'IA
2. L'IA génère `docs/backend/livrable/jira-backlog-decomposition.md` — arbre lisible Epic/Story/Sub-task → **valider avant de continuer**
3. L'IA traduit en Python → `docs/backend/livrable/jira_backlog.py` (depuis le template `playbook/tools/jira_backlog_template.py`)
4. Copier `playbook/tools/.env.example` → `docs/backend/livrable/.env` et le remplir
5. Lancer : `python3 playbook/tools/import_jira.py docs/backend/livrable/jira_backlog.py`

### Ce qu'on produit

- `docs/backend/livrable/jira-backlog-decomposition.md` — décomposition lisible Epic/Story/Sub-task
- `docs/backend/livrable/jira_backlog.py` — données backlog (EPICS, STORIES, SUBTASKS)
- Tickets créés dans Jira via `playbook/tools/import_jira.py`

### Comment savoir qu'on a terminé

- Chaque item de `checklist-implementation.md` est couvert par au moins une Story ou Sub-task
- Le script s'est exécuté sans erreur et affiche le résumé final
- La décomposition est relue et validée avant import

### ✅ Checkpoint documentation

- Mettre à jour `SUIVI-PROJET.md` — Phase 6.5 → ✅
- Le playbook est terminé — le projet continue dans Jira + repository git

---

## Résumé — ordre de démarrage d'un projet

```
Phase 0   →  Créer la structure documentation
Phase 1   →  Cas d'usage + acteurs + MVP
Phase 2   →  Specs fonctionnelles + règles métier
Phase 3   →  Modèle domaine + diagramme de classes
Phase 4   →  Workflows des flux clés
Phase 5   →  Specs Frontend — valider les contrats API depuis les besoins réels du frontend
Phase 6   →  Validation cohérence + checklist d'implémentation
Phase 6.5 →  Backlog Jira — checklist → decomposition.md → jira_backlog.py → import
             ▶ FIN DU PLAYBOOK — le projet continue dans Jira + repository git
```

> À chaque fin de phase : synchroniser toute la documentation avant de passer à la suivante.

---

## Modules complémentaires — autres playbooks

Une fois le backlog backend importé dans Jira, d'autres playbooks peuvent cadrer les modules suivants selon le besoin :

| Module     | Playbook                      | Déclencher quand                        |
| ---------- | ----------------------------- | --------------------------------------- |
| Frontend   | `playbook/frontend-playbook/` | Backend cadré dans Jira ✅              |
| SDK Client | `playbook/sdk-playbook/`      | Plusieurs interfaces prévues            |
| DevOps     | `playbook/devops-playbook/`   | Tous les modules à déployer sont cadrés |

Voir `playbook/README.md` pour le graphe de dépendances complet.

