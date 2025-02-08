"""Unit tests for attachment processor."""
import unittest
from unittest.mock import Mock, patch
from src.processors.attachment_processor import AttachmentProcessor
import io

class TestAttachmentProcessor(unittest.TestCase):
    """Test cases for AttachmentProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = AttachmentProcessor()
    
    def test_detect_mime_type(self):
        """Test MIME type detection."""
        test_data = b'%PDF-1.4\n'  # PDF file header
        mime_type = self.processor.detect_mime_type(test_data)
        self.assertEqual(mime_type, 'application/pdf')
    
    @patch('PyPDF2.PdfReader')
    def test_extract_text_from_pdf(self, mock_pdf_reader):
        """Test PDF text extraction."""
        mock_page = Mock()
        mock_page.extract_text.return_value = 'Test invoice content'
        mock_pdf_reader.return_value.pages = [mock_page]
        
        text = self.processor.extract_text_from_pdf(b'fake pdf content')
        
        self.assertEqual(text, 'Test invoice content')
        mock_page.extract_text.assert_called_once()
    
    # def test_extract_text_from_docx(self):
    #     """Test DOCX text extraction."""
    #     with patch('docx.Document') as mock_document:
    #         mock_paragraph = Mock()
    #         mock_paragraph.text = 'Test holiday booking'
    #         mock_doc = Mock()
    #         mock_doc.paragraphs = [mock_paragraph]
    #         mock_document.return_value = mock_doc
    #         
    #         text = self.processor.extract_text_from_docx(b'fake docx content')
    #         
    #         self.assertEqual(text, 'Test holiday booking')
    #         mock_document.assert_called_once()
    
    def test_analyze_image(self):
        """Test image analysis."""
        with patch('PIL.Image.open') as mock_image:
            mock_image.return_value.format = 'JPEG'
            mock_image.return_value.size = (100, 100)
            mock_image.return_value.mode = 'RGB'
            
            result = self.processor.analyze_image(b'fake image data')
            
            self.assertEqual(result['format'], 'JPEG')
            self.assertEqual(result['size'], (100, 100))
            self.assertEqual(result['mode'], 'RGB')
    
    def test_categorize_attachment_photo(self):
        """Test photo categorization."""
        attachment = {'data': b'fake image data'}
        self.processor.detect_mime_type = Mock(return_value='image/jpeg')
        
        category = self.processor.categorize_attachment(attachment)
        
        self.assertEqual(category, 'photo')
    
    def test_categorize_attachment_invoice(self):
        """Test invoice categorization."""
        attachment = {'data': b'fake pdf data'}
        self.processor.detect_mime_type = Mock(return_value='application/pdf')
        self.processor.extract_text_from_pdf = Mock(return_value='Invoice #123')
        
        category = self.processor.categorize_attachment(attachment)
        
        self.assertEqual(category, 'invoice')
    
    def test_categorize_attachment_holiday(self):
        """Test holiday document categorization."""
        attachment = {'data': b'fake docx data'}
        self.processor.detect_mime_type = Mock(return_value='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.processor.extract_text_from_docx = Mock(return_value='Holiday booking confirmation')
        
        category = self.processor.categorize_attachment(attachment)
        
        self.assertEqual(category, 'holiday')
    
    def test_categorize_attachment_document(self):
        """Test default document categorization."""
        attachment = {'data': b'fake pdf data'}
        self.processor.detect_mime_type = Mock(return_value='application/pdf')
        self.processor.extract_text_from_pdf = Mock(return_value='Regular document content')
        
        category = self.processor.categorize_attachment(attachment)
        
        self.assertEqual(category, 'document')
