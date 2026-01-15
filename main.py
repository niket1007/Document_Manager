import streamlit as st

pages = st.secrets.get("config", {}).get("pages", [])
st_pages = []
for page in pages:
    page_path = f"Web_Pages/{page}"
    title = page.replace(".py", "").replace("_", " ").capitalize()
    st_pages.append(
        st.Page(page=page_path,
                title=title)
    )

nav = st.navigation(pages=st_pages)
nav.run()