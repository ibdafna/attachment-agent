"""Service for uploading files to Dropbox with category-based organization."""
from typing import Dict, Optional
import os
from pathlib import Path
import dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode

class DropboxService:
    """Service for interacting with Dropbox API."""
    
    def __init__(self, access_token: Optional[str] = None):
        """Initialize the Dropbox service with authentication."""
        self.access_token = access_token or os.getenv('DROPBOX_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("Dropbox access token is required")
        self.client = dropbox.Dropbox(self.access_token)
        self.base_folder = "/Attachments"  # Root folder for all attachments
        
    def ensure_folder_exists(self, folder_path: str) -> None:
        """Ensure that a folder exists in Dropbox, creating it if necessary."""
        try:
            self.client.files_get_metadata(folder_path)
        except ApiError as e:
            if e.error.is_path() and e.error.get_path().is_not_found():
                self.client.files_create_folder_v2(folder_path)
            else:
                raise
    
    def get_category_path(self, category: str) -> str:
        """Get the full Dropbox path for a category folder."""
        return f"{self.base_folder}/{category}"
    
    def upload_file(self, file_data: bytes, filename: str, category: str) -> Dict:
        """Upload a file to the appropriate category folder in Dropbox."""
        # Ensure the base and category folders exist
        self.ensure_folder_exists(self.base_folder)
        category_path = self.get_category_path(category)
        self.ensure_folder_exists(category_path)
        
        # Construct the full file path
        file_path = f"{category_path}/{filename}"
        
        try:
            # Upload the file with overwrite mode
            response = self.client.files_upload(
                file_data,
                file_path,
                mode=WriteMode.overwrite
            )
            
            # Create a shared link for the file
            shared_link = self.client.sharing_create_shared_link(file_path)
            
            return {
                'name': response.name,
                'path': response.path_display,
                'id': response.id,
                'shared_link': shared_link.url
            }
        except ApiError as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    def list_category_contents(self, category: str) -> list:
        """List all files in a category folder."""
        category_path = self.get_category_path(category)
        try:
            result = self.client.files_list_folder(category_path)
            return [entry for entry in result.entries]
        except ApiError as e:
            if e.error.is_path() and e.error.get_path().is_not_found():
                return []
            raise
