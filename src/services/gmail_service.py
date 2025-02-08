"""Gmail service for reading emails and extracting attachments."""
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
import os
import pickle

class GmailService:
    """Service for interacting with Gmail API."""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, credentials_path: str = 'credentials.json', token_path: str = 'token.pickle'):
        """Initialize the Gmail service with authentication."""
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.service = None
        
    def authenticate(self) -> None:
        """Authenticate with Gmail API."""
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('gmail', 'v1', credentials=self.creds)
    
    def list_messages_with_attachments(self, max_results: int = 100) -> List[Dict]:
        """List messages that have attachments."""
        if not self.service:
            self.authenticate()
            
        results = self.service.users().messages().list(
            userId='me',
            maxResults=max_results,
            q='has:attachment'
        ).execute()
        
        return results.get('messages', [])
    
    def get_message_details(self, message_id: str) -> Dict:
        """Get detailed information about a specific message."""
        if not self.service:
            self.authenticate()
            
        return self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
    
    def get_attachment(self, message_id: str, attachment_id: str) -> Optional[bytes]:
        """Download a specific attachment from a message."""
        if not self.service:
            self.authenticate()
            
        attachment = self.service.users().messages().attachments().get(
            userId='me',
            messageId=message_id,
            id=attachment_id
        ).execute()
        
        if attachment:
            return base64.urlsafe_b64decode(attachment['data'])
        return None
    
    def process_message_attachments(self, message_id: str) -> List[Dict]:
        """Process all attachments in a message."""
        message = self.get_message_details(message_id)
        attachments = []
        
        if 'payload' not in message:
            return attachments
            
        parts = [message['payload']]
        while parts:
            part = parts.pop()
            
            if 'parts' in part:
                parts.extend(part['parts'])
                
            if 'body' in part and 'attachmentId' in part['body']:
                attachment_data = self.get_attachment(
                    message_id,
                    part['body']['attachmentId']
                )
                
                if attachment_data:
                    attachments.append({
                        'filename': part.get('filename', 'unknown'),
                        'mimeType': part.get('mimeType', 'application/octet-stream'),
                        'data': attachment_data
                    })
                    
        return attachments
