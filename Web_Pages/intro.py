import streamlit as st

def intro_ui():
    st.title("Introduction")
    st.header("App Name: Document Manager", divider=True)


if st.session_state.get("logged_in", False):
    intro_ui()