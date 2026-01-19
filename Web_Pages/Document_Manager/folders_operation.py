import streamlit as st
from GDrive.services import get_gdrive_instance, GDriveSession
from Web_Pages.Utility.utils import error_logging, get_gdrive_folders

def delete_folder(session: GDriveSession, index: int) -> None:
    with st.spinner("Deleting the folder"):
        folder_id = st.session_state["gdrive_folders"][index]["id"]
        status = session.delete_folder_or_file(folder_id=folder_id)
    if status:
        st.success("Deleted Successfully.")
        st.session_state["gdrive_folders"].pop(index)

def create_folder(session: GDriveSession, name: str) -> None:
    with st.spinner("Creating the folder"):
        folders = st.session_state["gdrive_folders"]
        for folder in folders:
            if folder["name"] == name:
                st.error("Similar name folder already exists.")
                return
        folder_id = session.create_folder(folder_name=name)
    
    if folder_id is not None:
        st.success("File created successfully.")
        st.session_state["gdrive_folders"].append({
            "id": folder_id,
            "name": name
        })

def folders_operation_ui():
    folders = None

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
        tab1, tab2 = st.tabs(["View/Delete", "Create"])

        with tab1:
            st.subheader("View/Delete Folders")
            if len(folders) == 0:
                st.write("No Folder Created.")
            else:
                for index, folder in enumerate(folders):
                    col1, col2 = st.columns(2)
                    col1.write(f"{index+1}. {folder['name']}")
                    col2.button(
                        label="Delete", 
                        key=index , 
                        on_click=lambda session=session, index=index : delete_folder(session, index))

        with tab2:
            st.subheader("Create Folders")
            folder_name = st.text_input("Enter Folder Name")
            st.button(
                label="Create",
                on_click=lambda session=session, fol_name=folder_name : create_folder(session, fol_name))

if st.session_state.get("logged_in", False):
    folders_operation_ui()