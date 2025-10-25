from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tkinter import messagebox
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = '1mMNlsaeyxfV5t2y4VfnS4QDYxBZcNmoT'

class API_Service:
    def __init__(self):
        self.creds = None

        self.load_saved_token()
        self.check_credentials()
        self.api_connect()

    def load_saved_token(self):
        if os.path.exists('token.pkl'):
            with open('token.pkl', 'rb') as token:
                self.creds = pickle.load(token)

    def check_credentials(self):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials/user_credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save credentials for next time
            with open('token.pkl', 'wb') as token:
                pickle.dump(self.creds, token)
    
    def api_connect(self):
        self.service = build('drive', 'v3', credentials=self.creds)

    def upload_file(self, input_file):
        file_path = input_file
        file_name = os.path.basename(file_path)

        file_metadata = {
            'name': file_name,
            'parents': [FOLDER_ID]
        }

        file_metadata['mimeType'] = 'application/vnd.google-apps.spreadsheet'
        media = MediaFileUpload(file_path, mimetype='text/csv')

        self.service.files().create(
            body = file_metadata,
            media_body = media,
            fields = 'id, name, mimeType'
        ).execute()

        messagebox.showinfo("Info", "Upload Complete!")

MyAPIService = API_Service()