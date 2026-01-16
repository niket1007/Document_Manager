import streamlit as st

user_data = st.user.to_dict()

if user_data.get("is_logged_in", False) and user_data.get("email") in st.secrets["emails"]["allowlist"]:
    st.session_state["logged_in"] = True
    st_pages ={
        "Introduction": [st.Page(page="Web_Pages/intro.py", title="Intro")],
        "Utility": [st.Page(page="Web_Pages/image_to_pdf.py", title="Image to PDF")],
        "Document Manager": [
            st.Page("Web_Pages/folders_operation.py", title="Folders"),
            st.Page("Web_Pages/upload_documents.py", title="Upload"),
            st.Page("Web_Pages/view_documents.py", title="View")
        ]
    }
    nav = st.navigation(pages=st_pages)
    nav.run()

if user_data.get("is_logged_in", False) and user_data.get("email") not in st.secrets["emails"]["allowlist"]:
    st.sidebar.write("Unallowed user. Reach out to admin.")

if not st.user.is_logged_in:
    st.header("Document Manager")
    is_login_clicked = st.sidebar.button("Login With Google")
    if is_login_clicked:
        st.login()
else:
    is_logout_clicked = st.sidebar.button("Log out")
    if is_logout_clicked:
        st.session_state["logged_in"] = False
        st.logout()


