# Guide — Ajouter une feature après l'import initial

> Ce guide s'applique après qu'au moins un module ait été importé dans Jira
> et que `docs/jira-registry.json` existe.
>
> Exemple fil rouge : **feature Notifications push**.

---

## Index — navigation rapide

| Section                        | Usage                                           |
| ------------------------------ | ----------------------------------------------- |
| Prérequis                      | Vérifier les conditions avant de démarrer       |
| FT1 — Feature Brief            | Définir la feature et son scope pressenti       |
| FT2 — Gap Analysis             | Lire l'existant, identifier le delta par module |
| FT3 — Module Briefs + Backlogs | Produire les fichiers Python par module         |
| FT4 — Import Jira              | Lancer les imports dans l'ordre                 |
| Après l'import                 | Vérifier le registre et Jira                    |

---

## Prérequis

1. `docs/jira-registry.json` existe et contient au moins un module non-null
2. Les IDs Jira des Epics cibles sont renseignés dans le registre (champ `jira_id`)
3. `docs/backend/livrable/.env` est rempli avec les credentials Jira

> Si `jira_id` est null pour une Epic cible, le renseigner manuellement depuis Jira
> avant de lancer l'import en mode `add`.

---

## FT1 — Feature Brief

Créer `docs/features/[nom]/feature-brief.md` avec la structure suivante :

```markdown
# Feature Brief — [Nom de la feature]

## Description

[Ce que la feature fait — 2 à 4 phrases maximum]

## Valeur métier

[Pourquoi c'est important pour l'utilisateur]

## Scope pressenti

- Backend : oui / non — [couches probablement impactées]
- Frontend : oui / non
- SDK : oui / non
- DevOps : oui / non
```

**Exemple — Notifications push :**

```markdown
# Feature Brief — Notifications push

## Description

Permettre à l'utilisateur de recevoir des notifications push lors d'événements clés
(bilan atteint, Diet terminée, rappel repas manquant). Les notifications sont déclenchées
par des événements domaine et envoyées via un service tiers (FCM/APNs).

## Valeur métier

Augmente l'engagement actif — l'utilisateur est averti sans ouvrir l'application.

## Scope pressenti

- Backend : oui — Application Layer (service), Infrastructure (push provider), API (endpoints)
- Frontend : oui — gestion des permissions push, affichage des notifications
- SDK : non
- DevOps : non
```

**Valider avant FT2 :** la description est claire, le scope pressenti est raisonnable.
FT2 confirmera ou ajustera ce scope après lecture de l'existant.

---

## FT2 — Gap Analysis

C'est la phase centrale du feature-playbook.
Elle lit la documentation existante de chaque module pressenti et produit un diagnostic.

### Ce qu'il faut lire

| Module pressenti | Lire                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| Backend          | `docs/backend/domaine/`, `docs/backend/livrable/checklist-implementation.md`, `docs/jira-registry.json` |
| Frontend         | `docs/frontend/`, `docs/jira-registry.json`                                                             |
| SDK              | `docs/sdk/`                                                                                             |
| DevOps           | `docs/devops/`                                                                                          |

### Ce qu'il faut identifier pour chaque module

1. **Existant** — quels Epics/Stories couvrent déjà partiellement ce besoin ?
2. **Delta** — qu'est-ce qui manque concrètement ?
3. **Mode** — `add` si des Epics existants peuvent accueillir les Stories, `create` si aucun Epic n'est adapté

### Structure du livrable

Créer `docs/features/[nom]/gap-analysis.md` :

```markdown
# Gap Analysis — [Nom de la feature]

## Module Backend

### Existant

- EPIC-002 (NUT-5) — Application Layer : couvre les services métier → peut accueillir NotificationService
- EPIC-004 (NUT-17) — API Layer : couvre les controllers → peut accueillir NotificationsController

### Delta

- NotificationService (envoi, gestion des tokens FCM/APNs)
- Entité Notification dans le domaine
- Table Notifications (migration EF Core)
- Endpoints POST /notifications + GET /notifications

### Décision

MODE = add — les Epics existants EPIC-002 et EPIC-004 sont suffisants.

---

## Module Frontend

### Existant

- EPIC-101 (NUT-28) — UI Components : couvre les composants réutilisables → peut accueillir NotificationBanner

### Delta

- Demande de permission push au premier lancement
- Composant NotificationBanner (affichage in-app)
- Intégration avec l'endpoint GET /notifications

### Décision

MODE = add — EPIC-101 est suffisant.

---

## Résumé

| Module   | Mode | Epics ciblés       |
| -------- | ---- | ------------------ |
| Backend  | add  | EPIC-002, EPIC-004 |
| Frontend | add  | EPIC-101           |
```

### Les 3 cas possibles

**Cas A — feature simple (un seul module, Epics existants suffisants)**
→ Gap analysis courte, 1 seul backlog `MODE=add`.

**Cas B — feature multi-modules (plusieurs modules, Epics existants suffisants)**
→ Gap analysis par module, N backlogs `MODE=add` (un par module).

**Cas C — nouveau service (aucun Epic existant ne couvre le besoin)**
→ Gap analysis conclut qu'un nouveau groupe d'Epics est nécessaire.
→ `MODE=create` avec une plage refs libre (400+ par convention).
→ Exemple : service de facturation ajouté après l'import initial.

**Valider avant FT3 :** le gap-analysis est relu et approuvé — c'est le verrou qualité.

---

## FT3 — Module Briefs + Backlogs

Produire un fichier Python par module identifié en FT2.

### 1. Consulter le registre — trouver les prochains refs disponibles (400+)

```json
// docs/jira-registry.json — consulter registry["features"][]
{
  "backend":  { ... },   // ne pas toucher — figé après import initial
  "frontend": { ... },   // ne pas toucher — figé après import initial
  "features": []         // vide = premier import feature → EPIC-400, STORY-400, SUB-400
}
```

Prendre le `max` sur tous les `max_epic_ref`, `max_story_ref`, `max_sub_ref` de `registry["features"][]` :

```python
max_epic  = max((e["max_epic_ref"]  for e in features), default=399)
max_story = max((e["max_story_ref"] for e in features), default=399)
max_sub   = max((e["max_sub_ref"]   for e in features), default=399)
# Prochains refs : EPIC-(max_epic+1), STORY-(max_story+1), SUB-(max_sub+1)
```

### 2. Créer les fichiers backlog

```bash
cp playbook/tools/jira_backlog_template.py \
   docs/features/notifications/livrable/jira_backlog_feature_notifications_backend.py

cp playbook/tools/jira_backlog_template.py \
   docs/features/notifications/livrable/jira_backlog_feature_notifications_frontend.py
```

### 3. Remplir — Backend

```python
MODULE = "feature"   # toujours
MODE   = "create"    # toujours — chaque feature crée ses propres Epics

EXISTING_EPICS = {}  # toujours vide — les features ne touchent pas aux Epics des modules

EPICS = [
    ("EPIC-400", "Notifications — Backend", "Epics feature notifications côté backend.", "feature"),
]

STORIES = [
    # ── EPIC-400 ─────────────────────────────────────────────────────────────────
    ("STORY-400", "NotificationService", "Service de gestion des notifications push.", "Medium", "feature", 5, "EPIC-400"),
    ("STORY-401", "NotificationsController", "Endpoints REST pour les notifications.", "Medium", "feature", 3, "EPIC-400"),
]

SUBTASKS = [
    # ── STORY-400 ────────────────────────────────────────────────────────────────
    ("SUB-400", "Créer l'entité Notification", "Champs : UserId, Type, Message, IsRead, CreatedAt.", "Medium", "feature", "STORY-400"),
    ("SUB-401", "Implémenter NotificationService.Send()", "Logique d'envoi via FCM/APNs.", "Medium", "feature", "STORY-400"),
    ("SUB-402", "Migration EF Core — table Notifications", "Ajouter la migration pour la table.", "Medium", "feature", "STORY-400"),

    # ── STORY-401 ────────────────────────────────────────────────────────────────
    ("SUB-403", "Implémenter POST /notifications", "Endpoint création notification.", "Medium", "feature", "STORY-401"),
    ("SUB-404", "Implémenter GET /notifications", "Endpoint liste + filtre IsRead.", "Medium", "feature", "STORY-401"),
    ("SUB-405", "Tests d'intégration NotificationsController", "xUnit + Testcontainers.", "Medium", "tests", "STORY-401"),
]
```

### 4. Remplir — Frontend

```python
MODULE = "feature"
MODE   = "create"

EXISTING_EPICS = {}

EPICS = [
    ("EPIC-401", "Notifications — Frontend", "Epic feature notifications côté frontend.", "feature"),
]

STORIES = [
    ("STORY-402", "NotificationBanner + permission push", "Composant et demande de permission.", "Medium", "feature", 5, "EPIC-401"),
]

SUBTASKS = [
    ("SUB-406", "Demande de permission push au premier lancement", "iOS + Android.", "Medium", "feature", "STORY-402"),
    ("SUB-407", "Composant NotificationBanner", "Affichage in-app des notifications.", "Medium", "feature", "STORY-402"),
    ("SUB-408", "Intégration GET /notifications", "Fetch et affichage de la liste.", "Medium", "feature", "STORY-402"),
]
```

---

## FT4 — Import Jira

Importer dans l'ordre : backend en premier (il crée les entités référencées par le frontend).

```bash
python3 playbook/tools/import_jira.py \
   docs/features/notifications/livrable/jira_backlog_feature_notifications_backend.py
```

Sortie attendue :

```
📂 Backlog chargé : ...jira_backlog_feature_notifications_backend.py
⚙️  Mode : CREATE | Module : feature
✅ Connecté en tant que : Prénom Nom
==================================================
📦 Création des Epics...
   ✅ NUT-42 — Notifications — Backend
==================================================
📖 Création des Stories...
   ✅ NUT-43 — NotificationService
   ✅ NUT-44 — NotificationsController
==================================================
🔧 Création des Sub-tasks...
   ✅ NUT-45 — Créer l'entité Notification
   ✅ NUT-46 — Implémenter NotificationService.Send()
   ✅ NUT-47 — Migration EF Core — table Notifications
   ✅ NUT-48 — Implémenter POST /notifications
   ✅ NUT-49 — Implémenter GET /notifications
   ✅ NUT-50 — Tests d'intégration NotificationsController
==================================================
🎉 Import terminé !
   Epics    : 1/1
   Stories  : 2/2
   Sub-tasks: 6/6
✅ Registre mis à jour : docs/jira-registry.json
```

Puis le frontend :

```bash
python3 playbook/tools/import_jira.py \
   docs/features/notifications/livrable/jira_backlog_feature_notifications_frontend.py
```

---

## Après l'import

### Vérifier le registre

```json
// docs/jira-registry.json — registry["features"][] enrichi, modules inchangés
{
  "backend":  { "max_epic_ref": 5, "max_story_ref": 27, "max_sub_ref": 119, ... },   // inchangé
  "frontend": { "max_epic_ref": 3, "max_story_ref": 135, "max_sub_ref": 178, ... },  // inchangé
  "features": [
    {
      "name": "jira_backlog_feature_notifications_backend",
      "last_import": "2026-05-01",
      "max_epic_ref": 400,
      "max_story_ref": 401,
      "max_sub_ref": 405,
      "epics": [{ "ref": "EPIC-400", "jira_id": "NUT-42", "name": "Notifications — Backend" }]
    },
    {
      "name": "jira_backlog_feature_notifications_frontend",
      "last_import": "2026-05-01",
      "max_epic_ref": 401,
      "max_story_ref": 402,
      "max_sub_ref": 408,
      "epics": [{ "ref": "EPIC-401", "jira_id": "NUT-51", "name": "Notifications — Frontend" }]
    }
  ]
}
```

La prochaine feature commencera à EPIC-402, STORY-403, SUB-409
(`max` sur toutes les entrées de `registry["features"][]`).

### Vérifier dans Jira

- Les Stories apparaissent dans les Epics correspondants
- Les Sub-tasks sont rattachées aux bonnes Stories
- Les labels `feature` permettent de filtrer tous les tickets de la feature
