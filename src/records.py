import json
import os

RECORDS_FILE = "records.json"


def load_records():
    if not os.path.exists(RECORDS_FILE):
        return {"max_wave": 0, "max_score": 0}

    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        return {"max_wave": 0, "max_score": 0}


def save_records(max_wave, max_score):
    data = {"max_wave": max_wave, "max_score": max_score}
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
