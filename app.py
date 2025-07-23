from flask import Flask, render_template, request, jsonify, session
from chatbot.diagnosis import diagnose, evaluate_confirmed_conditions
from chatbot.data_loader import load_conditions
from chatbot.logger import log_user_input

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    session.clear()
    session['stage'] = 'ask_name'
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input'].strip()

    if 'stage' not in session:
        session['stage'] = 'ask_name'

    if session['stage'] == 'ask_name':
        if len(user_input.split()) > 3:
            return jsonify({"reply": "❗ That seems like symptoms. Please tell me just your name first 😊"})

        session['user_name'] = user_input
        session['stage'] = 'ask_symptom'
        return jsonify({"reply": f"👋 Hello *{user_input}*! What symptoms are you experiencing today?"})

    if session['stage'] == 'ask_symptom':
        result = diagnose(user_input)
        session['qa_log'] = [] 

        if 'error' in result:
            return jsonify({"reply": result['error']})
        

        if 'symptoms' in result:
            log_user_input({
                "name": session.get('user_name', 'Unknown'),
                "symptoms": result['symptoms']
            })

        session['questions'] = result.get('questions', [])
        session['condition_map'] = result.get('map', {})
        session['fallback_conditions'] = result.get('fallback_conditions', [])
        session['fallback_stage'] = False
        session['confirmed'] = {}
        session['index'] = 0

        if not session['questions']:
            return jsonify({"reply": "😕 I couldn't find any questions based on your symptoms. Please try rephrasing or adding more."})

        session['stage'] = 'followup'
        return jsonify({"reply": f"❓ {session['questions'][0]}"})

    if session['stage'] == 'followup':
        answer = user_input.lower()
        question_index = session.get('index', 0)
        current_question = session['questions'][question_index]
        condition_name = session['condition_map'].get(current_question)

        if answer in ['yes', 'y']:
            session['confirmed'][condition_name] = session['confirmed'].get(condition_name, 0) + 1

        session['index'] += 1

        if session['index'] < len(session['questions']):
            next_question = session['questions'][session['index']]
            return jsonify({"reply": f"❓ {next_question}"})
        else:
            confirmed = session.get('confirmed', {})
            all_conditions = load_conditions()
            response_text = evaluate_confirmed_conditions(confirmed, all_conditions)
            session.clear()
            return jsonify({"reply": response_text})

    return jsonify({"reply": "❓ I'm not sure what you mean. Please try again."})

@app.route('/followup', methods=['POST'])
def followup():
    user_input = request.form['user_input'].strip().lower()

    questions = session.get('questions', [])
    index = session.get('index', 0)
    confirmed = session.get('confirmed', {})
    condition_map = session.get('condition_map', {})
    user_name = session.get('user_name', 'Unknown')
    negatives = session.get('negatives', {})
    filtered_conditions = session.get('filtered_conditions', [])

    if index >= len(questions):
        session.clear()
        return jsonify({"reply": "❗ Session expired or completed. Please restart."})

    current_question = questions[index]
    related_condition = condition_map.get(current_question)

    # Log the user response
    log_user_input({
        "name": user_name,
        "question": current_question,
        "answer": user_input
    })
    session.setdefault("qa_log", []).append({
        "question": current_question,
        "user_answer": user_input
    })

    # Track responses
    if related_condition:
        if user_input in ['yes', 'y', 'yeah', 'yep']:
            confirmed[related_condition] = confirmed.get(related_condition, 0) + 1
        elif user_input in ['no', 'n', 'nope', 'nah']:
            negatives[related_condition] = negatives.get(related_condition, 0) + 1

    session['confirmed'] = confirmed
    session['negatives'] = negatives   

    index += 1
    session['index'] = index

    # Move to next valid question (based on filtered_conditions)
    while index < len(questions):
        next_question = questions[index]
        next_condition = condition_map.get(next_question)

        # ✅ Skip if 2 negative responses already given
        if negatives.get(next_condition, 0) >= 2:
            index += 1
            continue

        if not filtered_conditions or next_condition in filtered_conditions:
            session['index'] = index

            # 🔍 Check if any condition has 2 or 3+ confirmations
            for condition, count in confirmed.items():
                if count >= 3:
                    return jsonify({"reply": f"🧠 *Suspected Condition: {condition}*\n❓ {next_question}"})
                elif count == 2:
                    return jsonify({"reply": f"🩺 *You may have: {condition}*\n❓ {next_question}"})

            return jsonify({"reply": f"❓ {next_question}"})

        index += 1

    # If all questions are done, evaluate
    all_conditions = load_conditions()
    response_text = evaluate_confirmed_conditions(confirmed, all_conditions)
    entry = {
        "name": session.get("user_name", "Unknown"),
        "symptoms": session.get("symptoms", []),
        "qa": session.get("qa_log", []),
        "diagnosis": response_text
    }
    log_user_input(entry)
    
    session.clear()
    return jsonify({"reply": response_text})

@app.route("/answer_followup", methods=["POST"])
def answer_followup():
    user_answer = request.form["user_input"].strip().lower()
    question_idx = session.get("current_question_index", 0)
    questions = session.get("followup_questions", [])
    condition_map = session.get("condition_map", {})
    answers = session.get("followup_answers", {})

    if question_idx >= len(questions):
        return jsonify({"reply": "✅ Follow-up complete. Please wait for diagnosis..."})

    current_question = questions[question_idx]
    condition = condition_map.get(current_question)

    if condition:
        if condition not in answers:
            answers[condition] = 0
        if user_answer in ["yes", "y", "yeah", "yep"]:
            answers[condition] += 1

    session["followup_answers"] = answers
    session["current_question_index"] = question_idx + 1

    if question_idx + 1 < len(questions):
        next_question = questions[question_idx + 1]
        return jsonify({"reply": f"🤔 {next_question}"})
    else:
        all_conditions = load_conditions()
        response_text = evaluate_confirmed_conditions(answers, all_conditions)
        session.clear()
        return jsonify({"reply": response_text})

if __name__ == '__main__':
    app.run(debug=True)
