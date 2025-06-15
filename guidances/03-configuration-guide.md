# Configuration Guide

## ⚙️ System Configuration and Customization

This guide covers how to configure and customize the OCR Document Processing System.

### Configuration Files

#### Main Configuration (`core/config.py`)
This file contains all system-wide settings and document category definitions.

### Directory Configuration

#### Upload Folder Structure
```python
UPLOAD_FOLDER = 'uploads'
```

The system creates the following folder structure automatically:
```
uploads/
├── invoices/                    # E-fatura, irsaliye
├── ids/                        # Kimlik kartı, nüfus cüzdanı
├── cheque/                     # Çek belgeleri
├── contracts/                  # Sözleşmeler
├── trade_registry_gazette/     # Ticaret sicili gazetesi
├── power_of_attorney/          # Vekaletname
├── signature_declaration/      # İmza beyannamesi
├── abf/                       # ABF formu
├── cheque_customer_screening/  # Çek müşteri tarama
├── promissory_note/           # Senet
├── residence_certificate/     # Yerleşim yeri belgesi
├── driver_license/            # Sürücü belgesi
├── population_register/       # Nüfus kayıt örneği
├── tax_plate/                 # Vergi levhası
├── factoring_agreement/       # Faktoring sözleşmesi
├── activity_certificate/      # Faaliyet belgesi
├── independent_audit_certificate/ # Bağımsız denetim
├── kvkk_explicit_consent/     # KVKK açık rıza
├── digital_abf_commitment/    # Dijital ABF taahhütnamesi
├── offset_and_payment_order/  # Mahsup ve ödeme emri
├── unprocessed_return_payment_order/ # İşlenmemiş iade
├── others/                    # Sınıflandırılamayan
└── error_files/              # Hata dosyaları
```

#### Customizing Folders
To add new category folders:

```python
# In core/config.py
CATEGORY_FOLDERS = [
    'invoices', 'ids', 'cheque',
    # Add your new categories here
    'new_category_1',
    'new_category_2'
]
```

### Document Categories Configuration

#### Category Keywords System
Each document category is defined by specific Turkish keywords:

```python
CATEGORIES = {
    "category_name": [
        "keyword1", "keyword2", "keyword3"
    ]
}
```

#### Existing Categories Detail

##### 1. Invoice Documents
```python
"invoices": [
    'e-fatura', 'ettn', 'fatura no', 'fatura tarihi', 
    'fatura tipi', 'mal hizmet toplam tutarı', 'fatura',
    'invoice', 'ınvoıce', 'taşıma irsaliye', 'irsaliye',
    'müşteri v.d.', 'müşteri v.d.no.'
]
```

##### 2. Identity Documents
```python
"ids": [
    't.c. kimlik no', 't.c. kimlik no.', 'nüfus cüzdanı', 
    'kimlik kartı', 'türkiye cumhuriyeti', 'uyruğu', 
    'gender', 'nationality', 'identity card'
]
```

##### 3. Check Documents
```python
"cheque": [
    'çek', 'keşideci', 'keşide yeri', 'çek seri no', 
    'çak', 'çak no', 'tacir', 'basım tarihi', 'keşide',
    'findeks', 'mersis no', 'morsis no'
]
```

##### 4. Contract Documents
```python
"contracts": [
    'taraflar arasında akdedilmiştir', 'işbu sözleşme',
    'sözleşmenin konusu', 'hak ve yükümlülükler',
    'tarafların mutabakatı', 'kefalet', 'faktoring sözleşmesi'
]
```

#### Adding New Categories

1. **Add to CATEGORY_FOLDERS**:
```python
CATEGORY_FOLDERS = [
    # existing categories...
    'your_new_category'
]
```

2. **Define Keywords**:
```python
CATEGORIES = {
    # existing categories...
    "your_new_category": [
        'keyword1', 'keyword2', 'specific_phrase',
        'turkish_keyword', 'english_keyword'
    ]
}
```

3. **Test Classification**:
```python
from core import DocumentClassifier

classifier = DocumentClassifier()
result = classifier.classify_text("text containing your keywords")
print(result)  # Should return 'your_new_category'
```

### OCR Engine Configuration

#### Tesseract Settings (`core/ocr_engine.py`)
```python
class OCREngine:
    def __init__(self, language: str = 'tur', config: str = '--oem 3 --psm 6'):
        self.language = language    # OCR language
        self.config = config       # Tesseract configuration
```

#### Available Languages
- `'tur'` - Turkish (default)
- `'eng'` - English
- `'tur+eng'` - Turkish + English

#### Tesseract Configuration Options

##### OCR Engine Mode (OEM)
- `--oem 0` - Legacy engine only
- `--oem 1` - Neural nets LSTM engine only
- `--oem 2` - Legacy + LSTM engines
- `--oem 3` - Default, based on what is available (recommended)

##### Page Segmentation Mode (PSM)
- `--psm 6` - Uniform block of text (default)
- `--psm 3` - Fully automatic page segmentation
- `--psm 8` - Single word
- `--psm 13` - Raw line

#### Custom OCR Configuration
```python
from core import OCREngine

# Custom configuration
ocr = OCREngine(
    language='tur+eng',           # Multiple languages
    config='--oem 3 --psm 3'     # Different segmentation
)
```

### Image Processing Configuration

#### Image Processing Settings (`core/image_processor.py`)

##### PDF to Image Conversion
```python
# DPI setting for PDF conversion
pages = convert_from_path(file_path, dpi=300)  # Higher DPI = better quality
```

##### Image Upscaling
```python
def upscale_image(image_cv2, scale_factor: float = 2.0):
    # Configurable scale factor
    return cv2.resize(image_cv2, None, fx=scale_factor, fy=scale_factor)
```

##### Rotation Angles
```python
angles = [0, 90, 180, 270]  # Try these rotations
```

#### Customizing Image Processing

1. **Change PDF DPI**:
```python
# In _load_from_pdf method
pages = convert_from_path(file_path, dpi=600)  # Higher quality
```

2. **Modify Scale Factor**:
```python
# In DocumentProcessor
upscaled_img = self.image_processor.upscale_image(img, scale_factor=3.0)
```

3. **Add New Rotation Angles**:
```python
# Custom angles
angles = [0, 45, 90, 135, 180, 225, 270, 315]
```

### File Operations Configuration

#### Filename Generation (`core/file_operations.py`)
```python
def generate_unique_filename(code: str, folder: str, ext: str) -> str:
    date_str = datetime.now().strftime("%d%m%Y")  # Date format
    base_name = f"{code}_{date_str}"              # Naming pattern
```

#### Customizing File Naming

1. **Change Date Format**:
```python
date_str = datetime.now().strftime("%Y%m%d")     # YYYYMMDD
date_str = datetime.now().strftime("%d-%m-%Y")   # DD-MM-YYYY
```

2. **Custom Naming Pattern**:
```python
base_name = f"{code}_{date_str}_processed"       # Add suffix
base_name = f"doc_{code}_{date_str}"             # Add prefix
```

### Validation Configuration

#### TC Validation (`core/validators.py`)
The TC validation follows the official Turkish algorithm and cannot be customized.

#### VKN Validation (`core/validators.py`)
The VKN validation follows the official Turkish tax authority algorithm.

#### Adding Custom Validators

1. **Create New Validator Class**:
```python
class CustomValidator:
    @staticmethod
    def is_valid_custom_id(custom_id: str) -> bool:
        # Your validation logic
        return True
    
    @staticmethod
    def extract_custom_id_from_text(text: str) -> str:
        # Your extraction logic
        return "extracted_id"
```

2. **Integrate with DocumentIdentifier**:
```python
class DocumentIdentifier:
    @staticmethod
    def extract_identifier(text: str) -> str:
        # Try TC first
        tc = TCValidator.extract_tc_from_text(text)
        if tc:
            return tc
        
        # Try VKN
        vkn = VKNValidator.extract_vkn_from_text(text)
        if vkn:
            return vkn
        
        # Try your custom validator
        custom_id = CustomValidator.extract_custom_id_from_text(text)
        if custom_id:
            return custom_id
        
        return None
```

### Environment Variables

#### Optional Environment Configuration
```bash
# Tesseract executable path (if not in PATH)
export TESSERACT_CMD="/usr/local/bin/tesseract"

# Upload folder location
export OCR_UPLOAD_FOLDER="/path/to/uploads"

# OCR language
export OCR_LANGUAGE="tur"
```

#### Using Environment Variables
```python
import os
from core.config import UPLOAD_FOLDER

# Override with environment variable
upload_folder = os.getenv('OCR_UPLOAD_FOLDER', UPLOAD_FOLDER)
```

### Performance Tuning

#### Memory Optimization
```python
# Process images in smaller batches
batch_size = 10  # Process 10 files at a time

# Lower image quality for faster processing
pages = convert_from_path(file_path, dpi=150)  # Lower DPI
```

#### OCR Performance
```python
# Faster OCR configuration
config = '--oem 1 --psm 6'  # LSTM only, faster

# Skip rotation for speed
def _try_ocr_basic(self, img):
    # Only try 0° rotation
    text = self.ocr_engine.extract_text_from_image(img)
    return self.classifier.classify_text(text)
```

### Development vs Production Settings

#### Development Configuration
```python
# Verbose logging
DEBUG = True

# Lower quality for speed
PDF_DPI = 150
SCALE_FACTOR = 1.5

# Simple OCR
OCR_CONFIG = '--oem 3 --psm 6'
```

#### Production Configuration
```python
# Minimal logging
DEBUG = False

# Higher quality
PDF_DPI = 300
SCALE_FACTOR = 2.0

# Optimized OCR
OCR_CONFIG = '--oem 1 --psm 6'
```
