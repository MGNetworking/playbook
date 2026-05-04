# jira_backlog_template.py — Template générique de données backlog Jira
#
# WORKFLOW :
#   1. Copier ce fichier dans le dossier livrable/ du module concerné :
#        docs/backend/livrable/jira_backlog.py           ← backend  (dev-playbook)
#        docs/frontend/livrable/jira_backlog_frontend.py ← frontend (frontend-playbook)
#        docs/sdk/livrable/jira_backlog_sdk.py           ← SDK      (sdk-playbook)
#        docs/devops/livrable/jira_backlog_devops.py     ← DevOps   (devops-playbook)
#        docs/backend/livrable/jira_backlog_feature_[nom].py ← feature (feature-playbook)
#
#   2. Choisir le MODE :
#        "create" → crée les Epics + Stories + Sub-tasks (premier import d'un module)
#        "add"    → ajoute Stories + Sub-tasks à des Epics existants (feature ou ajout)
#
#   3. En mode "add" : renseigner EXISTING_EPICS depuis docs/jira-registry.json
#        EXISTING_EPICS = { "EPIC-001": "NUT-1", "EPIC-002": "NUT-5" }
#
#   4. Lancer depuis la racine du workspace :
#        python3 playbook/tools/import_jira.py docs/backend/livrable/jira_backlog.py
#        → le registre docs/jira-registry.json est mis à jour automatiquement
#
# RÈGLE DE MAPPING : ## → Epic | ### → Story | items liste → Sub-task
#
# CONVENTION DES PLAGES DE REFS (évite les collisions entre modules) :
#   Backend  : EPIC-001 → EPIC-099  |  STORY-001 → STORY-099  |  SUB-001 → SUB-099
#   Frontend : EPIC-100 → EPIC-199  |  STORY-100 → STORY-199  |  SUB-100 → SUB-199
#   SDK      : EPIC-200 → EPIC-299  |  STORY-200 → STORY-299  |  SUB-200 → SUB-299
#   DevOps   : EPIC-300 → EPIC-399  |  STORY-300 → STORY-399  |  SUB-300 → SUB-399
#
# FORMAT DES TUPLES :
#   EPICS    : (ref, summary, description, label)
#   STORIES  : (ref, summary, description, priority, label, story_points, epic_ref)
#   SUBTASKS : (ref, summary, description, priority, label, story_ref)
#
# LABELS    : libres — exemples : domain | frontend | sdk | devops | tests | feature
# PRIORITÉS : Highest | High | Medium | Low | Lowest

# ── Mode d'import ─────────────────────────────────────────────────────────────
# "create" : premier import d'un module — crée les Epics, Stories et Sub-tasks
# "add"    : ajout sur module existant — ajoute Stories/Sub-tasks aux Epics existants
MODE = "create"

# ── Epics existants (MODE "add" uniquement) ───────────────────────────────────
# Renseigner depuis docs/jira-registry.json avant de lancer l'import.
# Clé = ref locale (ex: "EPIC-001"), Valeur = ID Jira réel (ex: "NUT-1")
EXISTING_EPICS = {
    # "EPIC-001": "NUT-1",
    # "EPIC-002": "NUT-5",
}

# ── Module (pour mise à jour du registre) ─────────────────────────────────────
# Valeurs : "backend" | "frontend" | "sdk" | "devops" | "feature"
MODULE = "backend"

# ── Données backlog ───────────────────────────────────────────────────────────

EPICS = [
    # ("EPIC-001", "Nom de l'epic", "Description de l'epic.", "label"),
]

STORIES = [
    # ── Nom Epic ────────────────────────────────────────────────────────────────
    # ("STORY-001", "Nom de la story", "Description.", "Medium", "label", 3, "EPIC-001"),
]

SUBTASKS = [
    # ── STORY-001 : Nom de la story ─────────────────────────────────────────────
    # ("SUB-001", "Nom de la sub-task", "Description.", "Medium", "label", "STORY-001"),
]
