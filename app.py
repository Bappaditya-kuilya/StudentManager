from fpdf import FPDF
import streamlit as st
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# --- DATABASE SETUP ---
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --- PDF GENERATOR ---
def generate_pdf(student_name, fees, student_class):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(200, 10, txt="TutorBuddy - Fee Receipt", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Student Name: {student_name}", ln=True)
    pdf.cell(200, 10, txt=f"Class: {student_class}", ln=True)
    pdf.cell(200, 10, txt=f"Amount Received: INR {fees}", ln=True)
    pdf.cell(200, 10, txt=f"Status: PAID", ln=True)
    pdf.ln(20)
    pdf.cell(200, 10, txt="Authorized Signature", ln=True, align='R')
    
    return pdf.output()

# --- STREAMLIT UI ---
st.set_page_config(page_title="TutorBuddy", layout="wide")

# Sidebar for Registration
with st.sidebar:
    st.header("Register New Student")
    name = st.text_input("Name")
    s_class = st.text_input("Class")
    monthly_fees = st.number_input("Monthly Fees", min_value=0, step=100)
    parent = st.text_input("Parent Name")
    contact = st.text_input("Contact Number")

    if st.button("Add Student"):
        if name:
            data = {
                "name": name, 
                "student_class": s_class, 
                "monthly_fees": monthly_fees, 
                "parent_name": parent,
                "contact": contact,
                "is_paid": False
            }
            supabase.table("students").insert(data).execute()
            st.success("Student added successfully!")
            st.rerun()
        else:
            st.error("Name is required!")

# Main Dashboard
st.title("TutorBuddy Dashboard")

# 🔍 Search Feature
search_query = st.text_input("Search Student by Name", value="")

# Fetch Data
response = supabase.table("students").select("*").execute()
all_students = response.data

if all_students:
    # 📊 Metrics (Always calculate on ALL students for accuracy)
    total_rev = sum(s['monthly_fees'] for s in all_students if s['is_paid'])
    pending_rev = sum(s['monthly_fees'] for s in all_students if not s['is_paid'])
    
    m1, m2 = st.columns(2)
    m1.metric("Collected Revenue", f"INR {total_rev}")
    m2.metric("Pending Revenue", f"INR {pending_rev}", delta_color="inverse")

    st.divider()

    # Apply Filter for Display
    if search_query:
        display_list = [s for s in all_students if search_query.lower() in s['name'].lower()]
    else:
        display_list = all_students

# 🔍 Apply Filter for Display
    if search_query:
        display_list = [s for s in all_students if search_query.lower() in s['name'].lower()]
    else:
        display_list = all_students

   # Display Records
    if display_list:
        for s in display_list:
            # Use an Expander for "Details"
            with st.expander(f"👤 {s['name']} - Class {s['student_class']}"):
                # Inside the expander, show all hidden details
                detail_col1, detail_col2 = st.columns(2)
                with detail_col1:
                    st.write(f"**Parent Name:** {s['parent_name']}")
                    st.write(f"**Contact Number:** {s['contact']}")
                with detail_col2:
                    st.write(f"**Address:** {s.get('address', 'N/A')}")
                    st.write(f"**Monthly Fees:** INR {s['monthly_fees']}")
                # Add this alongside your Status and Receipt buttons
                if st.button("🗑️ Delete Student", key=f"del_{s['id']}"):
                    # SQL logic to remove from database
                    supabase.table("students").delete().eq("id", s['id']).execute()
                    st.warning(f"Student {s['name']} removed.")
                    st.rerun()
                st.divider()

                # Action Buttons (Status & Receipt)
                c1, c2 = st.columns(2)
                
                # Paid/Unpaid Toggle
                status_label = "Mark as Unpaid" if s['is_paid'] else "Mark as Paid"
                if c1.button(status_label, key=f"btn_{s['id']}"):
                    supabase.table("students").update({"is_paid": not s['is_paid']}).eq("id", s['id']).execute()
                    st.rerun()
                
                # Receipt Download
                if s['is_paid']:
                    pdf_result = generate_pdf(s['name'], s['monthly_fees'], s['student_class'])
                    c2.download_button(
                        label="📄 Download Receipt",
                        data=bytes(pdf_result),
                        file_name=f"Receipt_{s['name']}.pdf",
                        mime="application/pdf",
                        key=f"dl_{s['id']}"
                    )
                else:
                    c2.write("---")

    # ⚠️ Fix for the Yellow Warning Line:
    # Only show warning if there's a search query AND no results found
    elif search_query:
        st.warning(f"No student found matching '{search_query}'")