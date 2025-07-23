---
title: AI Medical Diagnostic Chatbot
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# 🧠 AI Medical Diagnostic Chatbot

This is a Flask-based AI-powered Medical Diagnostic Chatbot that dynamically interacts with users, gathers symptom details, and suggests possible conditions based on a rule-based symptom matching system.

## 🚀 Features

- 🧾 Multi-turn symptom collection and questioning
- 🤖 Dynamic question generation
- ✅ Smart condition detection (Suspected / Possible)
- 📁 Session tracking and input logging
- 🗣️ Voice input support (planned)
- 🧑‍⚕️ Suggested condition with basic medicine/doctors (planned)
- 🎨 User-friendly frontend

## 🛠️ Technologies Used

- Python 3.12+
- Flask
- HTML/CSS/JavaScript
- JSON (for condition and question rules)
- Hugging Face Spaces (deployment)

## 📂 Project Structure

```plaintext
├── app.py                 # Main Flask application
├── templates/
│   └── index.html         # Chat frontend
├── static/
│   ├── css/
│   └── js/
├── data/
│   └── conditions.json    # Symptom-condition mapping
├── logs/
│   └── user_logs.csv      # Logs of each user interaction
├── requirements.txt
├── Dockerfile
├── .huggingface.yml
├── README.md
├── REPORT.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE

Diagnosis Rules:
✅ If a condition gets 3 “yes” responses from the user → immediately confirm diagnosis and stop.
❗ If a condition gets 2 “yes” responses and no other conditions have that many → suspect that condition and show it.
⚠️ If no condition has 2 or more “yes” → show a fallback message like “No clear diagnosis found, consult a doctor.”

📦 Deployment
Deployed on Hugging Face Spaces using Docker and .huggingface.yml.

📃 License
This project is licensed under the MIT License. See LICENSE for more information.
