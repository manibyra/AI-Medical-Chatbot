import json
import re

with open("data/conditions.json", "r", encoding="utf-8") as f:
    conditions = json.load(f)

keywords = set()
for condition in conditions:
    for symptom in condition.get("symptoms", []):
        keywords.add(symptom.lower())

def extract_symptoms(text_input):
    text_input = text_input.lower()
    found = []
    for word in keywords:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text_input):
            found.append(word)
    return found
