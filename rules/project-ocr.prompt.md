# OCR Document Classification Project Rules

## Project Overview
This project is an automated document classification system that uses OCR (Optical Character Recognition) to categorize Turkish documents and extract TC (Turkish Citizenship Number) and VKN (Tax Identification Number) from them.

The project follows a clean, modular architecture with proper separation of concerns:

```
ocr_project/
├── main.py                    # Main execution script with batch processing
├── ocr_processor.py          # Legacy compatibility layer
├── README.md                 # Comprehensive project documentation
└── core/                     # Core processing modules
    ├── __init__.py           # Module exports and public API
    ├── config.py             # Configuration, categories, and directory setup
    ├── validators.py         # TC/VKN validation and extraction logic
    ├── image_processor.py    # Image processing and manipulation
    ├── ocr_engine.py         # OCR text extraction engine
    ├── classifiers.py        # Document classification logic
    ├── file_operations.py    # File system operations and naming
    ├── document_processor.py # Main document processing orchestrator
    ├── processor.py          # Batch processing coordination
    └── utils.py              # Utility functions and helpers
```

## Core Functionality Rules

### Document Classification Categories
The system supports the following document categories (defined in `core/config.py`):
- `trade_registry_gazette` - Turkish Trade Registry Gazette documents
- `digital_abf_commitment` - Digital ABF commitment documents  
- `kvkk_explicit_consent` - KVKK (GDPR) explicit consent documents
- `factoring_agreement` - Factoring service agreements
- `power_of_attorney` - Power of attorney documents
- `signature_declaration` - Signature declaration documents
- `abf` - ABF (Receivables Notification Form) documents
- `ids` - Identity documents (ID cards, passports)
- `invoices` - Invoices and delivery notes
- `cheque` - Check documents
- `cheque_customer_screening` - Check customer screening documents
- `promissory_note` - Promissory notes
- `contracts` - General contracts
- `residence_certificate` - Residence certificates
- `driver_license` - Driver's licenses
- `population_register` - Population registry documents
- `tax_plate` - Tax plates
- `activity_certificate` - Commercial activity certificates
- `independent_audit_certificate` - Independent audit certificates
- `offset_and_payment_order` - Payment orders
- `unprocessed_return_payment_order` - Unprocessed return payment orders
- `others` - Unclassified documents
- `error_files` - Documents that failed processing

Each category is defined with specific Turkish keywords in the `CATEGORIES` dictionary.

### OCR Processing Rules (Implemented in `core/ocr_engine.py` and `core/image_processor.py`)
1. **Language Support**: Primary language is Turkish (`lang='tur'`)
2. **Image Loading**: Supports PDF (first page at 300 DPI) and image formats via `ImageProcessor.load_image_from_file()`
3. **Image Rotation**: OCR attempted with 0°, 90°, 180°, and 270° rotations using `ImageProcessor.rotate_image()`
4. **Fallback Strategy**: If initial OCR fails, retry with 2x upscaled image using `ImageProcessor.upscale_image()`
5. **Configuration**: Uses Tesseract config `--oem 3 --psm 6`
6. **Text Normalization**: All extracted text converted to lowercase for keyword matching
7. **OCR Engine Class**: `OCREngine` class handles all text extraction with configurable language and Tesseract settings
8. **Rotation Strategy**: `extract_text_with_rotation()` method tries different angles until successful classification
9. **Upscaling Fallback**: `extract_text_with_upscaling()` method provides second-chance processing for difficult documents

### ID Extraction Rules (Implemented in `core/validators.py`)

#### TC (Turkish Citizenship Number) Validation (`TCValidator` class)
- Must be exactly 11 digits
- First digit cannot be 0
- Sum of first 10 digits mod 10 must equal the 11th digit
- Special checksum validation: `((sum of odd positions * 7) - sum of even positions) mod 10 = 10th digit`
- Extraction via `TCValidator.extract_tc_from_text()`

#### VKN (Tax Identification Number) Validation (`VKNValidator` class)
- Must be exactly 10 digits
- Complex algorithm validation with transformation and checksum verification
- Extraction via `VKNValidator.extract_vkn_from_text()`

#### Document Identifier Extraction (`DocumentIdentifier` class)
- Prioritizes TC over VKN when both are present
- Uses `DocumentIdentifier.extract_identifier()` method

### File Naming Rules (Implemented in `core/file_operations.py`)
1. **With ID Detection**: Use format `{detected_id}_{DDMMYYYY}.{extension}` via `FileOperations.generate_unique_filename()`
2. **Without ID**: Keep original filename with Unicode normalization via `utils.normalize_filename()`
3. **Duplicate Handling**: Append `(counter)` before extension for duplicates
4. **Unicode Normalization**: Apply NFKC normalization for cross-platform compatibility

### Folder Structure Rules (Managed by `core/config.py` and `core/file_operations.py`)
1. **Upload Folder**: All processed files go to `uploads/` directory (defined in `UPLOAD_FOLDER`)
2. **Category Folders**: Each category has its own subfolder under `uploads/` (defined in `CATEGORY_FOLDERS`)
3. **Auto Creation**: Folders created automatically via `setup_directories()` and `FileOperations.ensure_directory_exists()`
4. **Error Handling**: Failed files moved to `error_files/` folder via `FileOperations.move_file_to_category()`

## Coding Standards

### Modular Architecture
- **Separation of Concerns**: Each module has a specific responsibility
- **Core Modules**: All business logic contained in `core/` package
- **Entry Points**: `main.py` for batch processing, individual classes for specific operations
- **Backward Compatibility**: `ocr_processor.py` maintained for legacy support

### Error Handling
- **Try-Catch Blocks**: All OCR operations wrapped in exception handling
- **Error Categories**: Failed files automatically moved to `error_files` folder with logging
- **Graceful Degradation**: System continues processing other files when individual files fail
- **Meaningful Messages**: Error messages include file context and operation details

### Performance Guidelines
1. **Image Processing**: OpenCV used for image manipulation via `ImageProcessor` class
2. **PDF Handling**: Convert only first page at 300 DPI for classification via `pdf2image`
3. **Memory Management**: Temporary files cleaned up immediately in image processing
4. **Batch Processing**: Files processed sequentially with progress indicators via `process_files_in_directory()`
5. **Rotation Strategy**: Stop at first successful classification to avoid unnecessary processing

### Output Requirements
1. **Progress Tracking**: Show `[current/total]` format during processing via `DocumentProcessor.process_single_file()`
2. **File Movement Logging**: Log original name → category (+ new name if renamed)
3. **Summary Statistics**: Display final count per category via `utils.print_results()`
4. **Error Reporting**: Include error details for failed files with truncated error messages

## Usage Examples

### Batch Processing
```python
from core import setup_directories, process_files_in_directory

# Setup and process directory
setup_directories()
process_files_in_directory("Documents")
```

### Single Document Processing
```python
from core import DocumentProcessor

processor = DocumentProcessor()
category, identifier = processor.process_document("path/to/document.pdf", return_id=True)
```

### Legacy Compatibility
```python
from ocr_processor import classify_document

category = classify_document("path/to/document.pdf")
category, identifier = classify_document("path/to/document.pdf", return_id=True)
```

## Keywords Maintenance Rules

### Adding New Keywords (in `core/config.py`)
- Keywords must be in lowercase Turkish in the `CATEGORIES` dictionary
- Include common variations and typos for better matching
- Test with real documents before deployment
- Document the source/reason for new keywords in comments

### Category Assignment Priority (`DocumentClassifier` logic)
- First matching category wins (order matters in `CATEGORIES` dict)
- More specific keywords should be in categories that appear first
- Generic keywords should be in later categories
- Classification handled by `DocumentClassifier.classify_text()` method

## File Processing Rules

### Supported Formats
- **Images**: JPG, PNG, BMP, TIFF, etc. (OpenCV supported formats)
- **PDFs**: Extract first page only for classification
- **Input Validation**: Reject files that cannot be loaded

### Security Considerations
1. **File Path Validation**: Normalize and validate all file paths
2. **Temporary Files**: Clean up immediately after use
3. **File Permissions**: Ensure proper read/write permissions
4. **Input Sanitization**: Validate file extensions and content

## Development Guidelines

### Code Organization
- **Modular Structure**: All business logic separated into `core/` modules
- **Single Responsibility**: Each module handles one specific aspect of processing
- **Clean Interfaces**: Public APIs defined in `core/__init__.py`
- **Legacy Support**: `ocr_processor.py` maintained for backward compatibility
- **Configuration Centralization**: All settings and categories in `core/config.py`

### Testing Requirements
- Test with various document orientations
- Validate ID extraction accuracy
- Test file naming collision handling
- Verify folder creation and organization

### Documentation Standards
- Comment complex algorithms (especially ID validation)
- Document all function parameters and return values
- Explain business logic behind keyword categories
- Maintain this rules document for any changes

## Deployment Rules

### Environment Setup
- Ensure Tesseract is properly installed with Turkish language support
- Verify all Python dependencies are available
- Test file system permissions for folder creation
- Validate input/output directory structure

### Monitoring and Maintenance
- Monitor error rates per document type
- Track processing performance metrics
- Regular review of misclassified documents
- Update keyword lists based on new document types

## Version Control Rules
- Commit keyword changes separately from code changes
- Test all changes with sample documents before merging
- Document breaking changes in commit messages
- Maintain backward compatibility for file naming schemes

## Class Structure and Implementation Details

### Core Classes Overview

#### `DocumentProcessor` (Main Orchestrator)
- **Purpose**: Coordinates the entire document processing workflow
- **Key Methods**: 
  - `process_document()` - Process single document with optional ID extraction
  - `process_single_file()` - Process file and move to appropriate category
  - `_try_ocr_with_rotations()` - Internal method for rotation attempts
  - `_try_ocr_with_upscaling()` - Internal method for upscaling fallback
- **Dependencies**: Uses `OCREngine`, `DocumentClassifier`, `ImageProcessor`

#### `ImageProcessor` (Static Utility Class)
- **Purpose**: Handles all image processing operations
- **Key Methods**:
  - `load_image_from_file()` - Load PDF or image files
  - `rotate_image()` - Rotate images by 90° increments
  - `upscale_image()` - Upscale images for better OCR
  - `convert_cv2_to_pil()` - Convert OpenCV to PIL format
- **PDF Handling**: Converts first page at 300 DPI using `pdf2image`

#### `OCREngine` (Configurable OCR Processor)
- **Purpose**: Handles text extraction using Tesseract
- **Configuration**: Language='tur', config='--oem 3 --psm 6'
- **Key Methods**:
  - `extract_text_from_image()` - Basic text extraction
  - `extract_text_with_rotation()` - Try multiple angles
  - `extract_text_with_upscaling()` - Fallback with upscaled image

#### `DocumentClassifier` (Text-based Classification)
- **Purpose**: Classifies documents based on extracted text
- **Algorithm**: First keyword match wins (order matters)
- **Key Methods**:
  - `classify_text()` - Main classification method
  - `get_category_keywords()` - Get keywords for specific category

#### `TCValidator` and `VKNValidator` (ID Validation)
- **TC Validation**: 11-digit algorithm with checksum validation
- **VKN Validation**: 10-digit complex transformation algorithm
- **Static Methods**: Both provide `is_valid_*()` and `extract_*_from_text()`

#### `DocumentIdentifier` (ID Extraction Coordinator)
- **Purpose**: Coordinates TC/VKN extraction with priority handling
- **Priority**: TC numbers take precedence over VKN
- **Method**: `extract_identifier()` - Returns first valid ID found

#### `FileOperations` (File System Manager)
- **Purpose**: Handles all file system operations
- **Key Features**:
  - Unique filename generation with date stamps
  - Directory creation and management
  - File moving with conflict resolution
  - Recursive directory scanning

### Processing Flow Implementation

#### 1. **Document Loading Phase**
```python
# ImageProcessor handles both PDF and image formats
img = ImageProcessor.load_image_from_file(file_path)
```

#### 2. **OCR Extraction Phase**
```python
# Try multiple rotations for best results
category, identifier = processor._try_ocr_with_rotations(img)

# Fallback to upscaled image if needed
if category == 'others':
    category, identifier = processor._try_ocr_with_upscaling(img)
```

#### 3. **Classification Phase**
```python
# Text-based classification using keyword matching
category = classifier.classify_text(extracted_text)
```

#### 4. **ID Extraction Phase**
```python
# Extract TC or VKN with priority handling
identifier = DocumentIdentifier.extract_identifier(text)
```

#### 5. **File Management Phase**
```python
# Generate unique filename and move to category folder
if identifier:
    new_filename = FileOperations.generate_unique_filename(identifier, folder, ext)
FileOperations.move_file_to_category(source, category, new_filename)
```

### Error Handling Strategy

#### **Graceful Degradation**
- Individual file failures don't stop batch processing
- Failed files moved to `error_files` category
- Error messages truncated to 50 characters for clean output

#### **Exception Hierarchy**
- OCR failures → Continue with next rotation/upscaling
- Image loading failures → Move to error_files
- File operation failures → Log and continue

#### **Logging Pattern**
```python
print(f"[{idx}/{total}] {file_name} → {category} (NEW NAME: {new_filename})")
print(f"[{idx}/{total}] {file_name} → error_files ❌ {str(e)[:50]}")
```

### Performance Optimizations

#### **Early Exit Strategy**
- Stop rotation attempts after first successful classification
- Avoid unnecessary processing once category is determined

#### **Memory Management**
- Temporary PDF files cleaned up immediately
- OpenCV images released after processing

#### **Batch Processing Efficiency**
- Sequential processing with progress indicators
- File system operations batched where possible

### Configuration Management

#### **Centralized Settings** (`core/config.py`)
- All document categories and keywords
- Folder structure definitions
- Upload path configuration

#### **Runtime Configuration**
- OCR engine language and Tesseract settings
- Image processing parameters (scale factors, DPI)
- File naming conventions

### API Design Principles

#### **Public Interface** (`core/__init__.py`)
- Clean imports for all major classes
- Functional API for common operations
- Backward compatibility maintained

#### **Legacy Support** (`ocr_processor.py`)
- Simple wrapper around new `DocumentProcessor`
- Maintains exact same function signatures
- Zero breaking changes for existing code
