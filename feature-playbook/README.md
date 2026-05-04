# Feature Playbook

> Playbook **horizontal** — déclenché à tout moment après le premier import Jira d'un module.
> Aucune dépendance de niveau dans le DAG : s'exécute indépendamment des playbooks L0/L1/L2.

---

## Objectif

Ajouter une nouvelle fonctionnalité transversale à un projet existant en analysant l'existant
avant de produire des tickets Jira.

Le feature-playbook est le seul playbook avec une vue **cross-cutting** sur tous les modules —
sa valeur ajoutée est l'analyse de l'existant (gap analysis), pas uniquement la production de tickets.

```
dev-playbook        → produit (périmètre fixe : backend)
frontend-playbook   → produit (périmètre fixe : frontend)
sdk-playbook        → produit (périmètre fixe : SDK)
devops-playbook     → produit (périmètre fixe : DevOps)

feature-playbook    → ANALYSE d'abord, puis délègue à chaque module concerné
```

---

## Prérequis

- Au moins un module importé dans Jira (`docs/jira-registry.json` existant et peuplé)
- Les IDs Jira des Epics existants renseignés dans `docs/jira-registry.json`

---

## Phases

| Phase                          | Livrable                                                              | Rôle                                 |
| ------------------------------ | --------------------------------------------------------------------- | ------------------------------------ |
| FT1 — Feature Brief            | `docs/features/[nom]/feature-brief.md`                                | Définir la feature                   |
| FT2 — Gap Analysis             | `docs/features/[nom]/gap-analysis.md`                                 | Lire l'existant, identifier le delta |
| FT3 — Module Briefs + Backlogs | `docs/features/[nom]/livrable/jira_backlog_feature_[nom]_[module].py` | Produire un backlog par module       |
| FT4 — Import                   | Tickets Jira + registre mis à jour                                    | Importer chaque module               |

**FT2 est la phase centrale** — elle détermine quoi produire et où, avant toute décomposition.

---

## Phase FT1 — Feature Brief

Définir la feature en répondant à :

- **Quoi** : description fonctionnelle
- **Pourquoi** : valeur métier
- **Scope pressenti** : quels modules semblent impactés (backend / frontend / SDK / DevOps)

**Livrable :** `docs/features/[nom]/feature-brief.md`

> Ne pas présumer du scope définitif — FT2 le confirme après lecture de l'existant.

---

## Phase FT2 — Gap Analysis

Lire la documentation de chaque module potentiellement impacté pour identifier :

1. Ce qui **existe déjà** (Epics/Stories couvrant partiellement le besoin)
2. Ce qui **manque** (nouveau travail à ajouter)
3. Le **MODE** à utiliser pour cette feature

Sources à lire :

| Module          | Documentation à lire      |
| --------------- | ------------------------- |
| Backend         | `docs/backend/`           |
| Frontend        | `docs/frontend/`          |
| SDK             | `docs/sdk/`               |
| DevOps          | `docs/devops/`            |
| Epics existants | `docs/jira-registry.json` |

**Résolution selon le cas détecté :**

| Cas                 | Situation                                              | Backlogs produits |
| ------------------- | ------------------------------------------------------ | ----------------- |
| A — feature simple  | Un seul module impacté                                 | 1 backlog         |
| B — multi-modules   | Plusieurs modules impactés                             | N backlogs        |
| C — nouveau service | Aucun travail préalable dans les docs existants        | 1 backlog         |

> **Dans tous les cas :** `MODULE = "feature"`, `MODE = "create"`.
> Chaque feature crée ses propres Epics (plage 400+), indépendants des Epics des modules.
> Les Epics des modules (001–399) sont figés après leur import initial — une feature ne les touche jamais.

**Livrable :** `docs/features/[nom]/gap-analysis.md`

> Valider le gap-analysis avant FT3 — c'est le verrou qualité de ce playbook.

---

## Phase FT3 — Module Briefs + Backlogs

Pour chaque backlog identifié en FT2, produire un fichier Python :

```bash
cp playbook/tools/jira_backlog_template.py \
   docs/features/[nom]/livrable/jira_backlog_feature_[nom]_[scope].py
```

Champs obligatoires dans tous les cas :

```python
MODULE = "feature"   # toujours
MODE   = "create"    # toujours — chaque feature crée ses propres Epics
```

**Refs :** plage 400+ pour toutes les features. Consulter `registry["features"][]` dans
`docs/jira-registry.json` et prendre le `max` sur tous les `max_epic_ref`, `max_story_ref`, `max_sub_ref`
pour trouver le prochain ref disponible.

---

## Phase FT4 — Import Jira

Importer chaque backlog produit en FT3 :

```bash
python3 playbook/tools/import_jira.py \
   docs/features/[nom]/livrable/jira_backlog_feature_[nom]_[scope].py
```

Le script ajoute une entrée dans `registry["features"][]` après chaque import réussi.
Les entrées modules (`registry["backend"]`, `registry["frontend"]` etc.) ne sont **jamais modifiées**.

---

## Structure de sortie

```
docs/
└── features/
    └── [nom-feature]/
        ├── feature-brief.md                              ← FT1
        ├── gap-analysis.md                               ← FT2
        └── livrable/
            ├── jira_backlog_feature_[nom]_backend.py     ← FT3
            ├── jira_backlog_feature_[nom]_frontend.py    ← FT3
            └── ...
```

---

## Guide détaillé

Voir `guides/add-feature.md` pour le processus complet avec exemple (feature Notifications).
