# Development Guide

## 👨‍💻 Developer Environment Setup and Best Practices

This guide covers development environment setup, coding standards, and contribution guidelines for the OCR system.

## Development Environment Setup

### Prerequisites

1. **Python 3.8 or higher**
2. **Git for version control**
3. **Virtual environment tools** (venv, conda, or pipenv)
4. **Code editor** (VS Code, PyCharm, etc.)

### Initial Setup

#### 1. Clone and Setup Repository

```bash
# Clone repository
git clone <repository-url>
cd ocr_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

#### 2. Install System Dependencies

```bash
# macOS
brew install tesseract tesseract-lang poppler

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-tur poppler-utils

# Verify installations
tesseract --version
python -c "import cv2, PIL, pdf2image, pytesseract; print('All packages imported successfully')"
```

#### 3. Development Dependencies

**Create `requirements-dev.txt`**:
```txt
# Testing
pytest>=6.0.0
pytest-cov>=2.10.0
pytest-mock>=3.0.0

# Code Quality
black>=21.0.0
flake8>=3.8.0
mypy>=0.800
isort>=5.0.0

# Documentation
sphinx>=4.0.0
sphinx-rtd-theme>=0.5.0

# Pre-commit hooks
pre-commit>=2.10.0
```

#### 4. IDE Configuration

**VS Code Settings** (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

**PyCharm Configuration**:
- Enable Black formatter
- Configure flake8 linting
- Set up mypy type checking
- Configure pytest as test runner

## Coding Standards

### Code Style Guidelines

#### 1. Follow PEP 8
```python
# Good
class DocumentProcessor:
    """Main document processing class."""
    
    def __init__(self):
        self.ocr_engine = OCREngine()
        self.classifier = DocumentClassifier()
    
    def process_document(self, file_path: str) -> str:
        """Process document and return category."""
        # Implementation here
        pass

# Bad
class documentProcessor:
    def __init__(self):
        self.ocrEngine=OCREngine()
        self.classifier=DocumentClassifier()
    
    def processDocument(self,filePath):
        pass
```

#### 2. Use Type Hints
```python
# Good
from typing import Optional, List, Tuple

def extract_identifier(text: str) -> Optional[str]:
    """Extract TC or VKN from text."""
    pass

def process_files(file_paths: List[str]) -> List[Tuple[str, str]]:
    """Process multiple files."""
    pass

# Bad
def extract_identifier(text):
    pass

def process_files(file_paths):
    pass
```

#### 3. Comprehensive Docstrings
```python
def classify_text(self, text: str) -> str:
    """
    Classify text into document category based on keywords.
    
    Args:
        text (str): Extracted text content to classify. Should be
                   lowercase for optimal matching.
    
    Returns:
        str: Document category name. Returns 'others' if no 
             category matches the text content.
    
    Example:
        >>> classifier = DocumentClassifier()
        >>> result = classifier.classify_text("e-fatura ettn: 12345")
        >>> print(result)
        'invoices'
    
    Note:
        Classification is based on keyword matching defined in
        the CATEGORIES configuration dictionary.
    """
```

#### 4. Error Handling
```python
# Good
def load_image_from_file(file_path: str) -> np.ndarray:
    """Load image with proper error handling."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        _, ext = os.path.splitext(file_path)
        if ext.lower() == ".pdf":
            return self._load_from_pdf(file_path)
        else:
            return self._load_from_image(file_path)
            
    except Exception as e:
        logger.error(f"Failed to load image from {file_path}: {str(e)}")
        raise ValueError(f"Could not load image: {str(e)}") from e

# Bad
def load_image_from_file(file_path):
    if file_path.endswith('.pdf'):
        return load_pdf(file_path)
    else:
        return load_image(file_path)
```

### Project Structure Guidelines

#### 1. Module Organization
```
core/
├── __init__.py          # Export public APIs
├── config.py           # Configuration constants
├── document_processor.py # Main orchestrator
├── image_processor.py  # Image operations
├── ocr_engine.py      # OCR functionality
├── classifiers.py     # Document classification
├── validators.py      # ID validation
├── file_operations.py # File system operations
├── processor.py       # Batch processing
└── utils.py          # Utility functions
```

#### 2. Clear Separation of Concerns
```python
# Good - Single Responsibility
class OCREngine:
    """Handles only OCR text extraction."""
    
    def extract_text_from_image(self, img: np.ndarray) -> str:
        """Extract text using Tesseract."""
        pass

class DocumentClassifier:
    """Handles only document classification."""
    
    def classify_text(self, text: str) -> str:
        """Classify text into categories."""
        pass

# Bad - Mixed Responsibilities
class DocumentProcessor:
    def process_document(self, file_path: str) -> str:
        # Don't mix OCR, classification, and file operations
        img = cv2.imread(file_path)  # Image loading
        text = pytesseract.image_to_string(img)  # OCR
        category = self.classify(text)  # Classification
        self.move_file(file_path, category)  # File operations
        return category
```

#### 3. Configuration Management
```python
# Good - Centralized configuration
# In core/config.py
TESSERACT_CONFIG = '--oem 3 --psm 6'
PDF_DPI = 300
UPSCALE_FACTOR = 2.0

# Use configuration
class OCREngine:
    def __init__(self, config: str = TESSERACT_CONFIG):
        self.config = config

# Bad - Hardcoded values
class OCREngine:
    def extract_text(self, img):
        text = pytesseract.image_to_string(img, config='--oem 3 --psm 6')  # Hardcoded
```

### Git Workflow

#### 1. Branch Naming Convention
```bash
# Feature branches
feature/add-new-document-type
feature/improve-ocr-accuracy

# Bug fixes
bugfix/fix-memory-leak
bugfix/handle-corrupted-pdfs

# Hotfixes
hotfix/critical-validation-error

# Documentation
docs/update-api-reference
docs/add-troubleshooting-guide
```

#### 2. Commit Message Format
```bash
# Format: <type>(<scope>): <description>

feat(classifiers): add support for new document category
fix(validators): handle edge case in TC validation
docs(guides): update troubleshooting guide
test(validators): add comprehensive TC validation tests
refactor(core): improve error handling across modules
perf(ocr): optimize image processing for large files
```

#### 3. Pull Request Guidelines
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

## Development Workflow

### 1. Setting Up Pre-commit Hooks

**Create `.pre-commit-config.yaml`**:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 21.9b0
    hooks:
      - id: black
        language_version: python3.8

  - repo: https://github.com/pycqa/isort
    rev: 5.9.3
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.910
    hooks:
      - id: mypy
```

**Install hooks**:
```bash
pre-commit install
```

### 2. Code Formatting

```bash
# Format code with Black
black core/ tests/

# Sort imports
isort core/ tests/

# Check with flake8
flake8 core/ tests/

# Type checking
mypy core/
```

### 3. Testing Workflow

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test file
pytest tests/test_validators.py

# Run tests with specific marker
pytest -m integration

# Watch mode (install pytest-watch)
ptw -- --cov=core
```

## Adding New Features

### 1. Adding New Document Category

**Step 1**: Update configuration
```python
# In core/config.py
CATEGORY_FOLDERS.append('new_category')

CATEGORIES['new_category'] = [
    'keyword1', 'keyword2', 'specific_phrase'
]
```

**Step 2**: Write tests
```python
# In tests/test_classifiers.py
def test_new_category_classification(self):
    """Test new category classification."""
    test_texts = [
        "text with keyword1",
        "another text with keyword2"
    ]
    
    for text in test_texts:
        result = self.classifier.classify_text(text)
        assert result == "new_category"
```

**Step 3**: Test with real documents
```python
# Manual testing
from core import DocumentProcessor

processor = DocumentProcessor()
category = processor.process_document("sample_new_category.pdf")
print(f"Classified as: {category}")
```

### 2. Adding New Validator

**Step 1**: Create validator class
```python
# In core/validators.py
class NewIDValidator:
    """Validator for new ID type."""
    
    @staticmethod
    def is_valid_new_id(id_number: str) -> bool:
        """Validate new ID format."""
        # Validation logic
        return True
    
    @staticmethod
    def extract_new_id_from_text(text: str) -> Optional[str]:
        """Extract new ID from text."""
        # Extraction logic
        return None
```

**Step 2**: Integrate with DocumentIdentifier
```python
# Update DocumentIdentifier.extract_identifier()
def extract_identifier(text: str) -> Optional[str]:
    # Try TC first
    tc = TCValidator.extract_tc_from_text(text)
    if tc:
        return tc
    
    # Try VKN
    vkn = VKNValidator.extract_vkn_from_text(text)
    if vkn:
        return vkn
    
    # Try new ID type
    new_id = NewIDValidator.extract_new_id_from_text(text)
    if new_id:
        return new_id
    
    return None
```

**Step 3**: Add tests
```python
class TestNewIDValidator:
    def test_valid_new_ids(self):
        valid_ids = ["valid_id_1", "valid_id_2"]
        for id_num in valid_ids:
            assert NewIDValidator.is_valid_new_id(id_num)
```

### 3. Performance Optimization

#### 1. Profiling Code
```python
import cProfile
import pstats

def profile_processing():
    """Profile document processing."""
    pr = cProfile.Profile()
    pr.enable()
    
    # Your processing code here
    processor = DocumentProcessor()
    processor.process_document("test_document.pdf")
    
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions
```

#### 2. Memory Optimization
```python
import tracemalloc

def trace_memory():
    """Trace memory usage."""
    tracemalloc.start()
    
    # Your code here
    
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
    tracemalloc.stop()
```

## Code Review Guidelines

### 1. Review Checklist

**Functionality**:
- [ ] Code solves the intended problem
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Performance is acceptable

**Code Quality**:
- [ ] Follows coding standards
- [ ] Clear and meaningful names
- [ ] Appropriate comments and docstrings
- [ ] No code duplication

**Testing**:
- [ ] Unit tests added/updated
- [ ] Tests cover edge cases
- [ ] Integration tests if needed
- [ ] Manual testing performed

**Documentation**:
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] Code comments explain why, not what

### 2. Review Comments Format

```python
# Good review comments
# Suggestion: Consider using a constant for this magic number
RETRY_ATTEMPTS = 3  # Instead of hardcoded 3

# Question: Should we handle the case where text is None?
if text is not None:
    # process text

# Praise: Great error handling here!
try:
    result = process_document(file_path)
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    return None
```

## Documentation Guidelines

### 1. Code Documentation
- Use clear, concise docstrings
- Include examples in docstrings
- Document complex algorithms
- Keep comments up to date

### 2. API Documentation
- Document all public methods
- Include parameter types and descriptions
- Provide usage examples
- Document exceptions that can be raised

### 3. User Documentation
- Write clear setup instructions
- Provide working examples
- Include troubleshooting guides
- Keep documentation current

## Security Considerations

### 1. Input Validation
```python
def validate_file_path(file_path: str) -> bool:
    """Validate file path for security."""
    # Prevent directory traversal
    if '..' in file_path:
        return False
    
    # Check file extension
    allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in allowed_extensions:
        return False
    
    return True
```

### 2. Data Handling
- Never log sensitive data (TC, VKN numbers)
- Use secure temporary file handling
- Validate all user inputs
- Handle file permissions properly

### 3. Dependency Security
```bash
# Regular security checks
pip-audit  # Check for known vulnerabilities
safety check  # Alternative security checker

# Keep dependencies updated
pip list --outdated
pip install --upgrade package_name
```

## Deployment Considerations

### 1. Environment Configuration
```python
# Use environment variables for configuration
import os

TESSERACT_CMD = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

### 2. Logging Configuration
```python
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'ocr_system.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### 3. Production Checklist
- [ ] All dependencies pinned in requirements.txt
- [ ] Environment variables configured
- [ ] Logging configured appropriately
- [ ] Error monitoring set up
- [ ] Performance monitoring in place
- [ ] Security review completed
- [ ] Documentation updated
- [ ] Backup and recovery procedures defined
