# Architecture Guide

## 🏗️ System Architecture Overview

This guide explains the modular architecture of the OCR Document Processing System.

### Design Principles

1. **Separation of Concerns** - Each module has a single responsibility
2. **DRY Principle** - No code duplication across modules
3. **Extensibility** - Easy to add new document types and features
4. **Type Safety** - Proper type hints throughout the codebase
5. **Error Resilience** - Robust error handling and recovery

### Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Document Processing Flow                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   DocumentProcessor                         │
│  Main orchestrator that coordinates the workflow            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────┬─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ImageProcessor│     │  OCREngine  │     │ Classifiers │
│             │     │             │     │             │
│Load & Process│────▶│Extract Text │────▶│Classify Doc │
│Images/PDFs   │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                              │
                              ▼
                    ┌─────────────┐
                    │ Validators  │
                    │             │
                    │Extract TC/VKN│
                    │             │
                    └─────────────┘
                              │
                              ▼
                    ┌─────────────┐
                    │FileOperations│
                    │             │
                    │Move & Rename│
                    │             │
                    └─────────────┘
```

### Module Breakdown

#### 1. DocumentProcessor (`core/document_processor.py`)
**Purpose**: Main orchestrator that coordinates the entire processing workflow

**Key Features**:
- Manages the complete document processing pipeline
- Handles OCR retries with rotation and upscaling
- Integrates all processing components
- Error handling and fallback strategies

**Usage**:
```python
from core import DocumentProcessor

processor = DocumentProcessor()
category, identifier = processor.process_document("document.pdf", return_id=True)
```

#### 2. ImageProcessor (`core/image_processor.py`)
**Purpose**: Handles all image manipulation operations

**Key Features**:
- Load images from PDF and image files
- Image rotation (0°, 90°, 180°, 270°)
- Image upscaling for better OCR accuracy
- Format conversion between OpenCV and PIL

**Key Methods**:
```python
# Load from file (PDF or image)
img = ImageProcessor.load_image_from_file("document.pdf")

# Rotate image
rotated = ImageProcessor.rotate_image(img, 90)

# Upscale for better OCR
upscaled = ImageProcessor.upscale_image(img, scale_factor=2.0)

# Convert between formats
pil_img = ImageProcessor.convert_cv2_to_pil(cv2_img)
```

#### 3. OCREngine (`core/ocr_engine.py`)
**Purpose**: Text extraction using Tesseract OCR

**Configuration**:
- Language: Turkish (`'tur'`)
- Config: `'--oem 3 --psm 6'`
- Output: Normalized lowercase text

**Key Methods**:
```python
from core import OCREngine

ocr = OCREngine(language='tur')
text = ocr.extract_text_from_image(image)
text_with_rotation = ocr.extract_text_with_rotation(image)
text_upscaled = ocr.extract_text_with_upscaling(image)
```

#### 4. DocumentClassifier (`core/classifiers.py`)
**Purpose**: Classify documents based on extracted text content

**Features**:
- 21 predefined document categories
- Keyword-based classification
- Turkish language support
- Extensible category system

**Categories Supported** (see `core/config.py`):
```python
CATEGORIES = {
    "invoices": ["e-fatura", "fatura no", "invoice"],
    "ids": ["t.c. kimlik no", "nüfus cüzdanı", "kimlik kartı"],
    "cheque": ["çek", "keşideci", "çek seri no"],
    # ... 18 more categories
}
```

#### 5. Validators (`core/validators.py`)
**Purpose**: Extract and validate Turkish identification numbers

**Classes**:
- `TCValidator` - Turkish Republic ID (11 digits)
- `VKNValidator` - Tax Identification Number (10 digits)
- `DocumentIdentifier` - Main extraction coordinator

**TC Validation Algorithm**:
```python
# Must be 11 digits, first digit ≠ 0
# Sum of first 10 digits mod 10 = 11th digit
# ((1st+3rd+5th+7th+9th)*7 - (2nd+4th+6th+8th)) mod 10 = 10th digit
```

**VKN Validation Algorithm**:
```python
# Must be 10 digits
# Complex transformation and check digit calculation
# Based on official Turkish tax authority algorithm
```

#### 6. FileOperations (`core/file_operations.py`)
**Purpose**: Handle file system operations

**Key Features**:
- Generate unique filenames with timestamps
- Move files to category folders
- Directory creation and management
- File conflict resolution

**Usage**:
```python
from core import FileOperations

# Generate unique filename
filename = FileOperations.generate_unique_filename("12345", "folder", "pdf")

# Move file to category
FileOperations.move_file_to_category("source.pdf", "invoices", "new_name.pdf")

# Get all files in directory
files = FileOperations.get_all_files_in_directory("input_folder")
```

### Configuration System (`core/config.py`)

#### Directory Structure
```python
UPLOAD_FOLDER = 'uploads'
CATEGORY_FOLDERS = [
    'invoices', 'ids', 'cheque', 'contracts',
    'trade_registry_gazette', 'power_of_attorney',
    # ... all 21 categories
]
```

#### Category Keywords
Each category has specific Turkish keywords for classification:
```python
CATEGORIES = {
    "invoices": [
        'e-fatura', 'ettn', 'fatura no', 'fatura tarihi',
        'mal hizmet toplam tutarı', 'irsaliye'
    ],
    "contracts": [
        'taraflar arasında akdedilmiştir', 'işbu sözleşme',
        'sözleşmenin konusu', 'hak ve yükümlülükler'
    ]
}
```

### Processing Flow

1. **Input** → Document file (PDF or image)
2. **Load** → `ImageProcessor.load_image_from_file()`
3. **OCR** → `OCREngine.extract_text_from_image()`
4. **Retry** → If failed, try rotations and upscaling
5. **Classify** → `DocumentClassifier.classify_text()`
6. **Extract ID** → `DocumentIdentifier.extract_identifier()`
7. **Move** → `FileOperations.move_file_to_category()`

### Extension Points

#### Adding New Document Categories
1. Update `CATEGORY_FOLDERS` in `core/config.py`
2. Add keywords to `CATEGORIES` dictionary
3. Test with sample documents

#### Adding New Image Formats
1. Extend `ImageProcessor._load_from_image()`
2. Add format-specific handling
3. Update error handling

#### Adding New Validation Types
1. Create new validator class in `core/validators.py`
2. Implement validation algorithm
3. Update `DocumentIdentifier.extract_identifier()`

### Performance Considerations

- **Memory**: Images are processed one at a time
- **CPU**: OCR is the most intensive operation
- **I/O**: Batch processing minimizes file operations
- **Caching**: No caching implemented (stateless design)

### Error Handling Strategy

1. **Graceful Degradation** - Continue processing other files
2. **Fallback Mechanisms** - Rotation → Upscaling → Error folder
3. **Detailed Logging** - Track processing results
4. **User Feedback** - Clear progress indicators
