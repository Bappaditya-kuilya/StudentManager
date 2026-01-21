from fpdf import FPDF
import streamlit as st
import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import date

# --- 1. STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(page_title="TutorBuddy Pro", layout="wide")

# --- 2. PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Poppins', sans-serif !important;
        background-color: #050505;
        color: #E5E7EB;
    }

    .stApp {
        background: radial-gradient(circle at 20% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at 80% 80%, rgba(30, 58, 138, 0.05) 0%, transparent 40%);
    }

    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        color: #FFFFFF !important;
    }

    .stExpander {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        margin-bottom: 1rem;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        border: none;
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 14px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
        transition: 0.3s;
        width: 100%;
    }

    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.4);
    }

    [data-testid="stMetricValue"] {
        color: #34D399 !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE SETUP ---
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --- 4. PREMIUM PDF GENERATOR (Fixed Bytearray Error) ---
def generate_pdf(name, parent_name, class_name, amount, date_str):
    pdf = FPDF()
    pdf.add_page()
    
    # Emerald Header
    pdf.set_fill_color(16, 185, 129)
    pdf.rect(0, 0, 210, 40, 'F')
    
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, "TUTORBUDDY RECEIPT", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, f"Date: {date_str}", ln=True, align='C')
    
    pdf.ln(20)
    
    # Table Content
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(95, 12, "Description", border=1, fill=True)
    pdf.cell(95, 12, "Details", border=1, fill=True, ln=True)
    
    pdf.set_font("Arial", '', 11)
    rows = [
        ("Student Name", name),
        ("Parent Name", parent_name),
        ("Class", class_name),
        ("Amount Paid", f"INR {amount}")
    ]
    
    for label, val in rows:
        pdf.cell(95, 10, label, border=1)
        pdf.cell(95, 10, str(val), border=1, ln=True)
    
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Status: PAID", ln=True, align='R')
    pdf.set_draw_color(16, 185, 129)
    pdf.line(140, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Authorized Signature", align='R')
    
    return bytes(pdf.output(dest='S'))

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("Register New Student")
    reg_name = st.text_input("Name")
    reg_class = st.text_input("Class")
    reg_fees = st.number_input("Monthly Fees", min_value=0, step=100)
    reg_parent = st.text_input("Parent Name")
    reg_contact = st.text_input("Contact Number")

    if st.button("Add Student"):
        if reg_name:
            data = {
                "name": reg_name, "student_class": reg_class, 
                "monthly_fees": reg_fees, "parent_name": reg_parent,
                "contact": reg_contact, "is_paid": False
            }
            supabase.table("students").insert(data).execute()
            st.success("Student added!")
            st.rerun()
        else:
            st.error("Name is required!")

# --- 6. MAIN DASHBOARD ---
st.title("🎓 TutorBuddy Dashboard")

search_query = st.text_input("🔍 Search Student")

response = supabase.table("students").select("*").execute()
all_students = response.data

if all_students:
    # Metrics
    total_rev = sum(s['monthly_fees'] for s in all_students if s['is_paid'])
    pending_rev = sum(s['monthly_fees'] for s in all_students if not s['is_paid'])
    
    m1, m2 = st.columns(2)
    m1.metric("Collected Revenue", f"INR {total_rev}")
    m2.metric("Pending Revenue", f"INR {pending_rev}")

    st.divider()

    # Filter Logic
    display_list = [s for s in all_students if search_query.lower() in s['name'].lower()] if search_query else all_students

    # Display Loop
    for s in display_list:
        with st.expander(f"👤 {s['name']} - Class {s['student_class']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Parent:** {s.get('parent_name', 'N/A')}")
                st.write(f"**Contact:** {s.get('contact', 'N/A')}")
            with col2:
                st.write(f"**Fees:** INR {s['monthly_fees']}")
                st.write(f"**Status:** {'✅ Paid' if s['is_paid'] else '❌ Unpaid'}")

            btn_col1, btn_col2, btn_col3 = st.columns(3)
            
            # Toggle Status
            status_txt = "Mark Unpaid" if s['is_paid'] else "Mark Paid"
            if btn_col1.button(status_txt, key=f"st_{s['id']}"):
                supabase.table("students").update({"is_paid": not s['is_paid']}).eq("id", s['id']).execute()
                st.rerun()
            
            # PDF Download
            if s['is_paid']:
                today_str = date.today().strftime("%d-%m-%Y")
                pdf_bytes = generate_pdf(s['name'], s.get('parent_name', 'N/A'), s['student_class'], s['monthly_fees'], today_str)
                btn_col2.download_button(
                    label="📄 Receipt",
                    data=pdf_bytes,
                    file_name=f"Receipt_{s['name']}.pdf",
                    mime="application/pdf",
                    key=f"dl_{s['id']}"
                )
            
            # Delete
            if btn_col3.button("🗑️ Delete", key=f"del_{s['id']}"):
                supabase.table("students").delete().eq("id", s['id']).execute()
                st.rerun()
else:
    st.info("No students registered yet.")