import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "settings.json")
SETTINGS_FILE = os.path.normpath(SETTINGS_FILE)

DEFAULTS = {
    "theme":            "system",
    "lang_code":        "PT",
    "alert_distance":   50,
    "refresh_interval": 60,
    "ntfy_topic":       "",
}

def load() -> dict:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                data = json.load(f)
                return {**DEFAULTS, **data}
        except Exception:
            pass
    return dict(DEFAULTS)

def save(settings: dict) -> None:
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print("[SETTINGS ERROR]", e)
