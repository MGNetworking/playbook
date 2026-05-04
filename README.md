# Playbook — Système de gestion de projets logiciels

> Collection de playbooks réutilisables pour conduire un projet de bout en bout.
> Chaque playbook est indépendant mais peut consommer les livrables des playbooks précédents.

---

## Architecture — Graphe de dépendances (DAG)

```
dev-playbook          (Level 0 — aucune dépendance)
      │
      ├──────────────────────┐
      ▼                      ▼
frontend-playbook       sdk-playbook
(Level 1)               (Level 1)
      │                      │
      └──────────┬───────────┘
                 ▼
          devops-playbook
          (Level 2 — dépend de tout ce qui précède)


feature-playbook      (Horizontal — hors DAG, déclenché à tout moment après le premier import)
```

> Règle : un playbook ne dépend jamais d'un playbook de niveau égal ou supérieur.
> Pas de dépendance circulaire possible.
> `feature-playbook` est orthogonal au DAG — il s'exécute après n'importe quel import initial.

---

## Playbooks disponibles

| Playbook             | Scope                                     | Entrée                                       | Sortie                                            |
| -------------------- | ----------------------------------------- | -------------------------------------------- | ------------------------------------------------- |
| `dev-playbook/`      | Conception → Backlog Jira backend         | Rien                                         | Specs · Domaine · Checklist · Backlog Jira        |
| `frontend-playbook/` | Cadrage frontend [optionnel]              | Livrables dev-playbook                       | Specs frontend · Checklist · Backlog Jira         |
| `sdk-playbook/`      | Cadrage SDK client [optionnel]            | Livrables dev-playbook                       | Specs SDK · Checklist · Backlog Jira              |
| `devops-playbook/`   | Cadrage DevOps [optionnel]                | Livrables de tout ce qui précède             | Specs DevOps · Checklist · Backlog Jira           |
| `feature-playbook/`  | Ajout de feature post-import [horizontal] | `docs/jira-registry.json` + `docs/[module]/` | Gap Analysis · Backlogs par module · Tickets Jira |

> **Règle commune :** chaque playbook s'arrête au backlog Jira importé. Le code vit dans le repository git + Jira.

---

## Outil partagé — Import Jira

**Workflow identique pour tous les playbooks :**

```
1. Copier  playbook/tools/jira_backlog_template.py
           → docs/backend/livrable/jira_backlog.py                  (backend, MODE=create)
           → docs/frontend/livrable/jira_backlog_frontend.py         (frontend, MODE=create)
           → docs/sdk/livrable/jira_backlog_sdk.py                   (SDK, MODE=create)
           → docs/devops/livrable/jira_backlog_devops.py             (DevOps, MODE=create)
           → docs/features/[nom]/livrable/jira_backlog_feature_[nom]_[module].py  (feature, MODE=add)

2. Demander à l'IA de remplir depuis la checklist du playbook

3. Copier  playbook/tools/.env.example → docs/backend/livrable/.env  (une seule fois)

4. Exécuter depuis la racine du workspace :
   python3 playbook/tools/import_jira.py docs/backend/livrable/jira_backlog.py
   python3 playbook/tools/import_jira.py docs/frontend/livrable/jira_backlog_frontend.py
   → docs/jira-registry.json est mis à jour automatiquement après chaque import
```

**Convention des plages de refs (évite les collisions entre modules) :**

| Module                    | EPIC    | STORY   | SUB     | MODULE dans le backlog |
| ------------------------- | ------- | ------- | ------- | ---------------------- |
| Backend                   | 001–099 | 001–099 | 001–099 | `"backend"`            |
| Frontend                  | 100–199 | 100–199 | 100–199 | `"frontend"`           |
| SDK                       | 200–299 | 200–299 | 200–299 | `"sdk"`                |
| DevOps                    | 300–399 | 300–399 | 300–399 | `"devops"`             |
| Features (tous les cas)   | 400+    | 400+    | 400+    | `"feature"`            |

> Les features utilisent **toujours** `MODULE="feature"` et `MODE="create"` — elles créent leurs propres Epics
> dans la plage 400+, indépendants des Epics des modules. Les entrées modules (`registry["backend"]` etc.)
> sont figées après leur import initial et ne sont jamais modifiées par une feature.

---

## Structure

```
playbook/
├── README.md                ← ce fichier — point d'entrée global
├── tools/
│   ├── import_jira.py       ← outil partagé d'import Jira (modes create / add)
│   ├── jira_backlog_template.py  ← template données backlog
│   └── .env.example         ← template credentials Jira
├── dev-playbook/            ← Spec-Driven Development (Level 0)
├── frontend-playbook/       ← Implémentation frontend (Level 1)
├── sdk-playbook/            ← SDK client (Level 1)
├── devops-playbook/         ← DevOps et déploiement (Level 2)
└── feature-playbook/        ← Ajout de features post-import (Horizontal)

docs/
├── jira-registry.json       ← registre Jira centralisé — mis à jour automatiquement par import_jira.py
└── features/
    └── [nom-feature]/       ← livrables feature-playbook (FT1→FT4)
        ├── feature-brief.md
        ├── gap-analysis.md
        └── livrable/
            └── jira_backlog_feature_[nom]_[module].py
```

---

## Démarrer un projet

1. Toujours commencer par `dev-playbook/` — lire son `README.md`
2. Une fois le backend terminé, choisir les playbooks Level 1 selon le besoin
3. `devops-playbook/` en dernier — quand tout ce qui doit être déployé est prêt
