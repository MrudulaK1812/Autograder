# 🎓 AutoGrader – Intelligent Assessment & Feedback System

AutoGrader is a full-stack AI-powered evaluation tool built for academic institutions. It provides separate dashboards for "teachers" and "students", streamlining test creation, automated result evaluation, and feedback delivery.

---
Key Features

👩‍🏫 Teacher Dashboard
- Create tests with questions and associated keyword-based evaluation criteria.
- Upload scanned student answer sheets (PDFs).
- Answers are automatically evaluated using OCR and AI-based matching logic.
- View evaluation reports and download scores with keyword-based highlights.

### 👨‍🎓 Student Dashboard
- Log in using PRN or credentials to access the portal.
- View attempted tests and check detailed scores.
- Get feedback based on missed or matched keywords and scoring logic.

## 🛠️ Tech Stack

- Frontend: Streamlit (Python)
- Backend: Python, PyMuPDF, Mistral AI (for OCR & scoring)
- Database: MongoDB (for storing tests, answers, users, scores)
- Auth: Simple login/signup (username/PRN-based)
- Deployment: "https://autograder.streamlit.app/"

