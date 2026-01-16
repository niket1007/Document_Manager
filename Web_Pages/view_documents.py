import streamlit as st
from Mega.services import get_megaserivces_instance, Mega, MegaServices

def delete_file(service: MegaServices, session: Mega, pid: int, cid: int):
    file_id = st.session_state["mega_all_data"][pid]["children"][cid]["id"]
    status = service.delete_file(session, file_id)
    if status:
        st.success("File deleted successfully.")
        st.session_state["mega_all_data"][pid]["children"].pop(cid)

def download_file(service: MegaServices, session: Mega, pid: int, cid: int):
    parent_folder_id = st.session_state["mega_all_data"][pid]["parent"]["id"]
    child_file_id = st.session_state["mega_all_data"][pid]["children"][cid]["id"]
    status = service.download_file(session, parent_folder_id, child_file_id)
    if status:
        st.success("File downloaded successfully.")

def view_ui():
    mega_service = get_megaserivces_instance()
    mega_session = None
    folders = None
    complete_data = None

    bar = st.progress(0, "Initiating mega cloud connection.")
    if st.session_state.get("mega_logged_in", False):
        mega_session = st.session_state["mega_logged_data"]
    else:
        mega_session = mega_service.get_mega_session()
        st.session_state["mega_logged_data"] = mega_session
        st.session_state["mega_logged_in"] = True
    
    bar.progress(50, "Fetching folders list.")
    if "mega_folders" not in st.session_state:
        folders = mega_service.get_folders(mega_session)
        st.session_state["mega_folders"] = folders
    else:
        folders = st.session_state["mega_folders"]

    bar.progress(75, "Fetching files for each folder")
    if "mega_all_data" not in st.session_state:
        complete_data = mega_service.get_files_and_folders(mega_session, folders)
        st.session_state["mega_all_data"] = complete_data
    else:
        complete_data = st.session_state["mega_all_data"]
    

    bar.progress(100, "Loading UI.")
    bar.empty()

    refresh_button = st.button(label="Refresh", type='secondary')

    if refresh_button:
        del st.session_state["mega_all_data"]
        st.rerun()

    for pindex, data in enumerate(complete_data):
        expander = st.expander(data["parent"]["name"])
        if len(data["children"]) == 0:
            expander.write("No file found.")
        else:
            for cindex, child in enumerate(data["children"]):
                col1, col2, col3 = expander.columns(3)
                col1.write(child["name"])
                col2.button(
                    label="Download", 
                    key=f"Download-{child['name']}-{cindex}-{pindex}", 
                    width="stretch",
                    on_click=lambda service=mega_service, session=mega_session, pid=pindex, cid=cindex: download_file(service, session, pid, cid))
                col3.button(
                    label="Delete", 
                    key=f"Delete-{child['name']}-{cindex}-{pindex}", 
                    width="stretch",
                    on_click=lambda service=mega_service, session=mega_session, pid=pindex, cid=cindex: delete_file(service, session, pid, cid))


if st.session_state.get("logged_in", False):
    view_ui()