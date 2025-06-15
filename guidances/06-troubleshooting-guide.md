# Troubleshooting Guide

## 🐛 Common Issues and Solutions

This guide helps you diagnose and fix common problems with the OCR Document Processing System.

## Installation Issues

### Tesseract OCR Not Found

**Error Messages**:
```
TesseractNotFoundError: tesseract is not installed or it's not in your PATH
```

**Solutions**:

1. **macOS**:
```bash
# Install via Homebrew
brew install tesseract tesseract-lang

# Verify installation
tesseract --version

# If still not found, set path manually
export TESSERACT_CMD="/usr/local/bin/tesseract"
```

2. **Ubuntu/Debian**:
```bash
# Install Tesseract
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-tur

# Verify installation
tesseract --version
```

3. **Windows**:
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH or set environment variable
set TESSERACT_CMD="C:\Program Files\Tesseract-OCR\tesseract.exe"
```

4. **Python Code Fix**:
```python
import pytesseract

# Set Tesseract path manually
pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
```

### Missing Python Dependencies

**Error Messages**:
```
ModuleNotFoundError: No module named 'cv2'
ModuleNotFoundError: No module named 'PIL'
```

**Solution**:
```bash
# Install required packages
pip install opencv-python pillow pdf2image pytesseract

# Or install all at once
pip install -r requirements.txt
```

**Create `requirements.txt`**:
```txt
opencv-python>=4.5.0
Pillow>=8.0.0
pdf2image>=2.1.0
pytesseract>=0.3.8
```

### PDF Conversion Issues

**Error Messages**:
```
pdf2image.exceptions.PDFInfoNotInstalledError: Unable to get page count. Is poppler installed and in PATH?
```

**Solutions**:

1. **macOS**:
```bash
brew install poppler
```

2. **Ubuntu/Debian**:
```bash
sudo apt-get install poppler-utils
```

3. **Windows**:
```bash
# Download poppler from: http://blog.alivate.com.au/poppler-windows/
# Add to PATH
```

## Runtime Issues

### OCR Accuracy Problems

#### Poor Text Recognition

**Symptoms**:
- Documents classified as "others" incorrectly
- Missing text extraction
- Garbled characters

**Diagnostic Steps**:

1. **Check Image Quality**:
```python
from core import ImageProcessor

# Load and inspect image
img = ImageProcessor.load_image_from_file("problem_document.pdf")
print(f"Image shape: {img.shape}")
print(f"Image type: {img.dtype}")

# Save for manual inspection
cv2.imwrite("debug_image.jpg", img)
```

2. **Test OCR Directly**:
```python
from core import OCREngine

ocr = OCREngine()
img = ImageProcessor.load_image_from_file("problem_document.pdf")
text = ocr.extract_text_from_image(img)
print(f"Extracted text: {text}")
```

3. **Try Different OCR Settings**:
```python
# Different page segmentation modes
ocr_modes = [
    '--oem 3 --psm 3',  # Fully automatic
    '--oem 3 --psm 6',  # Uniform block (default)
    '--oem 3 --psm 8',  # Single word
    '--oem 1 --psm 6'   # LSTM only
]

for config in ocr_modes:
    ocr = OCREngine(config=config)
    text = ocr.extract_text_from_image(img)
    print(f"Config {config}: {text[:100]}...")
```

**Solutions**:

1. **Improve Image Quality**:
```python
# Increase upscaling factor
upscaled = ImageProcessor.upscale_image(img, scale_factor=3.0)

# Try different DPI for PDF
pages = convert_from_path(file_path, dpi=600)  # Higher DPI
```

2. **Image Preprocessing**:
```python
import cv2

def preprocess_image(img):
    """Apply preprocessing for better OCR."""
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply threshold
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh
```

3. **Language Configuration**:
```python
# Try multiple languages
ocr = OCREngine(language='tur+eng')  # Turkish + English
```

#### Wrong Document Classification

**Symptoms**:
- Invoices classified as "others"
- Documents going to wrong categories

**Diagnostic Steps**:

1. **Check Extracted Text**:
```python
from core import DocumentProcessor, DocumentClassifier

processor = DocumentProcessor()

# Get the actual extracted text
img = processor.image_processor.load_image_from_file("misclassified_doc.pdf")
text = processor.ocr_engine.extract_text_from_image(img)
print(f"Extracted text:\n{text}")

# Test classification
classifier = DocumentClassifier()
category = classifier.classify_text(text)
print(f"Classified as: {category}")
```

2. **Check Keywords**:
```python
# Check if expected keywords are present
expected_keywords = classifier.get_category_keywords("invoices")
print(f"Invoice keywords: {expected_keywords}")

# Check which keywords are found
found_keywords = [kw for kw in expected_keywords if kw in text.lower()]
print(f"Found keywords: {found_keywords}")
```

**Solutions**:

1. **Add Missing Keywords**:
```python
# In core/config.py, add missing keywords
CATEGORIES = {
    "invoices": [
        'e-fatura', 'fatura no', 'invoice',
        # Add new keywords found in misclassified documents
        'yeni_keyword', 'another_keyword'
    ]
}
```

2. **Check Text Encoding**:
```python
# Ensure proper Turkish character handling
text = text.replace('ı', 'i').replace('ğ', 'g')  # Normalize if needed
```

### File Processing Issues

#### Permission Errors

**Error Messages**:
```
PermissionError: [Errno 13] Permission denied: 'uploads/invoices/document.pdf'
```

**Solutions**:

1. **Check File Permissions**:
```bash
# Check permissions
ls -la uploads/

# Fix permissions
chmod 755 uploads/
chmod 644 uploads/*/*.pdf
```

2. **Check File Locks**:
```python
import time

# Add retry mechanism
def safe_move_file(source, dest, max_retries=3):
    for attempt in range(max_retries):
        try:
            shutil.move(source, dest)
            return dest
        except PermissionError:
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait and retry
                continue
            raise
```

#### File Not Found Errors

**Error Messages**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'Documents/file.pdf'
```

**Solutions**:

1. **Use Absolute Paths**:
```python
import os

# Convert to absolute path
file_path = os.path.abspath("Documents/file.pdf")
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
```

2. **Check Working Directory**:
```python
print(f"Current working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")
```

3. **Validate File Extensions**:
```python
def is_valid_file(file_path):
    """Check if file exists and has valid extension."""
    if not os.path.exists(file_path):
        return False
    
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in valid_extensions
```

### Memory Issues

#### Out of Memory Errors

**Error Messages**:
```
MemoryError: Unable to allocate array
```

**Solutions**:

1. **Process Files in Batches**:
```python
def process_files_in_batches(file_list, batch_size=10):
    """Process files in smaller batches."""
    for i in range(0, len(file_list), batch_size):
        batch = file_list[i:i + batch_size]
        for file_path in batch:
            # Process file
            process_single_file(file_path)
        
        # Force garbage collection
        import gc
        gc.collect()
```

2. **Reduce Image Quality**:
```python
# Lower DPI for PDF conversion
pages = convert_from_path(file_path, dpi=150)  # Lower DPI

# Smaller upscaling factor
upscaled = ImageProcessor.upscale_image(img, scale_factor=1.5)  # Reduced
```

3. **Monitor Memory Usage**:
```python
import psutil

def monitor_memory():
    """Monitor memory usage."""
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.2f} MB")

# Call before and after processing
monitor_memory()
```

## Configuration Issues

### Wrong Category Keywords

**Problem**: Documents not classifying correctly due to missing or incorrect keywords.

**Diagnosis**:
```python
# Test classification with sample text
from core import DocumentClassifier

classifier = DocumentClassifier()

test_text = "your document text here"
result = classifier.classify_text(test_text)
print(f"Classification result: {result}")

# Check all categories
for category, keywords in classifier.categories.items():
    matches = [kw for kw in keywords if kw in test_text.lower()]
    if matches:
        print(f"Category {category}: matched {matches}")
```

**Solution**: Update `core/config.py` with correct keywords.

### Directory Structure Issues

**Problem**: Files not moving to correct folders.

**Diagnosis**:
```python
from core.config import CATEGORY_FOLDERS, UPLOAD_FOLDER
import os

# Check if all directories exist
for category in CATEGORY_FOLDERS:
    dir_path = os.path.join(UPLOAD_FOLDER, category)
    exists = os.path.exists(dir_path)
    print(f"Directory {dir_path}: {'EXISTS' if exists else 'MISSING'}")
```

**Solution**:
```python
from core import setup_directories

# Recreate directory structure
setup_directories()
```

## Performance Issues

### Slow Processing

**Symptoms**:
- Processing takes longer than expected
- System becomes unresponsive

**Diagnostic Steps**:

1. **Profile Processing Time**:
```python
import time

def profile_processing(file_path):
    """Profile each step of processing."""
    start_time = time.time()
    
    # Load image
    img = ImageProcessor.load_image_from_file(file_path)
    load_time = time.time() - start_time
    
    # OCR
    ocr_start = time.time()
    text = OCREngine().extract_text_from_image(img)
    ocr_time = time.time() - ocr_start
    
    # Classification
    classify_start = time.time()
    category = DocumentClassifier().classify_text(text)
    classify_time = time.time() - classify_start
    
    print(f"Load: {load_time:.2f}s, OCR: {ocr_time:.2f}s, Classify: {classify_time:.2f}s")
```

2. **Monitor System Resources**:
```python
import psutil

def system_status():
    """Check system resource usage."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    print(f"CPU: {cpu_percent}%")
    print(f"Memory: {memory.percent}% used ({memory.available / 1024**3:.1f}GB available)")
```

**Solutions**:

1. **Optimize OCR Settings**:
```python
# Use faster OCR configuration
ocr = OCREngine(config='--oem 1 --psm 6')  # LSTM only, faster
```

2. **Skip Unnecessary Steps**:
```python
# Skip rotation if not needed
def quick_process(file_path):
    img = ImageProcessor.load_image_from_file(file_path)
    text = OCREngine().extract_text_from_image(img)  # No rotation
    return DocumentClassifier().classify_text(text)
```

3. **Parallel Processing**:
```python
from multiprocessing import Pool

def process_files_parallel(file_list, num_processes=4):
    """Process files in parallel."""
    with Pool(num_processes) as pool:
        results = pool.map(process_single_file, file_list)
    return results
```

## Validation Issues

### TC/VKN Extraction Problems

**Problem**: Valid TC/VKN numbers not being extracted.

**Diagnosis**:
```python
from core.validators import TCValidator, VKNValidator

# Test with known valid numbers
test_tc = "12345678901"  # Replace with valid TC
test_vkn = "1234567890"  # Replace with valid VKN

print(f"TC valid: {TCValidator.is_valid_tc(test_tc)}")
print(f"VKN valid: {VKNValidator.is_valid_vkn(test_vkn)}")

# Test extraction from text
test_text = "T.C. Kimlik No: 12345678901"
extracted = TCValidator.extract_tc_from_text(test_text)
print(f"Extracted TC: {extracted}")
```

**Solutions**:

1. **Check Text Patterns**:
```python
import re

# Debug regex patterns
text = "your extracted text here"
tc_matches = re.findall(r'\b\d{11}\b', text)
vkn_matches = re.findall(r'\b\d{10}\b', text)

print(f"11-digit numbers found: {tc_matches}")
print(f"10-digit numbers found: {vkn_matches}")
```

2. **Improve Text Cleaning**:
```python
def clean_text_for_extraction(text):
    """Clean text for better number extraction."""
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common OCR errors
    text = text.replace('O', '0').replace('l', '1').replace('I', '1')
    
    return text
```

## Debugging Tools

### Enable Debug Logging

```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add logging to your code
logger = logging.getLogger(__name__)

def process_with_logging(file_path):
    logger.debug(f"Starting processing: {file_path}")
    
    try:
        # Your processing code
        result = process_document(file_path)
        logger.info(f"Successfully processed: {file_path} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to process {file_path}: {str(e)}")
        raise
```

### Debug Image Output

```python
def save_debug_images(img, base_name):
    """Save images at different processing stages."""
    import cv2
    
    # Original
    cv2.imwrite(f"debug_{base_name}_original.jpg", img)
    
    # Rotated versions
    for angle in [90, 180, 270]:
        rotated = ImageProcessor.rotate_image(img, angle)
        cv2.imwrite(f"debug_{base_name}_rot{angle}.jpg", rotated)
    
    # Upscaled
    upscaled = ImageProcessor.upscale_image(img)
    cv2.imwrite(f"debug_{base_name}_upscaled.jpg", upscaled)
```

### Test Classification Manually

```python
def debug_classification(text):
    """Debug classification step by step."""
    from core.config import CATEGORIES
    
    text_lower = text.lower()
    print(f"Text to classify: {text_lower[:200]}...")
    
    for category, keywords in CATEGORIES.items():
        matches = [kw for kw in keywords if kw in text_lower]
        if matches:
            print(f"Category '{category}' matches: {matches}")
        else:
            print(f"Category '{category}': no matches")
```

## Getting Help

### Error Reporting Checklist

When reporting issues, include:

1. **System Information**:
   - Operating system
   - Python version
   - Package versions (`pip list`)

2. **Error Details**:
   - Full error message and stack trace
   - Input file that caused the error
   - Expected vs actual behavior

3. **Environment**:
   - Working directory
   - File permissions
   - Available disk space

4. **Reproducible Example**:
   - Minimal code that reproduces the issue
   - Sample input files (anonymized)

### Common Support Commands

```bash
# Check Python environment
python --version
pip list | grep -E "(opencv|pillow|pytesseract|pdf2image)"

# Check Tesseract
tesseract --version
tesseract --list-langs

# Check system resources
df -h  # Disk space
free -h  # Memory (Linux)
top  # Running processes

# Check file permissions
ls -la uploads/
```

### Recovery Procedures

#### Reset Directory Structure
```bash
rm -rf uploads/
python -c "from core import setup_directories; setup_directories()"
```

#### Clean Temporary Files
```bash
find . -name "temp_image.jpg" -delete
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

#### Reinstall Dependencies
```bash
pip uninstall opencv-python pillow pytesseract pdf2image
pip install opencv-python pillow pytesseract pdf2image
```
