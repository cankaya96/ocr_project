# OCR Document Processing System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OCR](https://img.shields.io/badge/OCR-Tesseract-green.svg)](https://github.com/tesseract-ocr/tesseract)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red.svg)](https://opencv.org/)

A modular OCR document processing system for classifying Turkish documents and extracting identification numbers (TC/VKN). This project is developed for complex document archive separation, grouping, and identification processes at **MasterFabric** and is actively used by **Ulusal Faktoring** for their document management workflow.

## 👥 Contributors

- **[@cankaya96](https://github.com/cankaya96)** - Architecture Designer & Lead Developer
  - Planned and designed the core architecture of the project
  - Responsible for foundational development and implementation

- **[@gurkanfikretgunak](https://github.com/gurkanfikretgunak)** - Project Structure & Code Standards Lead
  - Established project context and boilerplate standards
  - Managed code-style structure and business requirements
  - Supervised project management and development workflow

## 🏢 Company References

This project is developed by **MasterFabric** and is actively used in production by:

### MasterFabric
- **Website**: [https://www.masterfabric.co](https://www.masterfabric.co)
- **LinkedIn**: [https://www.linkedin.com/company/masterfabric](https://www.linkedin.com/company/masterfabric)

### Ulusal Faktoring
- **Website**: [https://www.ulusalfaktoring.com/](https://www.ulusalfaktoring.com/)
- **LinkedIn**: [https://www.linkedin.com/company/ulusalfaktoring/](https://www.linkedin.com/company/ulusalfaktoring/)

## 🏗️ Architecture

The project has been refactored into a clean, modular structure following DRY principles and separation of concerns:

```
ocr_project/
├── main.py                    # Main execution script
├── ocr_processor.py          # Legacy compatibility layer
└── core/                     # Core processing modules
    ├── __init__.py           # Module exports
    ├── config.py             # Configuration and categories
    ├── validators.py         # TC/VKN validation logic
    ├── image_processor.py    # Image processing operations
    ├── ocr_engine.py         # OCR text extraction
    ├── classifiers.py        # Document classification
    ├── file_operations.py    # File system operations
    ├── document_processor.py # Main document processing orchestrator
    ├── processor.py          # Batch processing functionality
    └── utils.py              # Utility functions
```

## 🚀 Key Features

- **Modular Design**: Each component has a single responsibility
- **Type Safety**: Proper type hints throughout the codebase
- **Error Handling**: Robust error handling and logging
- **Extensible**: Easy to add new document types and validators
- **DRY Principle**: No code duplication
- **Backward Compatibility**: Legacy `ocr_processor.py` still works

## 📦 Core Modules

### DocumentProcessor
Main orchestrator that coordinates the entire processing workflow:
```python
from core import DocumentProcessor

processor = DocumentProcessor()
category, identifier = processor.process_document("document.pdf", return_id=True)
```

### Validators
TC (Turkish Republic ID) and VKN (Tax Number) validation:
```python
from core import TCValidator, VKNValidator, DocumentIdentifier

# Validate TC number
is_valid = TCValidator.is_valid_tc("12345678901")

# Extract identifier from text
identifier = DocumentIdentifier.extract_identifier(text)
```

### ImageProcessor
Image processing operations for OCR:
```python
from core import ImageProcessor

# Load and process images
img = ImageProcessor.load_image_from_file("document.pdf")
rotated = ImageProcessor.rotate_image(img, 90)
upscaled = ImageProcessor.upscale_image(img, 2.0)
```

### OCREngine
Text extraction using Tesseract:
```python
from core import OCREngine

ocr = OCREngine(language='tur')
text = ocr.extract_text_from_image(image)
```

### DocumentClassifier
Document classification based on content:
```python
from core import DocumentClassifier

classifier = DocumentClassifier()
category = classifier.classify_text(extracted_text)
```

### FileOperations
File system operations:
```python
from core import FileOperations

# Generate unique filename
filename = FileOperations.generate_unique_filename("12345", "folder", "pdf")

# Move file to category
FileOperations.move_file_to_category("source.pdf", "invoices", "new_name.pdf")
```

## 🔄 Usage Examples

### Batch Processing
```python
from core import setup_directories, process_files_in_directory

# Setup folder structure
setup_directories()

# Process all files in a directory
results = process_files_in_directory("input_folder")
```

### Single Document Processing
```python
from core import DocumentProcessor

processor = DocumentProcessor()

# Process with category only
category = processor.process_document("document.pdf")

# Process with identifier extraction
category, identifier = processor.process_document("document.pdf", return_id=True)
```

### Legacy Compatibility
```python
# Old code still works
from ocr_processor import classify_document

category = classify_document("document.pdf")
category, identifier = classify_document("document.pdf", return_id=True)
```

## 📋 Document Categories

The system classifies documents into the following categories:

- `invoices` - E-fatura, irsaliye
- `ids` - Kimlik kartı, nüfus cüzdanı
- `cheque` - Çek belgeleri
- `contracts` - Sözleşmeler
- `trade_registry_gazette` - Ticaret sicili gazetesi
- `tax_plate` - Vergi levhası
- `power_of_attorney` - Vekaletname
- `signature_declaration` - İmza beyannamesi
- And many more...

## 🛠️ Installation

1. Install required dependencies:
```bash
pip install pytesseract pillow opencv-python pdf2image
```

2. Ensure Tesseract is installed on your system
3. Configure Tesseract path if needed

## 🏃‍♂️ Running

```bash
python main.py
```

## 🧪 Testing

Each module can be tested independently:

```python
# Test validators
from core.validators import TCValidator
assert TCValidator.is_valid_tc("12345678901") == False

# Test image processing
from core.image_processor import ImageProcessor
img = ImageProcessor.load_image_from_file("test.pdf")

# Test classification
from core.classifiers import DocumentClassifier
classifier = DocumentClassifier()
category = classifier.classify_text("fatura no: 123")
```

## 🔧 Configuration

All configuration is centralized in `core/config.py`:

- Document categories and keywords
- Folder structure
- Upload paths

## 📈 Benefits of the New Structure

1. **Maintainability**: Each module has a clear purpose
2. **Testability**: Individual components can be tested in isolation
3. **Extensibility**: Easy to add new document types or validators
4. **Reusability**: Components can be used in different contexts
5. **Debugging**: Easier to identify and fix issues
6. **Performance**: Better resource management and optimization opportunities

## 🔄 Migration Guide

If you have existing code using the old structure:

**Old way:**
```python
from ocr_processor import classify_document, is_valid_tc
```

**New way:**
```python
from core import DocumentProcessor, TCValidator

processor = DocumentProcessor()
category = processor.process_document("file.pdf")
is_valid = TCValidator.is_valid_tc("12345678901")
```

The old `ocr_processor.py` still works for backward compatibility, but new development should use the modular structure.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 [@cankaya96](https://github.com/cankaya96) and [@gurkanfikretgunak](https://github.com/gurkanfikretgunak)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
