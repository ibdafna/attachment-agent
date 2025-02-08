"""Unit tests for Gmail service."""
import unittest
from unittest.mock import Mock, patch, MagicMock
from src.services.gmail_service import GmailService
import base64
import os

class TestGmailService(unittest.TestCase):
    """Test cases for GmailService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = GmailService('test_credentials.json', 'test_token.pickle')
        self.service.service = Mock()  # Mock the Gmail API service
    
    @patch('src.services.gmail_service.InstalledAppFlow')
    @patch('src.services.gmail_service.build')
    @patch('builtins.open')
    @patch('os.path.exists')
    def test_authenticate_new_credentials(self, mock_exists, mock_open, mock_build, mock_flow):
        """Test authentication with new credentials."""
        mock_exists.return_value = False
        mock_flow_instance = Mock()
        mock_flow.from_client_secrets_file.return_value = mock_flow_instance
        mock_flow_instance.run_local_server.return_value = Mock()
        
        self.service.authenticate()
        
        mock_flow.from_client_secrets_file.assert_called_once()
        mock_flow_instance.run_local_server.assert_called_once()
        mock_build.assert_called_once_with('gmail', 'v1', credentials=mock_flow_instance.run_local_server.return_value)
    
    def test_list_messages_with_attachments(self):
        """Test listing messages with attachments."""
        mock_response = {'messages': [{'id': '123', 'threadId': 'thread123'}]}
        self.service.service.users().messages().list().execute.return_value = mock_response
        
        messages = self.service.list_messages_with_attachments(max_results=1)
        
        self.assertEqual(messages, mock_response['messages'])
        self.service.service.users().messages().list.assert_called_with(
            userId='me',
            maxResults=1,
            q='has:attachment'
        )
    
    def test_get_message_details(self):
        """Test getting message details."""
        mock_message = {'id': '123', 'payload': {'parts': []}}
        self.service.service.users().messages().get().execute.return_value = mock_message
        
        message = self.service.get_message_details('123')
        
        self.assertEqual(message, mock_message)
        self.service.service.users().messages().get.assert_called_with(
            userId='me',
            id='123',
            format='full'
        )
    
    def test_get_attachment(self):
        """Test getting attachment data."""
        mock_attachment = {'data': base64.urlsafe_b64encode(b'test data')}
        self.service.service.users().messages().attachments().get().execute.return_value = mock_attachment
        
        attachment_data = self.service.get_attachment('123', 'att123')
        
        self.assertEqual(attachment_data, b'test data')
        self.service.service.users().messages().attachments().get.assert_called_with(
            userId='me',
            messageId='123',
            id='att123'
        )
    
    def test_process_message_attachments(self):
        """Test processing message attachments."""
        mock_message = {
            'payload': {
                'parts': [{
                    'filename': 'test.pdf',
                    'mimeType': 'application/pdf',
                    'body': {'attachmentId': 'att123'}
                }]
            }
        }
        mock_attachment_data = b'test data'
        
        self.service.get_message_details = Mock(return_value=mock_message)
        self.service.get_attachment = Mock(return_value=mock_attachment_data)
        
        attachments = self.service.process_message_attachments('123')
        
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0]['filename'], 'test.pdf')
        self.assertEqual(attachments[0]['mimeType'], 'application/pdf')
        self.assertEqual(attachments[0]['data'], mock_attachment_data)
