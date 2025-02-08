# Attachment Agent

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

### Implementation Plan

1. **Setup & Configuration**
   - Project structure setup
   - Environment configuration
   - Dependency management
   - Authentication setup for both Gmail and Dropbox

2. **Gmail Integration**
   - Implement Gmail API client
   - Setup email filtering
   - Implement attachment extraction
   - Handle various attachment types

3. **Attachment Processing**
   - Implement file type detection
   - Create categorization logic
   - Setup content analysis
   - Implement category mapping

4. **Dropbox Integration**
   - Implement Dropbox API client
   - Create folder structure management
   - Setup file upload system
   - Implement category-based organization

5. **Testing & Validation**
   - Unit tests for each component
   - Integration tests
   - End-to-end testing
   - Error handling and logging

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
