# Guide — Définir les écrans Frontend depuis les cas d'usage

> Référencé dans `methode-projet.md` — Phase 5 (Specs Frontend)
> Objectif : transformer une liste de cas d'usage en liste d'écrans cohérente, avant de définir les contrats API.

---

## Principe fondamental

Un écran = **une intention utilisateur principale**.

On ne part pas d'une maquette ni d'une intuition de navigation. On part des cas d'usage : chacun représente une action que l'utilisateur veut accomplir. Les écrans émergent de ces actions.

---

## Les 4 étapes

### Étape 1 — Un UC = un candidat écran

Lister tous les cas d'usage et en faire un candidat écran. À ce stade, pas de filtre — tout UC qui implique une interaction utilisateur est un candidat.

```
UC02 → candidat "Profil"
UC03 → candidat "Besoins nutritionnels"
UC04 → candidat "Créer un plan"
UC05 → candidat "Lancer un régime"
...
```

### Étape 2 — Regrouper les UCs au même contexte

**Question clé :** *"L'utilisateur fait-il ces deux actions dans le même élan, sans changer d'intention ?"*

Si oui → un seul écran. Si l'utilisateur doit "changer de mode mental" → deux écrans séparés.

**Exemples :**
- UC02 (renseigner données physiologiques) + UC03 (consulter BMR/TDEE) → même contexte → **écran Profil**
- UC04 (créer un plan) + liste des plans → même contexte → **écran Gestion DietPlans**
- UC08 (bilan journalier) + UC09 (tendances hebdomadaires) → même contexte, filtre de période → **écran Bilan nutritionnel**

### Étape 3 — Identifier les UCs embarqués

Certains UCs ne méritent pas d'écran dédié : ce sont des *sous-actions* d'un autre UC, qui s'exécutent sans quitter le contexte courant.

**Critère :** *"Cet UC peut-il s'exécuter sans que l'utilisateur quitte son écran actuel ?"*

Si oui → UC embarqué, pas d'écran propre.

**Exemples :**
- UC06 (rechercher un aliment) n'existe que dans l'acte de saisir un repas → embarqué dans **Saisie repas**
- Ajouter un MealItem → embarqué dans **Saisie repas**

### Étape 4 — Éliminer les UCs sans écran

Deux cas d'élimination :

| Raison | Exemple | Action |
|---|---|---|
| UC délégué à un service externe | UC01 — authentification via Keycloak | Le frontend redirige, aucun écran à spécifier |
| UC hors périmètre (vision future) | UC10 — recommandations alimentaires | À exclure jusqu'à la prochaine version |

---

## Résultat type — tableau de synthèse

| UC(s) | Règle appliquée | Écran résultant |
|---|---|---|
| UC02 + UC03 | Regroupement (même contexte) | Profil utilisateur |
| UC04 | Candidat direct | Gestion DietPlans |
| UC05 | Candidat direct | Diet active |
| UC06 | Embarqué dans UC07 | *(dans Saisie repas)* |
| UC07 | Candidat direct | Saisie repas |
| UC08 + UC09 | Regroupement (même contexte, filtre période) | Bilan nutritionnel |
| UC11 | Candidat direct | Suivi du poids |
| UC12 | Candidat direct | RGPD |
| UC01 | Délégué à Keycloak | *(aucun écran)* |
| UC10 | Hors périmètre MVP | *(aucun écran)* |

---

## Critères de qualité d'un bon écran

- **Une seule raison d'être** — l'utilisateur sait immédiatement pourquoi il est là
- **Dérivé d'au moins un UC** — pas d'écran inventé sans besoin métier identifié
- **Aucun UC oublié** — vérifier que chaque UC du MVP est couvert (écran propre ou embarqué)
- **Pas de redondance** — deux écrans ne font pas la même chose

---

## Format de documentation d'un écran

Une fois les écrans identifiés, chacun est documenté dans `docs/backend/livrable/specs-frontend.md` avec ce format :

```
## Écran N — [Nom]

**But :** [Ce que l'utilisateur fait sur cet écran]

**Données affichées**
- [Donnée 1 — source dans le modèle domaine]
- [Donnée 2]

**Appels API**
- [MÉTHODE] /endpoint  →  { champs retournés }

**Actions disponibles**
- [Action 1 — appel API correspondant]
```

> Ce format est agnostique du support (web, mobile, desktop) — il ne décrit pas le layout visuel, uniquement les données et les contrats API.

