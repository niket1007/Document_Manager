import streamlit as st
from GDrive.services import GDriveSession
import time

def error_logging():
    with st.spinner("Logging out user, facing some issue", show_time=True):
        time.sleep(2)        
        st.session_state.clear()
        st.cache_resource.clear()
        st.logout()

def get_gdrive_folders(session: GDriveSession):
    folders = None
    if "gdrive_folders" not in st.session_state:
        folders = session.get_folders()
        if folders is None:
            return
        st.session_state["gdrive_folders"] = folders
    else:
        folders = st.session_state["gdrive_folders"]
    return folders