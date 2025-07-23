# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-07-22
### Added
- Initial release of the AI Medical Diagnostic Chatbot.
- Flask backend with dynamic chat-based symptom diagnosis.
- Session-based tracking of questions and conditions.
- Voice input support for user symptoms.
- Symptom-to-condition mapping using `conditions.json`.
- Real-time condition confirmation and suspicion logic.
- `requirements.txt`, `README.md`, `LICENSE`, `REPORT.md`.

### Improved
- Dynamic question skipping based on negative responses.
- Two-tier condition confirmation: "You may have" and "Suspected Condition".
- Logging of user responses for each interaction.

### Fixed
- Session handling and proper question sequencing.

---

## [1.1.0] - Upcoming
### Planned
- Multilingual support.
- Doctor suggestion with direct links.
- Secure user feedback logging.
- Admin dashboard for monitoring condition trends.
