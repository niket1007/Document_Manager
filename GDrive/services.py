import streamlit as st
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from typing import Any

class GDriveSession:
    def __init__(self):
        self.service = self.get_drive_session()
        self.parent_folder_id = st.secrets["gdrive"]["parent_folder_id"]
    
    def get_drive_session(self) -> Any:
        try:
            tokens = st.user.tokens
            print(st.user.to_dict())
            if tokens is None:
                raise Exception("Login invalid")

            creds = Credentials(
                token=tokens.get("access"),
                refresh_token=tokens.get("refresh_token"),
                token_uri=st.secrets.get("auth")["google"]["token_uri"],
                client_id=st.secrets.get("auth")["google"]["client_id"],
                client_secret=st.secrets.get("auth")["google"]["client_secret"]
            )
            return build('drive', 'v3', credentials=creds)
        except Exception as e:
            st.error(f"Error while connecting to drive: {(str(e))}")
            return None

    def get_folders(self) -> list|None:
        try:
            query = f"'{self.parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            results = self.service.files().list(
                q=query, 
                fields="files(id, name)",
                spaces="drive").execute()
            return results.get('files', [])
        except Exception as e:
            st.error(f"Error while fetching folders: {str(e)}")
            return None
    
    def get_files_and_folders(self, folders: list) -> list|None:
        try:
            complete_data = []
            for folder in folders:
                f_id = folder["id"]
                query = f"'{f_id}' in parents and trashed = false"
                temp = []
                results = self.service.files().list(
                    q=query,
                    fields="files(id, name, webViewLink)",
                    spaces='drive').execute()
                files = results.get('files', [])
                for file in files:
                    temp.append({
                        "id": file["id"],
                        "name": file["name"],
                        "preview_link": file["webViewLink"]
                    })
                complete_data.append(
                    {
                        "parent": {"id": folder["id"], "name": folder["name"]},
                        "children": temp
                    }
                )
            return complete_data
        except Exception as e:
            st.error(f"Error while fetching folders: {str(e)}")
            return None

    def create_folder(self, folder_name: str) -> str|None:
        try:
            metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.parent_folder_id]
            }
            folder = self.service.files().create(body=metadata, fields='id').execute()
            return folder.get('id')
        except Exception as e:
            st.error(f"Error while creating folder: {str(e)}")
            return None
    
    def delete_folder_or_file(self, folder_id: str) -> bool:
        try:
            self.service.files().delete(fileId=folder_id).execute()
            return True
        except Exception as e:
            st.error(f"Error while deleting the file: {str(e)}")
            return False

    def upload_pdf(self, file_path: str, name: str, folder_id: str):
        try:
            metadata = {'name': name, 'parents': [folder_id]}
            media = MediaFileUpload(
                file_path, 
                mimetype='application/pdf', 
                resumable=True)
            
            self.service.files().create(
                body=metadata, 
                media_body=media, 
                fields='id').execute()
            return True
        except Exception as e:
            st.error(f"Error while uploading pdf: {str(e)}")
            return False

@st.cache_resource
def get_gdrive_instance():
    instance = GDriveSession()
    return instance