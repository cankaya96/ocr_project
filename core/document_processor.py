import os
from .image_processor import ImageProcessor
from .ocr_engine import OCREngine
from .classifiers import DocumentClassifier
from .validators import DocumentIdentifier
from .file_operations import FileOperations


class DocumentProcessor:
    """Main document processing class that orchestrates the entire workflow."""
    
    def __init__(self):
        """Initialize document processor with all required components."""
        self.ocr_engine = OCREngine()
        self.classifier = DocumentClassifier()
        self.image_processor = ImageProcessor()
    
    def process_document(self, file_path: str, return_id: bool = False):
        """
        Process a document file to extract category and identifier.
        
        Args:
            file_path: Path to the document file
            return_id: Whether to return extracted TC/VKN identifier
            
        Returns:
            tuple: (category, identifier) if return_id=True, else category only
        """
        try:
            # Load image from file
            img = self.image_processor.load_image_from_file(file_path)
            
            # Try OCR with different rotations
            category, identifier = self._try_ocr_with_rotations(img)
            
            # If initial OCR failed, try with upscaled image
            if category == 'others':
                print("Initial OCR failed, retrying with upscaled image...")
                category, identifier = self._try_ocr_with_upscaling(img)
                if category != 'others':
                    print("Success: classified with upscaled image.")
            
            return (category, identifier) if return_id else category
            
        except Exception as e:
            print(f"Error processing document {file_path}: {str(e)}")
            return ('others', None) if return_id else 'others'
    
    def _try_ocr_with_rotations(self, img):
        """Try OCR with different image rotations."""
        angles = [0, 90, 180, 270]
        
        for angle in angles:
            try:
                rotated = self.image_processor.rotate_image(img, angle)
                text = self.ocr_engine.extract_text_from_image(rotated)
                
                if text.strip():
                    identifier = DocumentIdentifier.extract_identifier(text)
                    category = self.classifier.classify_text(text)
                    
                    if category != 'others':
                        return category, identifier
                        
            except Exception:
                continue
        
        return 'others', None
    
    def _try_ocr_with_upscaling(self, img):
        """Try OCR with upscaled image."""
        try:
            upscaled_img = self.image_processor.upscale_image(img)
            return self._try_ocr_with_rotations(upscaled_img)
        except Exception:
            return 'others', None
    
    def process_single_file(self, file_path: str, idx: int, total: int) -> tuple:
        """
        Process a single file and move it to appropriate category folder.
        
        Returns:
            tuple: (category, original_filename)
        """
        file_name = os.path.basename(file_path)
        file_root, file_ext = os.path.splitext(file_name)
        
        try:
            # Get document category and identifier
            category, detected_id = self.process_document(file_path, return_id=True)
            
            # Generate new filename if identifier found
            if detected_id:
                new_filename = FileOperations.generate_unique_filename(
                    detected_id, 
                    os.path.join("uploads", category),
                    file_ext[1:]  # Remove the dot
                )
                print(f"[{idx}/{total}] {file_name} → {category} (NEW NAME: {new_filename})")
            else:
                new_filename = file_name
                print(f"[{idx}/{total}] {file_name} → {category}")
            
            # Move file to category folder
            FileOperations.move_file_to_category(file_path, category, new_filename)
            return category, file_name
            
        except Exception as e:
            # Handle error files
            error_category = "error_files"
            FileOperations.move_file_to_category(file_path, error_category, file_name)
            print(f"[{idx}/{total}] {file_name} → {error_category} ❌ {str(e)[:50]}")
            return error_category, file_name
