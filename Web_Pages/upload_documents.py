import streamlit as st
import tempfile
import os
from Web_Pages.Utility.utils import error_logging, get_gdrive_folders
from GDrive.services import get_gdrive_instance, GDriveSession

def upload_files(
        session: GDriveSession, uploaded_files: list, selected_folder_id: str):

    with st.spinner("Uploading files to google drive", show_time=True):
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            status = session.upload_pdf(
                tmp_file_path, 
                uploaded_file.name,
                selected_folder_id
            )
            os.remove(tmp_file_path)
            
            if status:
                st.success(f"{uploaded_file.name} uploaded successfully.")
            else:
                st.error(f"{uploaded_file.name} upload failed.")     

def upload_ui():

    bar = st.progress(0, "Initiating google drive connection.")
    session = get_gdrive_instance()
    if session is None:
        error_logging()
        return

    bar.progress(50, "Fetching folders list.")
    folders = get_gdrive_folders(session=session)
    if folders is None:
        return
    
    bar.progress(100, "Loading UI.")
    bar.empty()

    if folders is not None:
        with st.form("Upload Data To Drive", border=False, clear_on_submit=True):
            is_field_disabled = False
            folder_names = [folder["name"] for folder in folders]
            if folders is not None:
                if folders == []:
                    st.warning("No Folder exist, Go to Folders tab.")
                    is_field_disabled=True
                files_uploaded = st.file_uploader(
                    label="PDF Upload", type="pdf", accept_multiple_files=True, disabled=is_field_disabled)
                selected_folder = st.selectbox(
                    label="Folders", options=folder_names, disabled=is_field_disabled)
                is_submit = st.form_submit_button(
                    label="Upload", disabled=is_field_disabled)
                
                if is_submit:
                    if files_uploaded != []:
                        folder_id = None
                        for folder in folders:
                            if folder["name"] == selected_folder:
                                folder_id = folder["id"]
                                break
                        upload_files(session, files_uploaded, folder_id)

                    else:
                        st.error("No file uploaded.")

if st.session_state.get("logged_in", False):
    upload_ui()
