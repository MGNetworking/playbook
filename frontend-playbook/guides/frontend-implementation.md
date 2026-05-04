# Guide — Cadrage Frontend [Module optionnel]

> **Module indépendant** — démarrable après que le backlog backend est importé dans Jira.
> **Prérequis :** Phase 6.5 ✅ (backlog backend dans Jira, API spécifiée et stable)
> **Périmètre :** de la conception jusqu'au backlog Jira frontend importé.
> **Hors scope :** le code — il vit dans le repository git + Jira.
> **Point de départ :** `docs/backend/livrable/specs-frontend.md` — les écrans et leurs contrats API sont déjà définis (Phase 5).

---

## Comment reprendre ce module (démarrage à froid)

1. Lire `docs/backend/livrable/specs-frontend.md` — écrans, données affichées, appels API par écran
2. Lire `docs/backend/domaine/Diagramme-classes.md` — modèle de données de référence
3. Suivre les phases dans l'ordre

---

## Phase F1 — Architecture frontend

> À compléter lors du démarrage du module.

Décisions à documenter avant de générer le backlog :

- [ ] Stack choisie (framework, langage, tooling)
- [ ] Stratégie de routing
- [ ] Gestion de l'état (local / global / serveur)
- [ ] Authentification côté client (Keycloak PKCE ou Authorization Code Flow)
- [ ] Stratégie de déploiement (SPA statique, SSR, mobile natif)

---

## Phase F2 — Décomposition en composants

> À compléter lors du démarrage du module.

Source : `docs/backend/livrable/specs-frontend.md` — écrans identifiés.

Pour chaque écran :
- Identifier les composants réutilisables (formulaires, listes, cards)
- Définir l'arbre de composants (parent / enfants)
- Identifier les composants partagés entre écrans

---

## Phase F3 — Modèle d'état

> À compléter lors du démarrage du module.

Pour chaque écran / composant :
- Quelles données sont locales (état du formulaire) ?
- Quelles données sont globales (utilisateur connecté, entité active) ?
- Quelles données viennent du serveur (à fetcher à la demande) ?

---

## Phase F4 — Couche d'intégration API

> À compléter lors du démarrage du module.

- Un service par domaine métier
- Gestion centralisée des erreurs HTTP
- Gestion du token JWT (refresh automatique)
- Si SDK client prévu → voir `playbook/sdk-playbook/guides/sdk-client.md`

---

## Phase F5 — Backlog Jira Frontend ▶ FIN DU MODULE

```
checklist-frontend.md
        ↓ IA génère
docs/frontend/livrable/jira-backlog-decomposition-frontend.md   ← valider
        ↓ IA traduit en Python
docs/frontend/livrable/jira_backlog_frontend.py                 ← copié depuis playbook/tools/jira_backlog_template.py
        ↓ script
python3 playbook/tools/import_jira.py docs/frontend/livrable/jira_backlog_frontend.py
```

Plage de refs : EPIC-100 → EPIC-199 · STORY-100 → STORY-199 · SUB-100 → SUB-199
