import json
import os

# Base path to the data folder relative to this script
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_conditions():
    file_path = os.path.join("data", "conditions.json")
    if not os.path.exists(file_path):
        st.warning("⚠️ 'conditions.json' not found in /data.")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
