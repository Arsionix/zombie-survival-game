import json
import os

VOLUME = 0.7


def load_settings():
    global VOLUME
    settings_file = "settings.json"
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
                VOLUME = max(0.0, min(1.0, settings.get("volume", 0.7)))
        except (json.JSONDecodeError, KeyError):
            VOLUME = 0.7
    else:
        VOLUME = 0.7


def save_settings(volume):
    global VOLUME
    VOLUME = volume
    with open("settings.json", "w") as f:
        json.dump({"volume": volume}, f)


def get_volume():
    global VOLUME
    return VOLUME
