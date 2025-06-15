# API Reference

## 📚 Complete API Documentation

This guide provides detailed API documentation for all classes and methods in the OCR system.

## Core Modules

### DocumentProcessor

**Location**: `core/document_processor.py`

Main orchestrator class that coordinates the entire document processing workflow.

#### Class: `DocumentProcessor`

```python
class DocumentProcessor:
    def __init__(self):
        """Initialize document processor with all required components."""
```

##### Methods

**`process_document(file_path: str, return_id: bool = False)`**
```python
def process_document(self, file_path: str, return_id: bool = False):
    """
    Process a document file to extract category and identifier.
    
    Args:
        file_path (str): Path to the document file
        return_id (bool): Whether to return extracted TC/VKN identifier
        
    Returns:
        tuple: (category, identifier) if return_id=True, else category only
        
    Raises:
        Exception: If document processing fails
    """
```

**Example Usage**:
```python
from core import DocumentProcessor

processor = DocumentProcessor()

# Get category only
category = processor.process_document("invoice.pdf")

# Get category and identifier
category, identifier = processor.process_document("invoice.pdf", return_id=True)
```

**`process_single_file(file_path: str, idx: int, total: int)`**
```python
def process_single_file(self, file_path: str, idx: int, total: int) -> tuple:
    """
    Process a single file and move it to appropriate category folder.
    
    Args:
        file_path (str): Path to the file to process
        idx (int): Current file index for progress tracking
        total (int): Total number of files being processed
        
    Returns:
        tuple: (category, original_filename)
    """
```

---

### ImageProcessor

**Location**: `core/image_processor.py`

Handles all image manipulation operations for OCR processing.

#### Class: `ImageProcessor`

##### Static Methods

**`load_image_from_file(file_path: str)`**
```python
@staticmethod
def load_image_from_file(file_path: str):
    """
    Load image from file, handling both PDF and image formats.
    
    Args:
        file_path (str): Path to the image or PDF file
        
    Returns:
        numpy.ndarray: OpenCV image array
        
    Raises:
        ValueError: If file cannot be loaded
    """
```

**`rotate_image(image_cv2, angle: int)`**
```python
@staticmethod
def rotate_image(image_cv2, angle: int):
    """
    Rotate image by specified angle.
    
    Args:
        image_cv2: OpenCV image array
        angle (int): Rotation angle (0, 90, 180, 270)
        
    Returns:
        numpy.ndarray: Rotated image
        
    Raises:
        ValueError: If angle is not valid
    """
```

**`upscale_image(image_cv2, scale_factor: float = 2.0)`**
```python
@staticmethod
def upscale_image(image_cv2, scale_factor: float = 2.0):
    """
    Upscale image for better OCR results.
    
    Args:
        image_cv2: OpenCV image array
        scale_factor (float): Scaling factor (default: 2.0)
        
    Returns:
        numpy.ndarray: Upscaled image
    """
```

**`convert_cv2_to_pil(img_cv2)`**
```python
@staticmethod
def convert_cv2_to_pil(img_cv2):
    """
    Convert OpenCV image to PIL Image.
    
    Args:
        img_cv2: OpenCV image array
        
    Returns:
        PIL.Image: PIL Image object
    """
```

**Example Usage**:
```python
from core import ImageProcessor

# Load image
img = ImageProcessor.load_image_from_file("document.pdf")

# Rotate image
rotated = ImageProcessor.rotate_image(img, 90)

# Upscale image
upscaled = ImageProcessor.upscale_image(img, scale_factor=2.5)

# Convert to PIL
pil_img = ImageProcessor.convert_cv2_to_pil(img)
```

---

### OCREngine

**Location**: `core/ocr_engine.py`

Handles OCR text extraction from images using Tesseract.

#### Class: `OCREngine`

```python
class OCREngine:
    def __init__(self, language: str = 'tur', config: str = '--oem 3 --psm 6'):
        """
        Initialize OCR engine with configuration.
        
        Args:
            language (str): Tesseract language code (default: 'tur')
            config (str): Tesseract configuration string
        """
```

##### Methods

**`extract_text_from_image(img_cv2) -> str`**
```python
def extract_text_from_image(self, img_cv2) -> str:
    """
    Extract text from OpenCV image using Tesseract OCR.
    
    Args:
        img_cv2: OpenCV image array
        
    Returns:
        str: Extracted text in lowercase
    """
```

**`extract_text_with_rotation(img_cv2) -> str`**
```python
def extract_text_with_rotation(self, img_cv2) -> str:
    """
    Try OCR with different rotations to find best result.
    
    Args:
        img_cv2: OpenCV image array
        
    Returns:
        str: Extracted text from first successful rotation
    """
```

**`extract_text_with_upscaling(img_cv2) -> str`**
```python
def extract_text_with_upscaling(self, img_cv2) -> str:
    """
    Try OCR with upscaled image for better accuracy.
    
    Args:
        img_cv2: OpenCV image array
        
    Returns:
        str: Extracted text from upscaled image
    """
```

**Example Usage**:
```python
from core import OCREngine, ImageProcessor

# Initialize OCR engine
ocr = OCREngine(language='tur+eng', config='--oem 1 --psm 6')

# Load image
img = ImageProcessor.load_image_from_file("document.pdf")

# Extract text
text = ocr.extract_text_from_image(img)

# Extract with rotation fallback
text = ocr.extract_text_with_rotation(img)

# Extract with upscaling
text = ocr.extract_text_with_upscaling(img)
```

---

### DocumentClassifier

**Location**: `core/classifiers.py`

Classifies documents based on extracted text content.

#### Class: `DocumentClassifier`

```python
class DocumentClassifier:
    def __init__(self, categories: dict = None):
        """
        Initialize classifier with categories.
        
        Args:
            categories (dict): Custom categories dictionary (optional)
        """
```

##### Methods

**`classify_text(text: str) -> str`**
```python
def classify_text(self, text: str) -> str:
    """
    Classify text into document category based on keywords.
    
    Args:
        text (str): Extracted text to classify
        
    Returns:
        str: Document category name ('others' if no match)
    """
```

**`get_category_keywords(category: str) -> list`**
```python
def get_category_keywords(self, category: str) -> list:
    """
    Get keywords for specific category.
    
    Args:
        category (str): Category name
        
    Returns:
        list: List of keywords for the category
    """
```

**Example Usage**:
```python
from core import DocumentClassifier

# Initialize classifier
classifier = DocumentClassifier()

# Classify text
category = classifier.classify_text("e-fatura ettn numarası")
print(category)  # Output: "invoices"

# Get keywords for category
keywords = classifier.get_category_keywords("invoices")
print(keywords)  # Output: ['e-fatura', 'ettn', 'fatura no', ...]
```

---

### Validators

**Location**: `core/validators.py`

Extract and validate Turkish identification numbers.

#### Class: `TCValidator`

Turkish Republic ID number validator.

##### Static Methods

**`is_valid_tc(tc: str) -> bool`**
```python
@staticmethod
def is_valid_tc(tc: str) -> bool:
    """
    Validate Turkish Republic ID number according to official algorithm.
    
    Args:
        tc (str): 11-digit TC number string
        
    Returns:
        bool: True if valid, False otherwise
    """
```

**`extract_tc_from_text(text: str) -> str`**
```python
@staticmethod
def extract_tc_from_text(text: str) -> str:
    """
    Extract valid TC number from text.
    
    Args:
        text (str): Text to search for TC numbers
        
    Returns:
        str: Valid TC number or None if not found
    """
```

#### Class: `VKNValidator`

Turkish Tax Number validator.

##### Static Methods

**`is_valid_vkn(vkn: str) -> bool`**
```python
@staticmethod
def is_valid_vkn(vkn: str) -> bool:
    """
    Validate Turkish Tax Number according to official algorithm.
    
    Args:
        vkn (str): 10-digit VKN number string
        
    Returns:
        bool: True if valid, False otherwise
    """
```

**`extract_vkn_from_text(text: str) -> str`**
```python
@staticmethod
def extract_vkn_from_text(text: str) -> str:
    """
    Extract valid VKN number from text.
    
    Args:
        text (str): Text to search for VKN numbers
        
    Returns:
        str: Valid VKN number or None if not found
    """
```

#### Class: `DocumentIdentifier`

Main class for document identification number extraction.

##### Static Methods

**`extract_identifier(text: str) -> str`**
```python
@staticmethod
def extract_identifier(text: str) -> str:
    """
    Extract TC or VKN from text, prioritizing TC.
    
    Args:
        text (str): Text to search for identifiers
        
    Returns:
        str: Valid TC or VKN number, or None if not found
    """
```

**Example Usage**:
```python
from core import TCValidator, VKNValidator, DocumentIdentifier

# Validate TC number
is_valid = TCValidator.is_valid_tc("12345678901")

# Validate VKN number
is_valid = VKNValidator.is_valid_vkn("1234567890")

# Extract any identifier from text
text = "T.C. Kimlik No: 12345678901 Vergi No: 1234567890"
identifier = DocumentIdentifier.extract_identifier(text)
```

---

### FileOperations

**Location**: `core/file_operations.py`

Handles file system operations.

#### Class: `FileOperations`

##### Static Methods

**`generate_unique_filename(code: str, folder: str, ext: str) -> str`**
```python
@staticmethod
def generate_unique_filename(code: str, folder: str, ext: str) -> str:
    """
    Generate a unique filename with date and counter if needed.
    
    Args:
        code (str): Document identifier (TC/VKN)
        folder (str): Target folder path
        ext (str): File extension without dot
        
    Returns:
        str: Unique filename
    """
```

**`ensure_directory_exists(directory_path: str)`**
```python
@staticmethod
def ensure_directory_exists(directory_path: str):
    """
    Create directory if it doesn't exist.
    
    Args:
        directory_path (str): Path to create
    """
```

**`move_file_to_category(source_path: str, category: str, new_filename: str = None) -> str`**
```python
@staticmethod
def move_file_to_category(source_path: str, category: str, new_filename: str = None) -> str:
    """
    Move file to appropriate category folder.
    
    Args:
        source_path (str): Source file path
        category (str): Target category name
        new_filename (str): New filename (optional)
        
    Returns:
        str: Final destination path
    """
```

**`get_all_files_in_directory(directory_path: str) -> list`**
```python
@staticmethod
def get_all_files_in_directory(directory_path: str) -> list:
    """
    Recursively get all files in a directory.
    
    Args:
        directory_path (str): Directory to search
        
    Returns:
        list: List of file paths
    """
```

**Example Usage**:
```python
from core import FileOperations

# Generate unique filename
filename = FileOperations.generate_unique_filename("12345678901", "uploads/ids", "pdf")

# Create directory
FileOperations.ensure_directory_exists("uploads/new_category")

# Move file
dest_path = FileOperations.move_file_to_category("doc.pdf", "invoices", "renamed.pdf")

# Get all files
files = FileOperations.get_all_files_in_directory("input_folder")
```

---

## Utility Functions

### Configuration (`core/config.py`)

**`setup_directories()`**
```python
def setup_directories():
    """Create all necessary directories for the project."""
```

### Utilities (`core/utils.py`)

**`normalize_filename(filename: str) -> str`**
```python
def normalize_filename(filename: str) -> str:
    """
    Normalize Unicode characters for Windows/macOS compatibility.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Normalized filename
    """
```

**`print_results(folder_counts: dict)`**
```python
def print_results(folder_counts: dict):
    """
    Print the processing results summary.
    
    Args:
        folder_counts (dict): Dictionary of category -> count
    """
```

### Batch Processing (`core/processor.py`)

**`process_single_file(file_path: str, idx: int, total: int) -> tuple`**
```python
def process_single_file(file_path: str, idx: int, total: int) -> tuple:
    """
    Process a single file and return the result.
    
    Args:
        file_path (str): Path to file
        idx (int): Current file index
        total (int): Total files to process
        
    Returns:
        tuple: (category, original_filename)
    """
```

**`process_files_in_directory(directory_path: str) -> list`**
```python
def process_files_in_directory(directory_path: str) -> list:
    """
    Process all files in the given directory.
    
    Args:
        directory_path (str): Directory containing files to process
        
    Returns:
        list: List of (filename, category) tuples
    """
```

---

## Legacy Compatibility

### ocr_processor.py

**`classify_document(file_path: str, return_id: bool = False)`**
```python
def classify_document(file_path: str, return_id: bool = False):
    """
    Legacy function for backward compatibility.
    
    Args:
        file_path (str): Path to document
        return_id (bool): Whether to return identifier
        
    Returns:
        tuple: (category, identifier) if return_id=True, else category only
    """
```

## Constants and Enums

### Document Categories (`core/config.py`)

```python
CATEGORY_FOLDERS = [
    'invoices', 'ids', 'cheque', 'signature_declaration',
    'residence_certificate', 'trade_registry_gazette',
    'driver_license', 'population_register', 'tax_plate',
    'contracts', 'kvkk_explicit_consent', 'digital_abf_commitment',
    'power_of_attorney', 'abf', 'cheque_customer_screening',
    'promissory_note', 'offset_and_payment_order',
    'unprocessed_return_payment_order', 'others', 'error_files',
    'factoring_agreement', 'activity_certificate', 'independent_audit_certificate'
]
```

### Upload Configuration

```python
UPLOAD_FOLDER = 'uploads'
```
