from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive.readonly"]

class GDrive:
	def __init__(self, auth)
		creds = Credentials.from_authorized_user_info('token.json', SCOPES)
		self.service = build('docs', 'v1', credentials=creds)

