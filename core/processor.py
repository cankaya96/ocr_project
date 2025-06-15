import os
from .config import UPLOAD_FOLDER, CATEGORY_FOLDERS
from .utils import normalize_filename, print_results
from .file_operations import FileOperations
from .document_processor import DocumentProcessor

def process_single_file(file_path, idx, total):
    """Process a single file and return the result."""
    file_name = normalize_filename(os.path.basename(file_path))
    
    # Initialize document processor
    doc_processor = DocumentProcessor()
    
    # Process the file
    category, original_filename = doc_processor.process_single_file(file_path, idx, total)
    
    return category, original_filename

def process_files_in_directory(directory_path):
    """Process all files in the given directory."""
    results = []
    folder_counts = {folder: 0 for folder in CATEGORY_FOLDERS}

    all_files = FileOperations.get_all_files_in_directory(directory_path)
    total = len(all_files)

    for idx, file_path in enumerate(all_files, start=1):
        category, file_name = process_single_file(file_path, idx, total)
        folder_counts[category] += 1
        results.append((file_name, category))

    print_results(folder_counts)
    return results
