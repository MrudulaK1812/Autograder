import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Role Selection", layout="centered")

st.title("Select Your Role")
st.markdown("### Choose whether you're a **Student** or a **Teacher**")

# Role Selection in the center
col1, col2 = st.columns(2)
with col1:
    if st.button("Student", use_container_width=True):
        switch_page("student_dashboard")  # Navigates to student login page
with col2:
    if st.button("Teacher", use_container_width=True):
        switch_page("teacher_dashboard")  # Navigates to teacher login page
