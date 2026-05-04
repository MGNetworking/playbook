# Suivi de projet — [Nom du projet]

> **Objectif :** [Décrire en une phrase le but du produit — ex: API SaaS de gestion X — backend ASP.NET Core 8, architecture DDD 4 couches, déploiement Kubernetes]
> **Stack :** [Langage] · [Framework] · [ORM] · [Base de données] · [Auth] · [Tests]
> **Dernière mise à jour :** [date]

---

## Légende

| Symbole | Signification             |
| ------- | ------------------------- |
| ✅      | Terminé                   |
| 🔄      | En cours                  |
| ⏳      | À faire (prochaine étape) |
| 🔲      | À faire (future étape)    |
| ❓      | En attente de décision    |
| ⚠️      | Problème identifié        |

---

## Ordre de conception du projet

> **Où on en est : Phase [X] — [nom de l'étape en cours]**
> **Convention :** `🔲` à faire | `✅ livrable-1.md · livrable-2.md` — livrables produits listés dans la colonne

| Phase | Étape                                                                        | Statut |
| ----- | ---------------------------------------------------------------------------- | ------ |
| 0     | Initialisation — structure documentation + stack                             | 🔲     |
| 1     | Cadrage métier — besoin, acteurs, cas d'usage, MVP                           | 🔲     |
| 2     | Conception fonctionnelle — specs, règles métier, contraintes                 | 🔲     |
| 3     | Modélisation domaine — agrégats, attributs, invariants, diagramme de classes | 🔲     |
| 4     | Workflows — flux clés, décisions infrastructure                              | 🔲     |
| 5     | Specs Frontend — écrans, données affichées, contrats API                     | 🔲     |
| 6     | Validation cohérence — checklist d'implémentation, tous les gaps résolus     | 🔲     |
| 6.5   | Backlog Jira — checklist → decomposition.md → jira_backlog.py → import ▶ FIN | 🔲     |

> **La suite est gérée dans Jira** — le playbook s'arrête ici.

---

## Planning estimatif

> Les durées sont des estimations — à ajuster selon la complexité du projet.

| Phase | Description                    | Durée estimée | Date cible |
| ----- | ------------------------------ | ------------- | ---------- |
| 0     | Initialisation                 | 1 h           |            |
| 1     | Cadrage métier                 | 2–4 h         |            |
| 2     | Conception fonctionnelle       | 3–5 h         |            |
| 3     | Modélisation domaine           | 3–6 h         |            |
| 4     | Workflows                      | 2–4 h         |            |
| 5     | Specs Frontend                 | 1–3 h         |            |
| 6     | Validation cohérence           | 1–2 h         |            |
| 6.5   | Backlog Jira                   | 1–2 h         |            |

---

## Décisions tranchées ✅

| #   | Question                       | Décision                                |
| --- | ------------------------------ | --------------------------------------- |
| 1   | [Question métier ou technique] | [Décision prise + justification courte] |

---

## Décisions en attente ❓

| #   | Sujet              | Détail                                |
| --- | ------------------ | ------------------------------------- |
| A   | [Sujet à trancher] | [Description + impact si non tranché] |

---

## Corrections à apporter ⚠️

- [ ] [Correction identifiée — fichier concerné]

---

## Workflows à créer 🔲

| Workflow        | Statut |
| --------------- | ------ |
| [Nom du flux 1] | 🔲     |
| [Nom du flux 2] | 🔲     |
