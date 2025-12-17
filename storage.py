import json
import os

HIGHLIGHTS_FILE = "highlights.json"

def load_highlights():
    if not os.path.exists(HIGHLIGHTS_FILE):
        return {}

    with open(HIGHLIGHTS_FILE, "r") as f:
        return json.load(f)

def save_highlights(highlights):
    with open(HIGHLIGHTS_FILE, "w") as f:
        json.dump(highlights, f, indent=2)

def delete_highlight(highlights, track_id):
    if track_id in highlights:
        del highlights[track_id]
        save_highlights(highlights)
        return True
    return False
