import streamlit as st
from Web_Pages.Utility.utils import error_logging

def intro_ui():
    st.title("Introduction")
    st.header("App Name: Document Manager", divider=True)


if st.session_state.get("logged_in", False):
    intro_ui()