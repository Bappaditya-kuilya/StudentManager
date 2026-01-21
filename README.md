# 🎓 TutorBuddy - Tuition Management System

**TutorBuddy** is a lightweight Full-Stack MVP designed for tuition teachers to manage student records, track fee payments, and generate professional PDF receipts instantly.

---

## 🚀 Features
* **Student Management**: Register students with parent details and class info.
* **Real-time Dashboard**: Track 'Collected' vs 'Pending' revenue at a glance.
* **Dynamic Search**: Instantly filter students by name.
* **PDF Receipt Generation**: Download professional receipts for paid fees.
* **Cloud Database**: Powered by Supabase for reliable data storage.

## 🛠️ Tech Stack
* **Frontend**: Streamlit
* **Backend/Database**: Supabase (PostgreSQL)
* **PDF Engine**: fpdf2
* **Environment Management**: Python `uv`

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/Bappaditya-kuilya/Studentmanager.git](https://github.com/Bappaditya-kuilya/Studentmanager.git)
   cd Studentmanager


### 🔑 Environment Setup
Since the `.env` file is ignored for security, you need to create your own:
1. Create a file named `.env` in the root folder.
2. Add the following keys (get these from your Supabase Dashboard):
   ```text
   SUPABASE_URL = "your_project_url_here"
   SUPABASE_KEY = "your_anon_key_here"