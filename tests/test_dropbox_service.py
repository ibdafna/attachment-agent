"""Unit tests for Dropbox service."""
import unittest
from unittest.mock import Mock, patch
from src.services.dropbox_service import DropboxService
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode

class TestDropboxService(unittest.TestCase):
    """Test cases for DropboxService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('dropbox.Dropbox'):
            self.service = DropboxService('test_token')
            self.service.client = Mock()
    
    def test_init_without_token(self):
        """Test initialization without token."""
        with self.assertRaises(ValueError):
            DropboxService(None)
    
    def test_ensure_folder_exists_already_exists(self):
        """Test ensuring folder exists when it already does."""
        folder_path = '/test_folder'
        self.service.client.files_get_metadata.return_value = {'path': folder_path}
        
        self.service.ensure_folder_exists(folder_path)
        
        self.service.client.files_get_metadata.assert_called_with(folder_path)
        self.service.client.files_create_folder_v2.assert_not_called()
    
    def test_ensure_folder_exists_create_new(self):
        """Test creating folder when it doesn't exist."""
        folder_path = '/test_folder'
        error = ApiError('test', Mock())
        error.error = Mock()
        error.error.is_path.return_value = True
        error.error.get_path.return_value = Mock()
        error.error.get_path.return_value.is_not_found.return_value = True
        
        self.service.client.files_get_metadata.side_effect = error
        
        self.service.ensure_folder_exists(folder_path)
        
        self.service.client.files_create_folder_v2.assert_called_with(folder_path)
    
    def test_get_category_path(self):
        """Test getting category path."""
        category = 'invoice'
        expected_path = f"{self.service.base_folder}/{category}"
        
        path = self.service.get_category_path(category)
        
        self.assertEqual(path, expected_path)
    
    def test_upload_file_success(self):
        """Test successful file upload."""
        file_data = b'test data'
        filename = 'test.pdf'
        category = 'invoice'
        
        mock_response = Mock()
        mock_response.name = filename
        mock_response.path_display = f'/Attachments/{category}/{filename}'
        mock_response.id = 'file123'
        
        mock_shared_link = Mock()
        mock_shared_link.url = 'https://dropbox.com/s/file123'
        
        self.service.client.files_upload.return_value = mock_response
        self.service.client.sharing_create_shared_link.return_value = mock_shared_link
        
        result = self.service.upload_file(file_data, filename, category)
        
        self.service.client.files_upload.assert_called_with(
            file_data,
            f'/Attachments/{category}/{filename}',
            mode=WriteMode.overwrite
        )
        self.assertEqual(result['name'], filename)
        self.assertEqual(result['path'], f'/Attachments/{category}/{filename}')
        self.assertEqual(result['id'], 'file123')
        self.assertEqual(result['shared_link'], 'https://dropbox.com/s/file123')
    
    def test_list_category_contents(self):
        """Test listing category contents."""
        category = 'invoice'
        mock_entries = [Mock(), Mock()]
        mock_result = Mock()
        mock_result.entries = mock_entries
        
        self.service.client.files_list_folder.return_value = mock_result
        
        result = self.service.list_category_contents(category)
        
        self.service.client.files_list_folder.assert_called_with(f'/Attachments/{category}')
        self.assertEqual(result, mock_entries)
    
    def test_list_category_contents_empty(self):
        """Test listing contents of non-existent category."""
        category = 'nonexistent'
        error = ApiError('test', Mock())
        error.error = Mock()
        error.error.is_path.return_value = True
        error.error.get_path.return_value = Mock()
        error.error.get_path.return_value.is_not_found.return_value = True
        
        self.service.client.files_list_folder.side_effect = error
        
        result = self.service.list_category_contents(category)
        
        self.assertEqual(result, [])
