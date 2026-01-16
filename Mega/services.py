import streamlit as st
from mega import Mega

class MegaServices:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance    
    
    def __init__(self):
        self.mega = Mega()
        self.parent_folder_id = st.secrets["mega"]["parent_folder_id"]

    def get_mega_session(self) -> Mega|None:
        try:
            m = self.mega.login(
                email=st.secrets["mega"]["login_email"],
                password=st.secrets["mega"]["login_password"]
            )
            return m
        except Exception as e:
            st.error(f"Error while logging in: {str(e)}")
            return None
    
    def get_folders(self, session: Mega) -> list[dict[str, str]]|None:
        try:

            files = session.get_files_in_node(self.parent_folder_id)
            folders = []
            for id in files:
                file = files[id]
                if file["t"] == 1:
                    folders.append({
                        "id": file["h"],
                        "name": file["a"]["n"]
                    })
            return folders
        except Exception as e:
            st.error(f"Error while fetching folders: {str(e)}")
            return None
        
    def delete_folder(self, session: Mega, folder_id: str) -> bool:
        try:
            session.delete(folder_id)
            return True
        except Exception as e:
            st.error(f"Error while deleting the folder: {str(e)}")
            return False
    
    def get_files_and_folders(self, session: Mega, folders: list) -> list:
        complete_data = []
        for folder in folders:
            temp = []
            files = session.get_files_in_node(folder["id"])
            for file in files:
                temp.append({
                    "id": files[file]["h"],
                    "name": files[file]["a"]["n"]
                })
            complete_data.append(
                {
                    "parent": {"id": folder["id"], "name": folder["name"]},
                    "children": temp
                }
            )
        return complete_data
    
    def create_folder(self, session: Mega, folder_name: str) -> str|None:
        try:
            created_data = session.create_folder(
                name=folder_name,
                dest=self.parent_folder_id
            )

            id = created_data[folder_name]
            return id
        except Exception as e:
            st.error(f"Error while creating folder: {str(e)}")
            return None
    
    def upload_pdf(self, session: Mega, path: str, name: str, folder_id: str) -> bool:
        try:
            session.upload(path, folder_id, name)
            return True
        except Exception as e:
            st.error(f"Error while uploading pdf: {str(e)}")
            return False
    
    def delete_file(self, session: Mega, folder_id: str) -> bool:
        try:
            session.delete(folder_id)
            return True
        except Exception as e:
            st.error(f"Error while deleting the file: {str(e)}")
            return False

    def get_download_link(seld, session: Mega, parent_folder_id: str ,child_file_id: str) -> str|None:
        try:
            files = session.get_files_in_node(parent_folder_id)
            if child_file_id not in files:
                raise Exception("File does not exist.")
            link = session.get_link((child_file_id, files[child_file_id]))
            return link
        except Exception as e:
            st.error(f"Error while downloading the file: {str(e)}")
            return None

    def get_user_data(self, session: Mega):
        return session.get_storage_space()

@st.cache_resource
def get_megaserivces_instance():
    mega_instance = MegaServices()
    return mega_instance