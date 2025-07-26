import streamlit as st
from chatbot.data_loader import load_conditions
from chatbot.symptom_extractor import extract_symptoms
from chatbot.diagnosis import format_diagnosis, evaluate_confirmed_conditions, save_log
from chatbot.translator import translate_text
import os
import random
import time

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

langs = {
    "English": "en",
    "हिन्दी (Hindi)": "hi",
    "తెలుగు (Telugu)": "te",
    "தமிழ் (Tamil)": "ta",
    "ಕನ್ನಡ (Kannada)": "kn",
    "বাংলা (Bengali)": "bn"
}

selected_language = st.selectbox("Choose your language:", list(langs.keys()))
lang_code = langs[selected_language]
st.session_state.lang = lang_code

conditions = load_conditions()
st.set_page_config(page_title="🧠 AI Medical Diagnosis Assistant", layout="centered")
st.title(translate_text("🦠 AI Medical Diagnosis Assistant", src="en", dest=lang_code))

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
    st.session_state.user_data = {"name": "", "age": 0, "gender": ""}

if not st.session_state.chat_started:
    with st.form("user_info_form"):
        st.session_state.user_data["name"] = st.text_input(translate_text("Enter your name:", src="en", dest=lang_code))
        st.session_state.user_data["age"] = st.number_input(translate_text("Enter your age:", src="en", dest=lang_code), min_value=1, max_value=120, step=1)
        st.session_state.user_data["gender"] = st.selectbox(
            translate_text("Select your gender:", src="en", dest=lang_code), ["Male", "Female", "Other"]
        )
        submitted = st.form_submit_button(translate_text("Start Chat", src="en", dest=lang_code))

    if submitted:
        if st.session_state.user_data["name"] and st.session_state.user_data["age"] and st.session_state.user_data["gender"]:
            st.session_state.chat_started = True
            st.rerun()
        else:
            st.warning(translate_text("⚠️ Please fill in all fields to proceed.", src="en", dest=lang_code))

if st.session_state.chat_started:
    if "qa_log" not in st.session_state:
        st.session_state.qa_log = []
    if "chat" not in st.session_state:
        st.session_state.chat = []
        st.session_state.phase = "symptom_input"
        st.session_state.questions = []
        st.session_state.condition_map = {}
        st.session_state.conditions = []
        st.session_state.confirmed = {}
        st.session_state.negatives = {}
        st.session_state.follow_up = 0

    for entry in st.session_state.chat:
        with st.chat_message(entry["role"]):
            st.markdown(entry["message"])

    user_input = st.chat_input(translate_text("Enter your symptoms", src="en", dest=lang_code))
    if user_input:
        translated_input = translate_text(user_input, src=lang_code, dest='en')

        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat.append({"role": "user", "message": user_input})

        if st.session_state.phase == "symptom_input":
            symptoms = extract_symptoms(translated_input)
            if not symptoms:
                reply = "😕 I couldn't understand your symptoms. Please try again."
            else:
                st.session_state.symptoms = symptoms
                all_match = [cond for cond in conditions if all(sym in [s.lower() for s in cond.get("symptoms", [])] for sym in symptoms)]
                matches = all_match or [cond for cond in conditions if any(sym in [s.lower() for s in cond.get("symptoms", [])] for sym in symptoms)]

                if not matches:
                    reply = "😕 No relevant conditions found for your symptoms."
                else:
                    question_set = []
                    condition_map = {}
                    for cond in matches:
                        for q in cond.get("questions", []):
                            if q not in question_set:
                                question_set.append(q)
                                condition_map[q] = cond["name"]

                    if not question_set:
                        reply = "😕 No questions found for matched conditions."
                    else:
                        random.shuffle(question_set)
                        st.session_state.questions = question_set
                        st.session_state.condition_map = condition_map
                        st.session_state.conditions = matches
                        st.session_state.phase = "followup"
                        st.session_state.follow_up = 0
                        st.session_state.confirmed = {}
                        st.session_state.negatives = {}
                        reply = f"🧐 {question_set[0]} (yes/no)"

            translated_msg = translate_text(reply, src='en', dest=lang_code)
            st.chat_message("assistant").markdown(translated_msg)
            st.session_state.chat.append({"role": "assistant", "message": translated_msg})
            st.stop()

        elif st.session_state.phase == "followup":
            answer = user_input.strip().lower()
            yes_no_map = {
                "yes": "yes", "no": "no",
                "అవును": "yes", "లేదు": "no",
                "हाँ": "yes", "नहीं": "no",
                "हां": "yes", "नहीं": "no",
                "ஆம்": "yes", "இல்லை": "no",
                "ಹೌದು": "yes", "ಇಲ್ಲ": "no",
                "হ্যাঁ": "yes", "না": "no"
            }
            mapped_answer = yes_no_map.get(answer)

            if mapped_answer not in ["yes", "no"]:
                msg = "❗ Please answer with 'yes' or 'no'."
                translated_msg = translate_text(msg, src='en', dest=lang_code)
                st.chat_message("assistant").markdown(translated_msg)
                st.session_state.chat.append({"role": "assistant", "message": translated_msg})
                st.stop()

            current_question = st.session_state.questions[st.session_state.follow_up]
            condition_name = st.session_state.condition_map.get(current_question, "")
            st.session_state.qa_log.append({"question": current_question, "answer": mapped_answer})

            if mapped_answer == "yes":
                st.session_state.confirmed[condition_name] = st.session_state.confirmed.get(condition_name, 0) + 1
            else:
                st.session_state.negatives[condition_name] = st.session_state.negatives.get(condition_name, 0) + 1

            if st.session_state.confirmed.get(condition_name, 0) >= 3:
                condition = next((c for c in st.session_state.conditions if c["name"] == condition_name), None)
                if condition:
                    diagnosis = format_diagnosis(condition)
                    translated_diagnosis = translate_text(diagnosis, src='en', dest=lang_code)
                    st.chat_message("assistant").markdown(translated_diagnosis)
                    st.session_state.chat.append({"role": "assistant", "message": translated_diagnosis})
                    st.session_state.phase = "done"
                    try:
                        save_log(diagnosis)
                    except Exception as e:
                        st.warning(f"Log save failed: {e}")
                    st.stop()

            while True:
                st.session_state.follow_up += 1
                if st.session_state.follow_up >= len(st.session_state.questions):
                    break
                next_q = st.session_state.questions[st.session_state.follow_up]
                next_cond = st.session_state.condition_map.get(next_q, "")
                if st.session_state.negatives.get(next_cond, 0) < 2:
                    break

            if st.session_state.follow_up < len(st.session_state.questions):
                next_q = st.session_state.questions[st.session_state.follow_up]
                bot_msg = f"🧐 {next_q} (yes/no)"
                translated_bot_msg = translate_text(bot_msg, src='en', dest=lang_code)
                st.chat_message("assistant").markdown(translated_bot_msg)
                st.session_state.chat.append({"role": "assistant", "message": translated_bot_msg})
            else:
                diagnosis_text = evaluate_confirmed_conditions(
                    st.session_state.confirmed, st.session_state.conditions
                )
                translated_diagnosis = translate_text(diagnosis_text, src='en', dest=lang_code)
                st.chat_message("assistant").markdown(translated_diagnosis)
                st.session_state.chat.append({"role": "assistant", "message": translated_diagnosis})
                st.session_state.phase = "done"
                try:
                    save_log(diagnosis_text)
                except Exception as e:
                    st.warning(f"Log save failed: {e}")
                st.stop()
