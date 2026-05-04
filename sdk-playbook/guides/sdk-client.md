# Guide — Cadrage SDK Client [Module optionnel]

> **Module indépendant** — démarrable après que le backlog backend est importé dans Jira.
> **Prérequis :** Phase 6.5 ✅ (API spécifiée, contrats REST documentés)
> **Périmètre :** de la décision d'architecture jusqu'au backlog Jira SDK importé.
> **Hors scope :** le code — il vit dans le repository git + Jira.

---

## Quand créer un SDK client ?

| Situation | Décision |
|---|---|
| Un seul frontend | Pas nécessaire — appels API directs suffisent |
| Plusieurs frontends (web + mobile) | Justifié — évite de dupliquer la logique d'appel |
| Frontend externe / partenaire | Fortement recommandé — contrat explicite et versionné |

---

## Ce que le SDK contiendra (à documenter dans le backlog)

- DTOs partagés — mêmes types que l'API (Request / Response)
- Client HTTP typé — un service par ressource
- Gestion d'erreurs centralisée — mapping codes HTTP → exceptions métier
- Gestion du token — refresh automatique du JWT
- Versionnage — aligné sur les versions majeures de l'API (semver)

---

## Comment reprendre ce module (démarrage à froid)

1. Vérifier que les contrats API sont stables (`docs/4.nutrition-specifications-techniques.md`)
2. Décider : génération auto (NSwag, openapi-generator) ou SDK manuel
3. Choisir le langage cible (TypeScript, Kotlin/Swift, C#…)
4. Suivre les phases dans l'ordre

---

## Phase S1 — Décision d'architecture SDK

> À compléter lors du démarrage du module.

- [ ] Langage(s) cible(s)
- [ ] Génération auto depuis OpenAPI ou SDK écrit à la main
- [ ] Stratégie de publication (npm, NuGet, Maven, fichier source)
- [ ] Versionnage (semver, aligné sur l'API)

---

## Phase S2 — Conception du SDK

> À compléter lors du démarrage du module.

Pour chaque ressource API :
- Client HTTP typé (méthodes = endpoints)
- DTOs alignés sur les contrats API (Request / Response)
- Interface d'authentification (injection du token ou gestion interne)
- Gestion d'erreurs (exceptions typées par domaine)

---

## Phase S3 — Backlog Jira SDK ▶ FIN DU MODULE

```
checklist-sdk.md
        ↓ IA génère
docs/sdk/livrable/jira-backlog-decomposition-sdk.md   ← valider
        ↓ IA traduit en Python
docs/sdk/livrable/jira_backlog_sdk.py                 ← copié depuis playbook/tools/jira_backlog_template.py
        ↓ script
python3 playbook/tools/import_jira.py docs/sdk/livrable/jira_backlog_sdk.py
```

Plage de refs : EPIC-200 → EPIC-299 · STORY-200 → STORY-299 · SUB-200 → SUB-299
