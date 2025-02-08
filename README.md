# attachment-agent

An automated system that processes Gmail attachments and organizes them into categorized folders in Dropbox.

## Features

- Gmail Integration
  - Reads emails from Gmail account
  - Filters for emails with attachments
  - Supports common attachment types (PDF, images, documents, etc.)

- Attachment Processing
  - Extracts attachments from emails
  - Reads attachment content
  - Categorizes attachments based on content and type
  - Categories include: invoices, photos, holidays, and more

- Dropbox Integration
  - Automatically uploads processed attachments
  - Creates category-based folder structure
  - Organizes files by their identified categories

## Technical Architecture

### Components

1. **Gmail Service**
   - Uses Gmail API for email access
   - Handles OAuth2 authentication
   - Filters emails with attachments
   - Downloads attachments

2. **Attachment Processor**
   - Supports multiple file types:
     - Documents (PDF, DOC, DOCX)
     - Images (JPG, PNG, GIF)
     - Spreadsheets (XLS, XLSX)
     - Other common formats
   - Implements content analysis for categorization
   - Uses machine learning/AI for intelligent categorization

3. **Dropbox Service**
   - Handles Dropbox API integration
   - Manages folder structure creation
   - Handles file uploads
   - Maintains category-based organization

## Dependencies

- Python 3.12+
- Required Python packages:
  - google-api-python-client (Gmail API)
  - dropbox (Dropbox API)
  - python-magic (File type detection)
  - PyPDF2 (PDF processing)
  - Pillow (Image processing)
  - python-docx (Word document processing)
  - pytest (Testing)

## Setup Instructions

[To be added after initial implementation]

## Usage

[To be added after initial implementation]

## Development

[To be added after initial implementation]
