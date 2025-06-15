import cv2
import os
from PIL import Image
from pdf2image import convert_from_path


class ImageProcessor:
    """Handles image processing operations for OCR."""
    
    @staticmethod
    def rotate_image(image_cv2, angle: int):
        """Rotate image by specified angle (0, 90, 180, 270)."""
        if angle == 0:
            return image_cv2
            
        rotation_map = {
            90: cv2.ROTATE_90_CLOCKWISE,
            180: cv2.ROTATE_180,
            270: cv2.ROTATE_90_COUNTERCLOCKWISE
        }
        
        if angle not in rotation_map:
            raise ValueError(f"Invalid angle: {angle}. Must be 0, 90, 180, or 270.")
            
        return cv2.rotate(image_cv2, rotation_map[angle])
    
    @staticmethod
    def upscale_image(image_cv2, scale_factor: float = 2.0):
        """Upscale image for better OCR results."""
        return cv2.resize(
            image_cv2, 
            None, 
            fx=scale_factor, 
            fy=scale_factor, 
            interpolation=cv2.INTER_CUBIC
        )
    
    @staticmethod
    def load_image_from_file(file_path: str):
        """Load image from file, handling both PDF and image formats."""
        _, ext = os.path.splitext(file_path)
        
        if ext.lower() == ".pdf":
            return ImageProcessor._load_from_pdf(file_path)
        else:
            return ImageProcessor._load_from_image(file_path)
    
    @staticmethod
    def _load_from_pdf(file_path: str):
        """Load first page from PDF as OpenCV image."""
        pages = convert_from_path(file_path, dpi=300)
        pil_image = pages[0]
        
        # Convert PIL to OpenCV format
        temp_path = "temp_image.jpg"
        pil_image.save(temp_path)
        img = cv2.imread(temp_path)
        os.remove(temp_path)
        
        return img
    
    @staticmethod
    def _load_from_image(file_path: str):
        """Load image file as OpenCV image."""
        img = cv2.imread(file_path)
        if img is None:
            raise ValueError(f"Could not load image from: {file_path}")
        return img
    
    @staticmethod
    def convert_cv2_to_pil(img_cv2):
        """Convert OpenCV image to PIL Image."""
        return Image.fromarray(cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB))
