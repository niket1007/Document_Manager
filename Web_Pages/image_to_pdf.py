import streamlit as st
from uuid import uuid4
import img2pdf

def validate_fields(upload_files: list, pdf_file_name: str) -> bool:
    errors = ""
    if pdf_file_name is None or pdf_file_name.strip() == "":
        errors += "File Name"
    if len(upload_files) <= 0:
        errors += ", Upload File"
    
    if errors != "":
        st.error(f"Error: {errors}")
        return False
    return True

uploaded_data = st.file_uploader(label="Upload images", 
                        type=["jpeg, png, JPEG, PNG", "JPG", "jpg"],
                        accept_multiple_files=True)

pdf_file_name = st.text_input("PDF File Name")

if len(uploaded_data) > 0:
    exp = st.expander("Preview Image")
    for img in uploaded_data:
        exp.image(image=img,width=300)

col1, col2 = st.columns(2)

is_submit = col1.button(label="Convert To PDF", width="stretch")

if is_submit:
    if validate_fields(uploaded_data, pdf_file_name):
        images = []
        for img in uploaded_data:
            images.append(img.getvalue())
        pdf = img2pdf.convert(images)

        col2.download_button(
            label="Download PDF",
            data=pdf,
            file_name=pdf_file_name + ".pdf",
            mime="pdf",
            icon=":material/download:",
            width="stretch"
        )

