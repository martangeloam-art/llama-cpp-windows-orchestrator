import json
import os

CONFIGS_FILE = "saved_configs.json"


def read_configs():
    if not os.path.exists(CONFIGS_FILE):
        return {}
    try:
        with open(CONFIGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def write_configs(data):
    with open(CONFIGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
