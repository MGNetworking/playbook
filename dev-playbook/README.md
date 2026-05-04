# Dev Playbook — Spec-Driven Development

> Méthodologie personnelle pour démarrer et conduire un projet logiciel efficacement.
> Approche : concevoir avant de coder — cas d'usage → domaine → specs → Jira.
> Périmètre : de la conception jusqu'au backlog Jira importé (Phases 0 → 6.5).
> Le code vit dans le repository git + Jira — hors scope du playbook.

---

## Point d'entrée

**Fichier principal :** `methode-projet.md`

Lire l'index en tête de fichier pour naviguer directement à la phase ou section dont tu as besoin. Ne pas lire le fichier de haut en bas — utiliser les plages de lignes de l'index.

---

## Structure

```
dev-playbook/
├── README.md                        ← ce fichier — point d'entrée
├── methode-projet.md                ← méthode complète Phases 0 → 6.5 (avec index)
├── guides/
│   ├── specs-frontend.md            ← guide Phase 5 — identifier les écrans
│   └── jira-scrum.md                ← guide Phase 6.5 — backlog Jira (avec index)
├── templates/
│   └── suivi-projet.md              ← gabarit suivi de projet à copier en Phase 0
└── references/
    └── references-ddd.md            ← glossaire DDD, architecture, template CLAUDE.md, Mermaid
```

> Les outils Jira (moteur + template + credentials) sont dans `playbook/tools/` — partagés entre tous les playbooks.

---

## Ce qu'une IA doit charger

| Besoin | Fichier à charger | Lignes |
|---|---|---|
| Vue d'ensemble de la méthode | `methode-projet.md` — Index | 33 – 56 |
| Phase en cours | `methode-projet.md` — plage de la phase (voir index) | ~50 lignes |
| Identifier les écrans (Phase 5) | `guides/specs-frontend.md` | complet |
| Backlog Jira (Phase 6.5) | `guides/jira-scrum.md` — plage ciblée (voir index) | ~20 lignes |
| Outils Jira (moteur + template) | `playbook/tools/` | voir playbook/README.md |
| Glossaire DDD / Architecture | `references/references-ddd.md` | à la demande |
| Gabarits à copier | `templates/` | à la demande |

---

## Ordre de démarrage d'un projet

```
Phase 0   →  Copier templates/ → remplir SUIVI-PROJET.md + créer CLAUDE.md
Phase 1   →  Cas d'usage + acteurs + MVP
Phase 2   →  Specs fonctionnelles + règles métier
Phase 3   →  Modèle domaine + diagramme de classes
Phase 4   →  Workflows des flux clés
Phase 5   →  Specs Frontend (cf. guides/specs-frontend.md)
Phase 6   →  Validation cohérence + checklist d'implémentation
Phase 6.5 →  Backlog Jira (cf. guides/jira-scrum.md)
              checklist → decomposition.md (valider) → jira_backlog.py → import
              ▶ FIN DU PLAYBOOK
```

> Règle fondamentale : synchroniser toute la documentation à la fin de chaque phase avant de passer à la suivante.
> Le code est géré dans le repository git + Jira — le playbook ne couvre pas cette partie.

---

## Modules complémentaires — autres playbooks

Une fois le backlog backend importé dans Jira, d'autres playbooks peuvent cadrer les modules suivants :

| Module | Playbook | Guide de démarrage |
|---|---|---|
| Frontend | `playbook/frontend-playbook/` | `frontend-playbook/guides/frontend-implementation.md` |
| SDK Client | `playbook/sdk-playbook/` | `sdk-playbook/guides/sdk-client.md` |
| DevOps | `playbook/devops-playbook/` | — |

Voir `playbook/README.md` pour le graphe de dépendances complet (DAG).
