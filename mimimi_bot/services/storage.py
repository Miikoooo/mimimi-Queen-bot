import json
import os
from typing import Any, Dict

STATE_FILE = "state.json"


def load_state() -> Dict[str, Any]:
    # Wenn Datei fehlt: Default
    if not os.path.exists(STATE_FILE):
        return {"posted_ids": []}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Falls Datei leer/kaputt/kein dict
            if not isinstance(data, dict):
                return {"posted_ids": []}
            # posted_ids sicherstellen
            if "posted_ids" not in data or not isinstance(data["posted_ids"], list):
                data["posted_ids"] = []
            return data
    except Exception:
        # Bei JSON-Fehlern etc. auf Default zurückfallen
        return {"posted_ids": []}


def save_state(state: Dict[str, Any]) -> None:
    # Minimale Validierung
    if not isinstance(state, dict):
        state = {"posted_ids": []}
    if "posted_ids" not in state or not isinstance(state["posted_ids"], list):
        state["posted_ids"] = []

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
