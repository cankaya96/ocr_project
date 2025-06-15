import os
import shutil
from datetime import datetime
from .config import UPLOAD_FOLDER


class FileOperations:
    """Handles file system operations."""
    
    @staticmethod
    def generate_unique_filename(code: str, folder: str, ext: str) -> str:
        """Generate a unique filename with date and counter if needed."""
        date_str = datetime.now().strftime("%d%m%Y")
        base_name = f"{code}_{date_str}"
        filename = f"{base_name}.{ext}"
        counter = 1
        
        while os.path.exists(os.path.join(folder, filename)):
            filename = f"{base_name}({counter}).{ext}"
            counter += 1
            
        return filename
    
    @staticmethod
    def ensure_directory_exists(directory_path: str):
        """Create directory if it doesn't exist."""
        os.makedirs(directory_path, exist_ok=True)
    
    @staticmethod
    def move_file_to_category(source_path: str, category: str, new_filename: str = None) -> str:
        """Move file to appropriate category folder."""
        dest_folder = os.path.join(UPLOAD_FOLDER, category)
        FileOperations.ensure_directory_exists(dest_folder)
        
        if new_filename is None:
            new_filename = os.path.basename(source_path)
        
        dest_path = os.path.join(dest_folder, new_filename)
        
        # Handle file conflicts
        if os.path.exists(dest_path):
            base_name, ext = os.path.splitext(new_filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base_name}({counter}){ext}")
                counter += 1
        
        shutil.move(source_path, dest_path)
        return dest_path
    
    @staticmethod
    def get_all_files_in_directory(directory_path: str) -> list:
        """Recursively get all files in a directory."""
        all_files = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):  # Ensure it's a file
                    all_files.append(file_path)
        return all_files
