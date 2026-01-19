import streamlit as st
from Web_Pages.Utility.utils import error_logging, get_gdrive_folders
from GDrive.services import get_gdrive_instance, GDriveSession

def delete_file(session: GDriveSession, pid: int, cid: int):
    file_id = st.session_state["gdrive_all_data"][pid]["children"][cid]["id"]
    status = session.delete_folder_or_file(file_id)
    if status:
        st.success("File deleted successfully.")
        st.session_state["gdrive_all_data"][pid]["children"].pop(cid)

def refresh_page():
    del st.session_state["gdrive_all_data"]

def view_ui():
    bar = st.progress(0, "Initiating google drive connection.")
    session = get_gdrive_instance()
    if session is None:
        error_logging()
        return

    bar.progress(50, "Fetching folders list.")
    folders = get_gdrive_folders(session=session)
    if folders is None:
        return

    bar.progress(75, "Fetching files for each folder")
    if "gdrive_all_data" not in st.session_state:
        complete_data = session.get_files_and_folders(folders)
        if complete_data is None:
            return
        st.session_state["gdrive_all_data"] = complete_data
    else:
        complete_data = st.session_state["gdrive_all_data"]

    bar.progress(100, "Loading UI.")
    bar.empty()
    
    st.button(
        label="Refresh", 
        type='secondary',
        on_click=refresh_page())

    for pindex, data in enumerate(complete_data):
        expander = st.expander(data["parent"]["name"])
        if len(data["children"]) == 0:
            expander.write("No file found.")
        else:
            for cindex, child in enumerate(data["children"]):
                col1, col2, col3, col4 = expander.columns(4)
                col1.write(child["name"])
                
                col2.link_button("Preview", child["preview_link"], use_container_width=True)
                
                col3.button(
                    label="Download",
                    key=f"Download-{child['name']}-{cindex}-{pindex}",
                    width="stretch"
                )

                col4.button(
                    label="Delete", 
                    key=f"Delete-{child['name']}-{cindex}-{pindex}", 
                    width="stretch",
                    on_click=lambda session=session, pid=pindex, cid=cindex: delete_file(session, pid, cid))

                expander.divider(width="stretch")
       
if st.session_state.get("logged_in", False):
    view_ui()