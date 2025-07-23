---
title: AI Medical Diagnostic Chatbot – viswam.ai Report
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# 🧠 AI Medical Diagnostic Chatbot – viswam.ai Open-Source Challenge Report

## 👁️‍🗨️ Project Overview

The **AI Medical Diagnostic Chatbot** is a lightweight, AI-assisted web application built using Flask. It interacts with users in a conversational format, collects symptoms, dynamically asks relevant follow-up questions, and suggests potential medical conditions using a rule-based matching approach.

Designed for **low-bandwidth environments**, this chatbot emphasizes **accessibility, speed, and simplicity**, aligning perfectly with viswam.ai's mission of enabling open-source AI for real-life societal benefit.

---

## 👥 Teammates

- **Developers**: [Byra Manikanta Prasad, Gorile Shailaja,Pooja Kumari, Akhil Budige, Leela Nayan K.P, ]
- **Mentorship/Support**: viswam.ai Open-Source Community

---

## 🎯 Project Goals

- ✅ Support natural symptom input (typed or spoken)
- ✅ Dynamically guide users through medical questioning
- ✅ Suggest suspected conditions based on logic-based matching
- ✅ Deploy in low-resource environments with minimal dependencies
- ✅ Collect anonymized symptom data for future AI training

---

## 🔧 Technical Architecture

- **Frontend**: HTML + JavaScript chat interface
- **Backend**: Flask (Python 3.12+)
- **Symptom Mapping**: JSON-based rule set (`conditions.json`)
- **Logging**: User interactions saved to `logs/user_logs.csv`
- **Deployment**: Docker container on Hugging Face Spaces

---

## 🧠 Diagnostic Logic Flow

1. Prompt user for name and symptoms.
2. Tokenize input and match symptoms against a ruleset.
3. Ask related follow-up questions for matched conditions.
4. Apply condition detection rules:
   - ✅ **Suspected Condition** if ≥3 matched symptoms
   - ❓ **Possible Condition** if exactly 2 matched symptoms
   - ⚠️ **Fallback**: "No clear diagnosis" if <2 matches
5. Display final suggestion with basic explanation.

---

## 🌍 Accessibility & Local Impact

- 💡 **Lightweight** (<100MB RAM)
- 🕓 **Fast response time** (~100ms per interaction)
- 🧏 **Voice input** ready (via browser mic or `SpeechRecognition`)
- 🌐 Future plans for **Telugu / Hindi translation support**
- 📲 Easy to deploy in rural health camps, telemedicine kiosks, or mobile apps

---

## 📊 Evaluation Metrics

| Metric                      | Value            |
|----------------------------|------------------|
| Diagnosis accuracy (manual)| ~90% (known cases)|
| Avg. questions per session | 4–5              |
| Memory footprint           | <100MB           |
| Response latency           | ~100ms           |

---

## 🧭 Future Roadmap

- 🗣️ Voice-to-text integration using Whisper or Google Speech API
- 🧑‍⚕️ Doctor & clinic recommendations with links
- 🧠 OpenAI / LLM integration for fuzzy symptom inference
- 🔁 User feedback loop for model refinement

---

## 📍 Submission Details

- **Challenge**: viswam.ai 4-week Open Source AI Challenge
- **Domain**: Healthcare / Medical AI
- **App**: Flask Web Application
- **Deployed on**: Hugging Face Spaces using Docker
- **GitHub Repo**: [https://github.com/your-username/ai-medical-chatbot](https://github.com/your-username/ai-medical-chatbot)

---

_This project aims to bridge the healthcare gap with AI-driven first-level diagnostics, empowering users even in low-connectivity and underserved regions._

> “Accessible healthcare is not a luxury — it's a right. AI should help us get there.”

