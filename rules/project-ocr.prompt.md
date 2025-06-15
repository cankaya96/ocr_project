# OCR Document Classification Project Rules

## Project Overview
This project is an automated document classification system that uses OCR (Optical Character Recognition) to categorize Turkish documents and extract TC (Turkish Citizenship Number) and VKN (Tax Identification Number) from them.

## Core Functionality Rules

### Document Classification Categories
The system must support the following document categories:
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

### OCR Processing Rules
1. **Language Support**: Primary language is Turkish (`lang='tur'`)
2. **Image Rotation**: Must attempt OCR with 0°, 90°, 180°, and 270° rotations
3. **Fallback Strategy**: If initial OCR fails, retry with 2x upscaled image
4. **Configuration**: Use Tesseract config `--oem 3 --psm 6`
5. **Text Normalization**: Convert all extracted text to lowercase for keyword matching

### ID Extraction Rules

#### TC (Turkish Citizenship Number) Validation
- Must be exactly 11 digits
- First digit cannot be 0
- Sum of first 10 digits mod 10 must equal the 11th digit
- Special checksum validation: `((sum of odd positions * 7) - sum of even positions) mod 10 = 10th digit`

#### VKN (Tax Identification Number) Validation
- Must be exactly 10 digits
- Complex algorithm validation with transformation and checksum verification

### File Naming Rules
1. **With ID Detection**: Use format `{detected_id}_{DDMMYYYY}.{extension}`
2. **Without ID**: Keep original filename
3. **Duplicate Handling**: Append `(counter)` before extension for duplicates
4. **Unicode Normalization**: Apply NFKC normalization for cross-platform compatibility

### Folder Structure Rules
1. **Upload Folder**: All processed files go to `uploads/` directory
2. **Category Folders**: Each category has its own subfolder under `uploads/`
3. **Auto Creation**: Folders are created automatically if they don't exist
4. **Error Handling**: Failed files go to `error_files/` folder

## Coding Standards

### Error Handling
- Always use try-catch blocks for OCR operations
- Move failed files to `error_files` folder with error logging
- Provide meaningful error messages with file context

### Performance Guidelines
1. **Image Processing**: Use OpenCV for image manipulation
2. **PDF Handling**: Convert only first page at 300 DPI for classification
3. **Memory Management**: Clean up temporary files immediately
4. **Batch Processing**: Process files sequentially with progress indicators

### Output Requirements
1. **Progress Tracking**: Show `[current/total]` format during processing
2. **File Movement Logging**: Log original name → category (+ new name if renamed)
3. **Summary Statistics**: Display final count per category
4. **Error Reporting**: Include error details for failed files

## Keywords Maintenance Rules

### Adding New Keywords
- Keywords must be in lowercase Turkish
- Include common variations and typos
- Test with real documents before deployment
- Document the source/reason for new keywords

### Category Assignment Priority
- First matching category wins (order matters in categories dict)
- More specific keywords should be in categories that appear first
- Generic keywords should be in later categories

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
- Keep OCR logic in `ocr_processor.py`
- Keep main processing logic in `main.py`
- Separate concerns: classification, ID extraction, file operations
- Use descriptive function and variable names

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
