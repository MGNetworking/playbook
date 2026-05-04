# DevOps Playbook

> **Level 2** — dépend de `dev-playbook/` + optionnellement `frontend-playbook/` et `sdk-playbook/`
> Scope : tout ce qui vient après que le code est prêt à être déployé.
> Statut : **structure créée — contenu à construire**

---

## Ce playbook consomme

### Depuis dev-playbook/ (obligatoire)

| Livrable                             | Utilité                   |
| ------------------------------------ | ------------------------- |
| Repository git backend               | Base du pipeline CI/CD    |
| Architecture projet (4 couches .NET) | Structure des Dockerfiles |
| Variables d'environnement / secrets  | Configuration Kubernetes  |
| Port et configuration API            | Ingress / Service K8s     |

### Depuis frontend-playbook/ (si frontend déployé)

| Livrable                          | Utilité                  |
| --------------------------------- | ------------------------ |
| Repository git frontend           | Pipeline CI/CD frontend  |
| Type de build (SPA statique, SSR) | Stratégie de déploiement |

### Depuis sdk-playbook/ (si SDK publié)

| Livrable                    | Utilité                          |
| --------------------------- | -------------------------------- |
| Pipeline de publication SDK | Intégration dans le CI/CD global |

---

## Périmètre

| Phase | Sujet                                                        | Statut          |
| ----- | ------------------------------------------------------------ | --------------- |
| D1    | Git — branches, conventions de commit, protection de branche | 🔲 À construire |
| D2    | CI/CD — pipeline build + tests + lint automatiques           | 🔲 À construire |
| D3    | Docker — Dockerfile, docker-compose, multi-stage build       | 🔲 À construire |
| D4    | Kubernetes — déploiement, services, ingress, secrets         | 🔲 À construire |
| D5    | Monitoring / Observabilité — logs, métriques, alertes        | 🔲 À construire |

---

## Ce qui n'est PAS dans ce playbook

- Conception (domaine, specs, workflows) → `dev-playbook/`
- Implémentation frontend → `frontend-playbook/`
- SDK client → `sdk-playbook/`

---

## Séquence Jira (Phase D6 — à créer)

Même séquence que dev-playbook — deux étapes avant l'import :

```
checklist-devops.md
        ↓ IA génère
jira-backlog-decomposition-devops.md   ← valider avant de continuer
        ↓ IA traduit en Python
jira_backlog_devops.py                 ← copié depuis playbook/tools/jira_backlog_template.py
        ↓ script
python3 playbook/tools/import_jira.py docs/devops/livrable/jira_backlog_devops.py
```

Plage de refs : EPIC-300 → EPIC-399 · STORY-300 → STORY-399 · SUB-300 → SUB-399

---

## Structure prévue

```
devops-playbook/
├── README.md         ← ce fichier — contrat de dépendance + point d'entrée
└── guides/           ← un guide par phase DevOps
    ├── git.md        ← D1
    ├── cicd.md       ← D2
    ├── docker.md     ← D3
    ├── kubernetes.md ← D4
    └── monitoring.md ← D5
```
