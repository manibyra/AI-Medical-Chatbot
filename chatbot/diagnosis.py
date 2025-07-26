import json
import os
import random
import csv
from datetime import datetime
from chatbot.data_loader import load_conditions
from chatbot.symptom_extractor import extract_symptoms
import streamlit as st

# Load from JSON once at the top
conditions = load_conditions()

def format_diagnosis(condition):
    meds = condition.get("medicines", "None listed.")
    meds_list = [m.strip() for m in meds.split(",")] if isinstance(meds, str) else meds

    return f"""✅ Based on your answers, you might have:

**{condition['name']}**  
📋 {condition.get('advice', 'No advice available.')}  
💊 **Medicines:** {', '.join(meds_list)}  
👨‍⚕️ **Doctor:** {condition.get('specialist', 'General Physician')}

📝 Please consult a healthcare professional for confirmation."""

def match_conditions(user_symptoms):
    matched = []
    for condition in conditions:
        cond_symptoms = [s.lower() for s in condition.get("symptoms", [])]
        matched_symptoms = list(set(cond_symptoms) & set(user_symptoms))
        score = len(matched_symptoms) / len(cond_symptoms) if cond_symptoms else 0

        if (len(user_symptoms) == 1 and matched_symptoms) or score >= 0.5:
            matched.append((condition, score))

    matched.sort(key=lambda x: x[1], reverse=True)
    return [c for c, _ in matched[:1]]  # Return top match only

def get_followup_questions(condition, n=3):
    questions = condition.get("questions", [])
    return random.sample(questions, min(n, len(questions)))

def evaluate_condition(user_answers):
    return user_answers.count("yes") >= 2  # 2 or more yes = confirmed

def format_final_diagnosis(condition):
    meds = condition.get("medicines", "None listed.")
    meds_list = [m.strip() for m in meds.split(",")] if isinstance(meds, str) else meds
    return f"""✅ Based on your answers, you might have:

**{condition['name']}**  
📋 {condition.get('advice', 'No advice available.')}  
💊 **Medicines:** {', '.join(meds_list)}  
👨‍⚕️ **Doctor:** {condition.get('specialist', 'General Physician')}

📝 Please consult a healthcare professional for confirmation."""

def evaluate_confirmed_conditions(confirmed_conditions, all_conditions):
    """
    Returns a diagnosis summary based on confirmed symptoms.
    """
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

        meds = condition_info.get("medicines", [])
        if isinstance(meds, str):
            meds = [m.strip() for m in meds.split(",")]

        response.append(
            f"{prefix}: *{condition_info['name']}*\n"
            f"📋 Advice: {condition_info.get('advice', 'Consult a doctor.')}\n"
            f"💊 Medications: {', '.join(meds)}\n"
            f"👨‍⚕️ Doctor: {condition_info.get('specialist', 'General Physician')}"
        )

    return "\n\n".join(response) if response else "⚠️ No clear diagnosis found. Please consult a doctor."

def save_log(diagnosis_text):
    log_file = "logs/user_logs.csv"
    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.isfile(log_file)

    try:
        with open(log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "Timestamp",
                    "Name",
                    "Age",
                    "Gender",
                    "Symptoms",
                    "Q&A Log",
                    "Diagnosis"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                st.session_state.user_data.get("name", "N/A"),
                st.session_state.user_data.get("age", "N/A"),
                st.session_state.user_data.get("gender", "N/A"),
                ", ".join(st.session_state.get("symptoms", [])),
                "; ".join([f"{q['question']} = {q['answer']}" for q in st.session_state.get("qa_log", [])]),
                diagnosis_text
            ])
    except PermissionError as e:
        st.error(f"Permission denied when saving logs. Error: {e}")
    except Exception as e:
        st.error(f"Unexpected error while saving logs: {e}")
