# Quick Start Guide

## 🚀 Getting Started with OCR Document Processing System

This guide helps you get up and running with the OCR Document Processing System quickly.

### Prerequisites

1. **Python 3.8+** installed
2. **Tesseract OCR** installed for text extraction
3. **Required Python packages** (see Installation section)

### Installation

1. **Install Tesseract OCR:**
   ```bash
   # macOS
   brew install tesseract tesseract-lang
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-tur
   
   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install pytesseract opencv-python pillow pdf2image
   ```

3. **Verify Installation:**
   ```python
   import pytesseract
   print(pytesseract.get_tesseract_version())
   ```

### Basic Usage

#### 1. Process a Single Document

```python
from core import DocumentProcessor

# Initialize processor
processor = DocumentProcessor()

# Process document - returns category only
category = processor.process_document("path/to/document.pdf")
print(f"Document category: {category}")

# Process document - returns category and identifier (TC/VKN)
category, identifier = processor.process_document("path/to/document.pdf", return_id=True)
print(f"Category: {category}, ID: {identifier}")
```

#### 2. Batch Process Documents

```python
from core import setup_directories, process_files_in_directory

# Setup folder structure
setup_directories()

# Process all files in a directory
results = process_files_in_directory("Documents")
```

#### 3. Legacy Compatibility

```python
# Old code still works
from ocr_processor import classify_document

category = classify_document("document.pdf")
category, identifier = classify_document("document.pdf", return_id=True)
```

### Project Structure Overview

```
ocr_project/
├── main.py                    # Main execution script
├── ocr_processor.py          # Legacy compatibility layer
└── core/                     # Core processing modules
    ├── __init__.py           # Module exports
    ├── config.py             # Configuration and categories
    ├── document_processor.py # Main processing orchestrator
    ├── image_processor.py    # Image manipulation
    ├── ocr_engine.py         # Text extraction
    ├── classifiers.py        # Document classification
    ├── validators.py         # TC/VKN validation
    ├── file_operations.py    # File system operations
    ├── processor.py          # Batch processing
    └── utils.py              # Utility functions
```

### Key Features

- ✅ **21 Document Categories** - From invoices to contracts
- ✅ **Turkish ID Validation** - TC and VKN number extraction and validation
- ✅ **Multiple Formats** - PDF and image support
- ✅ **Smart OCR** - Rotation and upscaling fallback
- ✅ **Modular Design** - Easy to extend and maintain
- ✅ **Error Handling** - Robust error recovery
- ✅ **Batch Processing** - Process entire directories

### Next Steps

- 📖 Read the [Architecture Guide](02-architecture-guide.md) for detailed system design
- 🔧 Check [Configuration Guide](03-configuration-guide.md) for customization
- 🧪 See [Testing Guide](05-testing-guide.md) for quality assurance
- 🐛 Review [Troubleshooting Guide](06-troubleshooting-guide.md) for common issues

### Common Use Cases

1. **Document Classification System** - Automatically categorize incoming documents
2. **Identity Extraction** - Extract and validate Turkish ID numbers
3. **Bulk Document Processing** - Process hundreds of documents at once
4. **Document Workflow Automation** - Integrate with existing systems

### Performance Tips

- 📊 For large batches, consider processing in chunks
- 🖼️ High-resolution images work better for OCR
- 🔄 Most documents classify correctly on first try
- 📁 Use descriptive folder names for organized output
