import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set page config
st.set_page_config(page_title="AutoGrader", layout="wide")

# Title and Description
st.title("Welcome to AutoGrader")
st.markdown("### AI-Powered Answer Evaluation System")

# Ensure role selection exists in session state
if "role" not in st.session_state:
    st.session_state.role = None  # No default role, must log in first

# Centered Login Button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

if st.button("Login / Signup", use_container_width=True):
    switch_page("role_selection")  # Navigate to role selection page

st.markdown("</div>", unsafe_allow_html=True)

# Redirect only after successful login
if "logged_in" in st.session_state and st.session_state.logged_in:
    if st.session_state.role == "Student Dashboard":
        switch_page("student_dashboard")
    elif st.session_state.role == "Teacher Dashboard":
        switch_page("teacher_dashboard")