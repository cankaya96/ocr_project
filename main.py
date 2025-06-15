"""
Main execution script for OCR document processing.
Demonstrates the new modular structure usage.
"""
import os
from core import (
    setup_directories, 
    process_files_in_directory,
    DocumentProcessor
)


def main():
    """Main execution function."""
    print("🚀 Starting OCR Document Processing System")
    
    # Setup directories
    setup_directories()
    print("✅ Directories initialized")
    
    # Process files in batch
    directory_path = "Documents"
    if not os.path.exists(directory_path):
        print(f"ERROR: '{directory_path}' folder not found.")
        return
    
    print(f"📂 Processing files in: {directory_path}")
    process_files_in_directory(directory_path)


def process_single_document_example():
    """Example of processing a single document using the new structure."""
    # Initialize document processor
    processor = DocumentProcessor()
    
    # Process a single file
    file_path = "path/to/your/document.pdf"
    if os.path.exists(file_path):
        category, identifier = processor.process_document(file_path, return_id=True)
        print(f"Document classified as: {category}")
        if identifier:
            print(f"Extracted identifier: {identifier}")
    else:
        print(f"File not found: {file_path}")


if __name__ == "__main__":
    main()
