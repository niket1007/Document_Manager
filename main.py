import streamlit as st

ALLOWED_EMAIL = st.secrets["emails"]["allowlist"]

if st.user.is_logged_in:

    if st.user.email in ALLOWED_EMAIL:
        st.session_state["logged_in"] = True
        
        st_pages = {
            "Introduction": [st.Page(page="Web_Pages/intro.py", title="Intro")],
            "Utility": [st.Page(page="Web_Pages/image_to_pdf.py", title="Image to PDF")],
            "Document Manager": [
                st.Page("Web_Pages/Document_Manager/folders_operation.py", title="Folders"),
                st.Page("Web_Pages/Document_Manager/upload_documents.py", title="Upload"),
                st.Page("Web_Pages/Document_Manager/view_documents.py", title="View")
            ],
            "Admin Panels": [
                st.Page("Web_Pages/Admin_Panel/admin.py", title="Admin"),
            ]
        }
        nav = st.navigation(pages=st_pages)
        nav.run()
        
    else:
        st.sidebar.error("Access Denied: You are not authorized.")
        st.write(f"Logged in as: {st.user.email}")
    
    if st.sidebar.button("Log out"):
        st.logout()
else:
    st.header("Document Manager")
    st.info("Please login to continue")
    if st.sidebar.button("Login With Google"):
        st.login("google")