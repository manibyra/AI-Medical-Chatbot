import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/conditions.json')

def load_conditions():
    """
    Loads conditions from the JSON file and returns as a list of dictionaries.
    """
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            conditions = json.load(file)
        return conditions
    except FileNotFoundError:
        print("conditions.json not found.")
        return []
    except json.JSONDecodeError:
        print("Invalid JSON format in conditions.json.")
        return []
