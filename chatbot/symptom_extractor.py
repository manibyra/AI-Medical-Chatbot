import json
import os
import re

def extract_symptoms(text_input):
    
    file_path = os.path.join("data", "conditions.json")  

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        conditions = json.load(f)

    keywords = set()
    for condition in conditions:
        for symptom in condition.get("symptoms", []):
            keywords.add(symptom.lower())

    found = []
    text_input = text_input.lower()

    for word in keywords:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text_input):
            found.append(word)

    return found
