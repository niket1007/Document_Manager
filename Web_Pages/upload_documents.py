import streamlit as st
import time

def upload_to_drive(files: list) -> bool:
    my_bar = st.progress(0, text="Initiating Upload....")
    time.sleep(10)
    my_bar.progress(100, text="Upload Complete")
    return True

with st.form("Upload Data To Drive", border=False):
    files_uploaded = st.file_uploader(label="PDF Upload", type="pdf", accept_multiple_files=True)
    is_submit = st.form_submit_button("Upload")

    if is_submit:
        if files_uploaded is not None:
            upload_to_drive(files_uploaded)   
        else:
            st.error("No file uploaded.")