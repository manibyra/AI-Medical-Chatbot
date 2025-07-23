import json
from chatbot.data_loader import load_conditions
from chatbot.symptom_extractor import extract_symptoms
import random

# Load conditions from the dataset
conditions = load_conditions()

def match_conditions(user_symptoms):
    matched = []

    for condition in conditions:
        matched_symptoms = list(set(condition['symptoms']) & set(user_symptoms))
        total = len(condition['symptoms'])
        match_score = len(matched_symptoms) / total if total else 0

        # ✅ Accept even 1 symptom if user has entered only 1
        if (len(user_symptoms) == 1 and len(matched_symptoms) >= 1) or match_score >= 0.5:
            matched.append((condition, match_score))

    matched.sort(key=lambda x: x[1], reverse=True)
    return matched

def evaluate_confirmed_conditions(confirmed_conditions, all_conditions):
    response = []

    for condition_name, count in confirmed_conditions.items():
        condition_info = next((c for c in all_conditions if c['name'] == condition_name), None)
        if not condition_info:
            continue

        if count >= 3:
            prefix = "❗ Suspected Condition"
        elif count == 2:
            prefix = "🤔 You may have"
        else:
            continue  # Skip if only 0 or 1

        advice = {
            "condition": condition_info["name"],
            "advice": condition_info.get("advice", "Consult a doctor."),
            "medications": condition_info.get("medications", []),
            "doctor": condition_info.get("doctor", "General Physician")
        }

        response.append(
            f"{prefix}: *{advice['condition']}*\n"
            f"📋 Advice: {advice['advice']}\n"
            f"💊 Medications: {', '.join(advice['medications'])}\n"
            f"👨‍⚕️ Doctor: {advice['doctor']}"
        )

    return "\n\n".join(response) if response else "⚠️ No clear diagnosis found. Please consult a doctor."

# Utility to collect all questions for conditions containing the symptom
def collect_followup_questions(user_symptoms):
    question_bank = []
    related_conditions = []

    for cond in conditions:
        matched = any(sym.lower() in user_symptoms for sym in cond.get("symptoms", []))
        if matched:
            related_conditions.append(cond)
            for q in cond.get("questions", []):
                question_bank.append((q, cond["name"]))
    
    random.shuffle(question_bank)
    return question_bank, related_conditions

def ask_followup_questions(condition):
    questions = condition.get("questions", [])
    return random.sample(questions, min(3, len(questions)))

def get_final_advice(condition):
    raw_meds = condition.get("medicines", "No medicines listed.")
    meds = [m.strip() for m in raw_meds.split(",")] if isinstance(raw_meds, str) else raw_meds

    return {
        "condition": condition["name"],
        "advice": condition.get("advice", "No advice available."),
        "medications": meds,
        "doctor": condition.get("specialist", "General Physician")
    }
def diagnose(text_input):
    user_symptoms = extract_symptoms(text_input)

    if not user_symptoms:
        return {"error": "😕 I couldn't understand your symptoms. Please try again."}

    matched_conditions = []
    max_match_count = 0

    for condition in conditions:
        cond_symptoms = [s.lower() for s in condition.get("symptoms", [])]
        match_count = sum(1 for s in user_symptoms if s in cond_symptoms)

        if match_count > 0:
            matched_conditions.append((condition, match_count))
            max_match_count = max(max_match_count, match_count)

    # Step 1: Prioritize conditions with all symptoms matched
    primary_conditions = [c for c, m in matched_conditions if m == len(user_symptoms)]
    
    # Step 2: If no full match, get conditions with most matched symptoms
    if not primary_conditions and max_match_count > 0:
        primary_conditions = [c for c, m in matched_conditions if m == max_match_count]

    fallback_conditions = [c for c, m in matched_conditions if c not in primary_conditions]

    question_set = []
    condition_map = {}

    for condition in primary_conditions:
        for q in condition.get("questions", []):
            if q not in question_set:
                question_set.append(q)
                condition_map[q] = condition["name"]

    if not question_set:
        return {"error": "😕 I couldn't find any questions based on your symptoms. Please try rephrasing or adding more."}

    return {
        "questions": question_set,
        "map": condition_map,
        "symptoms": user_symptoms,
        "fallback_conditions": fallback_conditions
    }
