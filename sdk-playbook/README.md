# SDK Playbook

> **Level 1** — dépend de `dev-playbook/`
> Scope : cadrage SDK client — de la décision d'architecture jusqu'au backlog Jira importé.
> Hors scope : le code — il vit dans le repository git + Jira.
> Statut : **structure créée — contenu à construire**

---

## Quand utiliser ce playbook ?

| Situation | Décision |
|---|---|
| Un seul frontend | Pas nécessaire — appels API directs suffisent |
| Plusieurs frontends (web + mobile) | Justifié — évite de dupliquer la logique d'appel |
| Frontend externe / partenaire | Fortement recommandé — contrat explicite et versionné |

---

## Ce playbook consomme (depuis dev-playbook)

| Livrable | Fichier | Utilité |
|---|---|---|
| Endpoints REST | `docs/backend/4.[projet]-specifications-techniques.md` | Contrats API complets |
| Schéma OpenAPI | `GET /swagger/v1/swagger.json` (runtime) | Génération automatique possible |
| Modèle de données | `docs/backend/domaine/Diagramme-classes.md` | Types / DTOs à reproduire |

---

## Ce playbook produit

- Documentation de cadrage (architecture SDK, conception par ressource)
- `docs/sdk/livrable/checklist-sdk.md` — checklist d'implémentation SDK
- `docs/sdk/livrable/jira_backlog_sdk.py` — backlog Jira SDK (EPIC-200 → 299)

---

## Phases

```
Phase S1  →  Décision architecture (langage cible, génération auto ou manuel, publication)
Phase S2  →  Conception SDK (clients par ressource, DTOs, gestion erreurs)
Phase S3  →  Backlog Jira SDK  ▶ FIN DU PLAYBOOK
```

---

## Séquence Jira (Phase S3)

Même séquence que dev-playbook — deux étapes avant l'import :

```
checklist-sdk.md
        ↓ IA génère
jira-backlog-decomposition-sdk.md   ← valider avant de continuer
        ↓ IA traduit en Python
jira_backlog_sdk.py                 ← copié depuis playbook/tools/jira_backlog_template.py
        ↓ script
python3 playbook/tools/import_jira.py docs/sdk/livrable/jira_backlog_sdk.py
```

Plage de refs : EPIC-200 → EPIC-299 · STORY-200 → STORY-299 · SUB-200 → SUB-299

---

## Structure prévue

```
sdk-playbook/
├── README.md         ← ce fichier — contrat de dépendance + point d'entrée
└── guides/           ← guides par phase (à créer)
```
