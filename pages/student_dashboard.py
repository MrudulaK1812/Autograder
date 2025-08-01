import streamlit as st
import pymongo
from pymongo import MongoClient
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import bcrypt

# ---------------- Load Environment Variables ----------------
load_dotenv()
MONGO_URI = os.getenv("STUDENT_DB_URI")

# ---------------- MongoDB Connection ----------------
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["student"]
student_collection = db["student_metadata"]
scores_collection = db["student_scores"]

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="Student Dashboard", page_icon="🎓", layout="wide")

# ---------------- Helper Functions ----------------
def normalize_prn(prn_input):
    return prn_input.strip().upper()

# ---------------- Session Init ----------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "student_name" not in st.session_state:
    st.session_state["student_name"] = ""
if "prn" not in st.session_state:
    st.session_state["prn"] = ""

# ---------------- Sidebar Navigation ----------------
with st.sidebar:
    selected = option_menu(
        menu_title="Student Dashboard",
        options=["🔑 Login/Signup", "📊 View Results", "💬 View Feedback"],
        icons=["key", "bar-chart", "chat-left-text"],
        default_index=0,
    )

# ---------------- Login/Signup Page ----------------
if selected == "🔑 Login/Signup":
    st.title("🎓 Student Login/Signup")
    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Signup"])

    # --- Signup ---
    with tab2:
        st.subheader("Create a Student Account")
        student_name = st.text_input("Full Name", key="signup_name")
        prn = normalize_prn(st.text_input("PRN (Student ID)", key="signup_prn"))
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")

        if st.button("Sign Up"):
            if not (student_name and prn and password and confirm_password):
                st.error("❌ All fields are required.")
            elif password != confirm_password:
                st.error("❌ Passwords do not match.")
            elif student_collection.find_one({"prn": prn}):
                st.error("❌ PRN already exists. Please login.")
            else:
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                student_data = {
                    "student_name": student_name,
                    "prn": prn,
                    "password": hashed_password
                }
                student_collection.insert_one(student_data)
                st.success("✅ Signup successful! Please login.")

    # --- Login ---
    with tab1:
        st.subheader("Student Login")
        login_prn = normalize_prn(st.text_input("PRN (Student ID)", key="login_prn"))
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            student = student_collection.find_one({"prn": login_prn})
            if student and bcrypt.checkpw(login_password.encode(), student["password"].encode()):
                st.session_state["authenticated"] = True
                st.session_state["student_name"] = student["student_name"]
                st.session_state["prn"] = student["prn"]
                st.success(f"✅ Welcome, {student['student_name']}! Login successful.")
            else:
                st.error("❌ Invalid PRN or Password.")

    # --- Logged In Message ---
    if st.session_state["authenticated"]:
        st.subheader(f"👋 Welcome, {st.session_state['student_name']}!")
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.session_state["student_name"] = ""
            st.session_state["prn"] = ""
            st.success("✅ Logged out successfully.")

# ---------------- View Results ----------------
elif selected == "📊 View Results":
    st.title("📊 View Test Results")

    if not st.session_state.get("authenticated"):
        st.error("❌ Please log in to view results.")
        st.stop()

    prn = normalize_prn(st.session_state["prn"])
    st.write("🧪 Logged-in PRN:", prn)

    results = list(scores_collection.find({"prn": {"$regex": f"^{prn}$", "$options": "i"}}))

    if results:
        for result in results:
            st.subheader(f"📝 Test ID: {result.get('test_id', 'N/A')}")
            st.markdown(f"**Student Name:** {result.get('student_name', 'N/A')}")
            st.markdown(f"**Total Marks:** {result.get('total_marks', 0)} / {result.get('max_marks', 0)}")
            for question in result.get("results", []):
                st.markdown(f"**Question:** {question.get('question', '')}")
                st.markdown(f"**Score:** {question.get('score', '')}/5")
                st.markdown(f"**Feedback:** {question.get('evaluation', '')}")
                st.markdown("---")
    else:
        st.info("ℹ️ No test results found.")

# ---------------- View Feedback ----------------
elif selected == "💬 View Feedback":
    st.title("💬 View Feedback")

    if not st.session_state.get("authenticated"):
        st.error("❌ Please log in to view feedback.")
        st.stop()

    prn = normalize_prn(st.session_state["prn"])
    st.write("🧪 Logged-in PRN:", prn)

    feedbacks = list(scores_collection.find({"prn": {"$regex": f"^{prn}$", "$options": "i"}}))

    if feedbacks:
        for feedback in feedbacks:
            st.subheader(f"📝 Test ID: {feedback.get('test_id', 'N/A')}")
            for question in feedback.get("results", []):
                st.markdown(f"*Question:* {question.get('question', '')}")
                st.markdown(f"*Feedback:* {question.get('evaluation', '')}")
                st.markdown("---")
    else:
        st.info("ℹ️ No feedback found.")
