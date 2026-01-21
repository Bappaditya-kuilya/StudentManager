# 🎓 TutorBuddy - Tuition Management System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://studentmanager.streamlit.app/)

**TutorBuddy** is a lightweight Full-Stack MVP designed for tuition teachers to manage student records, track fee payments, and generate professional PDF receipts instantly.

---

## 🚀 Live Demo
Access the application here: [studentmanager.streamlit.app](https://studentmanager.streamlit.app/)

## ✨ Key Features
* **Student Management**: Register students with parent details and class info.
* **Real-time Dashboard**: Track 'Collected' vs 'Pending' revenue at a glance.
* **Dynamic Search**: Instantly filter students by name.
* **PDF Receipt Generation**: Download professional receipts for paid fees using `fpdf2`.
* **Cloud Database**: Powered by Supabase for reliable PostgreSQL storage.

## 🛠️ Tech Stack
* **Frontend**: Streamlit
* **Backend/Database**: Supabase (PostgreSQL)
* **Environment Management**: Python `uv`

## 📦 Local Setup
1. Clone the repo: `git clone https://github.com/Bappaditya-kuilya/StudentManager.git`
2. Install dependencies: `uv pip install -r requirements.txt`
3. Add your `.env` file with `SUPABASE_URL` and `SUPABASE_KEY`.
4. Run: `streamlit run app.py`

---
*Developed by [Bappaditya Kuilya](https://github.com/Bappaditya-kuilya)*