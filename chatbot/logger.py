import json
from datetime import datetime
import os

LOG_FILE = "data/user_corpus_data.json"

def log_user_input(entry):
    log_data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            try:
                log_data = json.load(file)
            except json.JSONDecodeError:
                log_data = []

    entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data.append(entry)

    with open(LOG_FILE, "w") as file:
        json.dump(log_data, file, indent=4)

