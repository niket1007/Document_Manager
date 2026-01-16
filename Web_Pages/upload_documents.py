import streamlit as st
import tempfile
import os
from Mega.services import get_megaserivces_instance, Mega, MegaServices

def upload_files(
        service: MegaServices, session: Mega, uploaded_files: list, selected_folder_id: str):

    with st.spinner("Uploading files to google drive", show_time=True):
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            status = service.upload_pdf(
                session, 
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
    mega_service = get_megaserivces_instance()
    mega_session = None
    folders = None

    bar = st.progress(0, "Initiating mega cloud connection.")
    if st.session_state.get("mega_logged_in", False):
        mega_session = st.session_state["mega_logged_data"]
    else:
        mega_session = mega_service.get_mega_session()
        if mega_session is None:
            return
        st.session_state["mega_logged_data"] = mega_session
        st.session_state["mega_logged_in"] = True

    bar.progress(50, "Fetching folders list.")
    if "mega_folders" not in st.session_state:
        folders = mega_service.get_folders(mega_session)
        st.session_state["mega_folders"] = folders
    else:
        folders = st.session_state["mega_folders"]
    
    bar.progress(100, "Loading UI.")
    bar.empty()

    if folders is not None:
        with st.form("Upload Data To Drive", border=False):
            is_field_disabled = False
            folder_names = [folder["name"] for folder in folders]
            if folders is not None:
                if folders == []:
                    is_field_disabled=True
                files_uploaded = st.file_uploader(
                    label="PDF Upload", type="pdf", accept_multiple_files=True, disabled=is_field_disabled)
                selected_folder = st.selectbox(
                    label="Folders", options=folder_names, disabled=is_field_disabled)
                is_submit = st.form_submit_button(
                    label="Upload", disabled=is_field_disabled)
                
                if folders == []:
                    st.warning("No Folder exist, Go to Folders tab.")
                if is_submit:
                    if files_uploaded != []:
                        folder_id = None
                        for folder in folders:
                            if folder["name"] == selected_folder:
                                folder_id = folder["id"]
                                break
                        upload_files(mega_service, mega_session, files_uploaded, folder_id)
                    else:
                        st.error("No file uploaded.")

if st.session_state.get("logged_in", False):
    upload_ui()
