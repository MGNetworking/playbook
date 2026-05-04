# Frontend Playbook

> **Level 1** — dépend de `dev-playbook/`
> Scope : cadrage frontend — de la conception jusqu'au backlog Jira importé.
> Hors scope : le code — il vit dans le repository git + Jira.
> Statut : **structure créée — contenu à construire**

---

## Ce playbook consomme (depuis dev-playbook)

| Livrable               | Fichier                                               | Utilité                                  |
| ---------------------- | ----------------------------------------------------- | ---------------------------------------- |
| Contrats API par écran | `docs/backend/livrable/specs-frontend.md`                     | PRIMARY — données + appels API par écran |
| Endpoints REST         | `docs/backend/4.[projet]-specifications-techniques.md`        | Formats Request/Response                 |
| Modèle de données      | `docs/backend/domaine/Diagramme-classes.md`                   | Champs disponibles par entité            |
| Flux authentification  | `docs/backend/annexes/workflow_Flux_authentification.mermaid` | Keycloak PKCE / Auth Code                |

---

## Ce playbook produit

- Documentation de cadrage (architecture, composants, modèle d'état, intégration API)
- `docs/frontend/livrable/checklist-frontend.md` — checklist d'implémentation frontend
- `docs/frontend/livrable/jira_backlog_frontend.py` — backlog Jira frontend (EPIC-100 → 199)

---

## Phases

```
Phase F1  →  Architecture (framework, routing, state management, auth)
Phase F2  →  Décomposition en composants (depuis specs-frontend.md)
Phase F3  →  Modèle d'état (local / global / serveur)
Phase F4  →  Couche d'intégration API (services par domaine)
Phase F5  →  Backlog Jira frontend  ▶ FIN DU PLAYBOOK
```

---

## Séquence Jira (Phase F5)

Même séquence que dev-playbook — deux étapes avant l'import :

```
checklist-frontend.md
        ↓ IA génère
jira-backlog-decomposition-frontend.md   ← valider avant de continuer
        ↓ IA traduit en Python
jira_backlog_frontend.py                 ← copié depuis playbook/tools/jira_backlog_template.py
        ↓ script
python3 playbook/tools/import_jira.py docs/frontend/livrable/jira_backlog_frontend.py
```

Plage de refs : EPIC-100 → EPIC-199 · STORY-100 → STORY-199 · SUB-100 → SUB-199

---

## Structure prévue

```
frontend-playbook/
├── README.md         ← ce fichier — contrat de dépendance + point d'entrée
└── guides/           ← guides par phase (à créer)
```
