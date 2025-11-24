import json
from pathlib import Path

def load_json(file_path):
    if Path(file_path).exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
