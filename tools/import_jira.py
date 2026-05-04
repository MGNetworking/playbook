#!/usr/bin/env python3
"""
Moteur d'import Jira — générique, réutilisable entre projets.

Usage (depuis la racine du workspace) :
    python3 playbook/tools/import_jira.py docs/backend/livrable/jira_backlog.py
    python3 playbook/tools/import_jira.py docs/frontend/livrable/jira_backlog_frontend.py
    python3 playbook/tools/import_jira.py docs/sdk/livrable/jira_backlog_sdk.py

Modes :
    MODE = "create"  → crée Epics + Stories + Sub-tasks (premier import d'un module)
    MODE = "add"     → ajoute Stories + Sub-tasks à des Epics existants (feature ou ajout)

Après chaque import réussi, docs/jira-registry.json est mis à jour automatiquement.

Prérequis :
    - <backlog_file>  rempli depuis le template (playbook/tools/jira_backlog_template.py)
    - docs/backend/livrable/.env rempli depuis le template (playbook/tools/.env.example)

Convention des plages de refs par module :
    Backend  : EPIC-001 → EPIC-099  |  STORY-001 → STORY-099  |  SUB-001 → SUB-099
    Frontend : EPIC-100 → EPIC-199  |  STORY-100 → STORY-199  |  SUB-100 → SUB-199
    SDK      : EPIC-200 → EPIC-299  |  STORY-200 → STORY-299  |  SUB-200 → SUB-299
    DevOps   : EPIC-300 → EPIC-399  |  STORY-300 → STORY-399  |  SUB-300 → SUB-399

Vérification de l'environnement :
    python3 --version
    python3 -c "import requests; print('OK')"
    # Si erreur : pip3 install requests --break-system-packages
"""

import json
import os
import sys
import time
import importlib.util
import requests
from datetime import date
from requests.auth import HTTPBasicAuth
from pathlib import Path

# ── Chargement du fichier backlog (chemin relatif au CWD) ─────────────────────
def load_backlog(backlog_filename):
    backlog_path = Path(backlog_filename)
    if not backlog_path.is_absolute():
        backlog_path = Path.cwd() / backlog_filename

    if not backlog_path.exists():
        print(f"❌ Fichier backlog introuvable : {backlog_path}")
        print(f"   1. Copie playbook/tools/jira_backlog_template.py → {backlog_filename}")
        print(f"   2. Remplis les listes EPICS, STORIES et SUBTASKS")
        print(f"   3. Relance : python3 playbook/tools/import_jira.py {backlog_filename}")
        sys.exit(1)

    module_name = backlog_filename.replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, backlog_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    MODE           = getattr(mod, 'MODE', 'create')
    EXISTING_EPICS = getattr(mod, 'EXISTING_EPICS', {})
    MODULE         = getattr(mod, 'MODULE', 'backend')

    if MODE not in ("create", "add"):
        print(f"❌ MODE invalide : '{MODE}'. Valeurs acceptées : 'create' ou 'add'.")
        sys.exit(1)

    if MODULE == "feature" and MODE != "create":
        print(f"❌ MODULE 'feature' requiert MODE='create'.")
        print("   Les features créent toujours leurs propres Epics — elles ne modifient jamais les modules existants.")
        sys.exit(1)

    if MODE == "create" and not mod.EPICS:
        print(f"❌ MODE 'create' : la liste EPICS est vide.")
        print("   Remplis EPICS avant de lancer le script en mode 'create'.")
        sys.exit(1)

    if MODE == "add" and not EXISTING_EPICS:
        print(f"❌ MODE 'add' : EXISTING_EPICS est vide.")
        print("   Renseigne EXISTING_EPICS depuis docs/jira-registry.json avant de lancer le script.")
        sys.exit(1)

    if not mod.STORIES:
        print(f"❌ La liste STORIES est vide.")
        sys.exit(1)

    return mod.EPICS, mod.STORIES, mod.SUBTASKS, MODE, EXISTING_EPICS, MODULE

# ── Chargement .env depuis docs/backend/livrable/ ────────────────────────────
def load_env():
    env_path = Path.cwd() / "docs" / "backend" / "livrable" / ".env"

    if not env_path.exists():
        print("❌ docs/backend/livrable/.env introuvable.")
        print("   Copie playbook/tools/.env.example vers docs/backend/livrable/.env et remplis les valeurs.")
        sys.exit(1)

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

# ── Vérification préalable — évite d'écraser un module existant en mode create ─
def check_registry_conflict(module, mode):
    registry_path = Path.cwd() / "docs" / "jira-registry.json"
    if mode != "create" or not registry_path.exists():
        return
    with open(registry_path) as f:
        registry = json.load(f)
    if registry.get(module) is not None:
        print(f"\n❌ MODULE '{module}' existe déjà dans docs/jira-registry.json.")
        print(f"   MODE='create' écraserait les Epics enregistrés et briserait les imports futurs.")
        print(f"   → Utilise MODE='add' pour ajouter des Stories/Sub-tasks à un module existant.")
        sys.exit(1)

# ── Mise à jour automatique du registre Jira ──────────────────────────────────
def update_registry(module, epic_keys, story_keys, epics_data, stories_data, subtasks_data, mode, backlog_file):
    registry_path = Path.cwd() / "docs" / "jira-registry.json"

    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = {"backend": None, "frontend": None, "sdk": None, "devops": None, "features": []}

    today = date.today().isoformat()

    def max_ref(data):
        return max((int(r.split("-")[1]) for r, *_ in data), default=0) if data else 0

    if module == "feature":
        entry = {
            "name":          Path(backlog_file).stem,
            "last_import":   today,
            "max_epic_ref":  max_ref(epics_data),
            "max_story_ref": max_ref(stories_data),
            "max_sub_ref":   max_ref(subtasks_data),
            "epics": [
                {"ref": ref, "jira_id": epic_keys.get(ref), "name": summary}
                for ref, summary, *_ in epics_data
            ],
        }
        if not isinstance(registry.get("features"), list):
            registry["features"] = []
        registry["features"].append(entry)
    else:
        current = registry.get(module) or {}
        current["last_import"] = today

        if mode == "create":
            current["max_epic_ref"]  = max_ref(epics_data)
            current["max_story_ref"] = max_ref(stories_data)
            current["max_sub_ref"]   = max_ref(subtasks_data)
            current["epics"] = [
                {"ref": ref, "jira_id": epic_keys.get(ref), "name": summary}
                for ref, summary, *_ in epics_data
            ]
        else:  # "add"
            current["max_story_ref"] = max(current.get("max_story_ref", 0), max_ref(stories_data))
            current["max_sub_ref"]   = max(current.get("max_sub_ref", 0), max_ref(subtasks_data))

        registry[module] = current

    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Registre mis à jour : docs/jira-registry.json")

# ── Helpers ────────────────────────────────────────────────────────────────────
def adf(text):
    """Texte brut → Atlassian Document Format."""
    return {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}]
    }

def create_issue(payload, auth, headers, api):
    r = requests.post(f"{api}/issue", auth=auth, headers=headers, json=payload)
    if r.status_code in (200, 201):
        return r.json()["key"]
    print(f"   ❌ Erreur {r.status_code}: {r.text[:200]}")
    return None

def get_subtask_type_name(project_key, auth, headers, api):
    r = requests.get(f"{api}/project/{project_key}", auth=auth, headers=headers)
    r.raise_for_status()
    types = r.json().get("issueTypes", [])
    for t in types:
        if "sub" in t["name"].lower() or "sous" in t["name"].lower():
            return t["name"]
    available = [t["name"] for t in types]
    print(f"❌ Aucun type Sub-task détecté. Types disponibles : {available}")
    sys.exit(1)

# ── Main ───────────────────────────────────────────────────────────────────────
if len(sys.argv) < 2:
    print("Usage : python3 playbook/tools/import_jira.py <backlog_file>")
    print("Exemple : python3 playbook/tools/import_jira.py docs/backend/livrable/jira_backlog.py")
    sys.exit(1)
backlog_file = sys.argv[1]
print(f"📂 Backlog chargé : {backlog_file}")

load_env()
EPICS, STORIES, SUBTASKS, MODE, EXISTING_EPICS, MODULE = load_backlog(backlog_file)
print(f"⚙️  Mode : {MODE.upper()} | Module : {MODULE}")

check_registry_conflict(MODULE, MODE)

JIRA_URL    = os.environ["JIRA_URL"].rstrip("/")
JIRA_EMAIL  = os.environ["JIRA_EMAIL"]
JIRA_TOKEN  = os.environ["JIRA_TOKEN"]
PROJECT_KEY = os.environ["JIRA_PROJECT_KEY"]
AUTH        = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS     = {"Accept": "application/json", "Content-Type": "application/json"}
API         = f"{JIRA_URL}/rest/api/3"

print(f"🔗 Connexion à {JIRA_URL}...")
r = requests.get(f"{API}/myself", auth=AUTH, headers=HEADERS)
if r.status_code != 200:
    print(f"❌ Connexion échouée ({r.status_code}). Vérifie docs/backend/livrable/.env")
    sys.exit(1)
print(f"✅ Connecté en tant que : {r.json()['displayName']}")

subtask_name = get_subtask_type_name(PROJECT_KEY, AUTH, HEADERS, API)
print(f"✅ Type Sub-task détecté : '{subtask_name}'")

epic_keys  = {}
story_keys = {}

# ── 1. Epics (MODE create uniquement) ─────────────────────────────────────────
if MODE == "create":
    print(f"\n{'='*50}")
    print("📦 Création des Epics...")
    for ref, summary, description, label in EPICS:
        key = create_issue({
            "fields": {
                "project":     {"key": PROJECT_KEY},
                "summary":     summary,
                "description": adf(description),
                "issuetype":   {"name": "Epic"},
                "priority":    {"name": "Medium"},
                "labels":      [label],
            }
        }, AUTH, HEADERS, API)
        if key:
            epic_keys[ref] = key
            print(f"   ✅ {key} — {summary}")
        time.sleep(0.3)
else:
    print(f"\n{'='*50}")
    print("🔗 Rattachement aux Epics existants...")
    epic_keys = dict(EXISTING_EPICS)
    for ref, jira_id in epic_keys.items():
        print(f"   📎 {ref} → {jira_id}")

# ── 2. Stories ─────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print("📖 Création des Stories...")
for ref, summary, description, priority, label, sp, epic_ref in STORIES:
    epic_key = epic_keys.get(epic_ref)
    fields = {
        "project":     {"key": PROJECT_KEY},
        "summary":     summary,
        "description": adf(description),
        "issuetype":   {"name": "Story"},
        "priority":    {"name": priority},
        "labels":      [label],
    }
    if epic_key:
        fields["customfield_10014"] = epic_key
    key = create_issue({"fields": fields}, AUTH, HEADERS, API)
    if key:
        story_keys[ref] = key
        print(f"   ✅ {key} — {summary}")
    time.sleep(0.3)

# ── 3. Sub-tasks ───────────────────────────────────────────────────────────────
ok = 0
print(f"\n{'='*50}")
print(f"🔧 Création des Sub-tasks (type : '{subtask_name}')...")
for ref, summary, description, priority, label, story_ref in SUBTASKS:
    parent_key = story_keys.get(story_ref)
    if not parent_key:
        print(f"   ⚠️  Parent introuvable pour {ref} ({story_ref}), ignoré")
        continue
    key = create_issue({
        "fields": {
            "project":     {"key": PROJECT_KEY},
            "summary":     summary,
            "description": adf(description),
            "issuetype":   {"name": subtask_name},
            "priority":    {"name": priority},
            "labels":      [label],
            "parent":      {"key": parent_key},
        }
    }, AUTH, HEADERS, API)
    if key:
        ok += 1
        print(f"   ✅ {key} — {summary}")
    time.sleep(0.3)

# ── Résumé ─────────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"🎉 Import terminé !")
if MODE == "create":
    print(f"   Epics    : {len(epic_keys)}/{len(EPICS)}")
print(f"   Stories  : {len(story_keys)}/{len(STORIES)}")
print(f"   Sub-tasks: {ok}/{len(SUBTASKS)}")

# ── Mise à jour automatique du registre ───────────────────────────────────────
update_registry(MODULE, epic_keys, story_keys, EPICS, STORIES, SUBTASKS, MODE, backlog_file)
