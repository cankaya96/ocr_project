import pytesseract
from .image_processor import ImageProcessor


class OCREngine:
    """Handles OCR text extraction from images."""
    
    def __init__(self, language: str = 'tur', config: str = '--oem 3 --psm 6'):
        """Initialize OCR engine with configuration."""
        self.language = language
        self.config = config
    
    def extract_text_from_image(self, img_cv2) -> str:
        """Extract text from OpenCV image using Tesseract OCR."""
        pil_img = ImageProcessor.convert_cv2_to_pil(img_cv2)
        text = pytesseract.image_to_string(
            pil_img, 
            config=self.config, 
            lang=self.language
        )
        return text.lower()
    
    def extract_text_with_rotation(self, img_cv2) -> str:
        """Try OCR with different rotations to find best result."""
        angles = [0, 90, 180, 270]
        
        for angle in angles:
            try:
                rotated = ImageProcessor.rotate_image(img_cv2, angle)
                text = self.extract_text_from_image(rotated)
                # Return first successful extraction
                if text.strip():
                    return text
            except Exception:
                continue
        
        return ""
    
    def extract_text_with_upscaling(self, img_cv2) -> str:
        """Try OCR with upscaled image for better accuracy."""
        upscaled_img = ImageProcessor.upscale_image(img_cv2)
        return self.extract_text_with_rotation(upscaled_img)
