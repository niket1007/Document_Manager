import streamlit as st
from Mega.services import get_megaserivces_instance, MegaServices, Mega

def delete_folder(service: MegaServices, session: Mega, index: int):
    folder_id = st.session_state["mega_folders"][index]["id"]
    status = service.delete_folder(session=session, folder_id=folder_id)
    if status:
        st.success("Deleted Successfully.")
        st.session_state["mega_folders"].pop(index)

def folders_operation_ui():
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
        if folders is None:
            return
        st.session_state["mega_folders"] = folders
    else:
        folders = st.session_state["mega_folders"]
    
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
                        on_click=lambda service=mega_service, session=mega_session, index=index: delete_folder(service, session, index))


        with tab2:
            st.subheader("Create Folders")
            with st.form("Create Folders", border=False):
                folder_name = st.text_input("Enter Folder Name")
                is_submitted = st.form_submit_button("Create")
                
                if is_submitted:
                    if folder_name in folders:
                        pass
                    folder_id = mega_service.create_folder(mega_session, folder_name=folder_name)
                    if folder_id is not None:
                        st.session_state["mega_folders"].append({
                            "id": folder_id,
                            "name": folder_name
                        })
                        st.rerun()

if st.session_state.get("logged_in", False):
    folders_operation_ui()