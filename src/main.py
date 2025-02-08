"""Main entry point for the attachment agent."""
import os
import sys
import logging
from dotenv import load_dotenv
from services.gmail_service import GmailService
from services.dropbox_service import DropboxService
from processors.attachment_processor import AttachmentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_credentials():
    """Verify all required credentials are present."""
    if not os.path.exists('.env'):
        logger.error('Missing .env file. Copy .env.example to .env and configure it.')
        sys.exit(1)
    
    if not os.getenv('DROPBOX_ACCESS_TOKEN'):
        logger.error('Missing DROPBOX_ACCESS_TOKEN in .env file')
        sys.exit(1)
    
    credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
    if not os.path.exists(credentials_path):
        logger.error(f'Missing Gmail credentials file: {credentials_path}')
        sys.exit(1)

def main():
    """Run the attachment agent."""
    # Load and verify credentials
    load_dotenv()
    check_credentials()
    
    try:
        # Initialize services
        gmail = GmailService(
            os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json'),
            os.getenv('GMAIL_TOKEN_PATH', 'token.pickle')
        )
        dropbox = DropboxService()
        processor = AttachmentProcessor()
        
        # Authenticate Gmail
        gmail.authenticate()
        
        # Process emails with attachments
        messages = gmail.list_messages_with_attachments()
        logger.info(f'Found {len(messages)} messages with attachments')
        
        for message in messages:
            try:
                attachments = gmail.process_message_attachments(message['id'])
                for attachment in attachments:
                    category = processor.categorize_attachment(attachment)
                    dropbox.upload_file(
                        file_data=attachment['data'],
                        filename=attachment['filename'],
                        category=category
                    )
                    logger.info(f"Processed {attachment['filename']} as {category}")
            except Exception as e:
                logger.error(f"Error processing message {message['id']}: {str(e)}")
                continue
    
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
