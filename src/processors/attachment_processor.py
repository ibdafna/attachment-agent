"""Processor for categorizing email attachments."""
from typing import Dict, Optional
import magic
import PyPDF2
from PIL import Image
import io
import re
from docx import Document

class AttachmentProcessor:
    """Processes and categorizes email attachments."""
    
    CATEGORIES = {
        'invoice': ['invoice', 'receipt', 'bill', 'statement', 'payment'],
        'photo': ['image/jpeg', 'image/png', 'image/gif'],
        'holiday': ['vacation', 'holiday', 'trip', 'travel', 'booking'],
        'document': ['application/pdf', 'application/msword', 
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    }
    
    def __init__(self):
        """Initialize the attachment processor."""
        self.mime = magic.Magic(mime=True)
    
    def detect_mime_type(self, data: bytes) -> str:
        """Detect the MIME type of the attachment."""
        return self.mime.from_buffer(data)
    
    def extract_text_from_pdf(self, data: bytes) -> Optional[str]:
        """Extract text content from a PDF file."""
        try:
            pdf_file = io.BytesIO(data)
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception:
            return None
    
    def extract_text_from_docx(self, data: bytes) -> Optional[str]:
        """Extract text content from a DOCX file."""
        try:
            doc = Document(io.BytesIO(data))
            return " ".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            print(f"Error extracting text from DOCX: {str(e)}")
            return None
    
    def analyze_image(self, data: bytes) -> Dict:
        """Analyze image metadata and content."""
        try:
            img = Image.open(io.BytesIO(data))
            return {
                'format': img.format,
                'size': img.size,
                'mode': img.mode
            }
        except Exception:
            return {}
    
    def categorize_attachment(self, attachment: Dict) -> str:
        """Categorize an attachment based on its content and type."""
        mime_type = self.detect_mime_type(attachment['data'])
        content_text = None
        
        # Check if it's an image
        if any(mime_type.startswith(photo_type) for photo_type in self.CATEGORIES['photo']):
            return 'photo'
        
        # Extract text content based on file type
        if mime_type == 'application/pdf':
            content_text = self.extract_text_from_pdf(attachment['data'])
        elif mime_type in ['application/msword', 
                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            content_text = self.extract_text_from_docx(attachment['data'])
        
        if content_text:
            # Check for invoice-related keywords
            if any(keyword in content_text.lower() for keyword in self.CATEGORIES['invoice']):
                return 'invoice'
            
            # Check for holiday-related keywords
            if any(keyword in content_text.lower() for keyword in self.CATEGORIES['holiday']):
                return 'holiday'
        
        # Default to document category if no specific category is found
        if mime_type in self.CATEGORIES['document']:
            return 'document'
        
        return 'other'
