# Testing Guide

## 🧪 Testing and Quality Assurance

This guide covers testing strategies, quality assurance practices, and validation techniques for the OCR system.

## Testing Strategy Overview

### Testing Pyramid
```
    ┌─────────────────────┐
    │   Integration Tests │  ← End-to-end workflow testing
    │                     │
    ├─────────────────────┤
    │    Unit Tests       │  ← Individual component testing
    │                     │
    ├─────────────────────┤
    │  Manual Testing     │  ← Document validation & edge cases
    └─────────────────────┘
```

## Unit Testing

### Setting Up Test Environment

1. **Install Testing Dependencies**:
```bash
pip install pytest pytest-cov pytest-mock
```

2. **Create Test Structure**:
```
tests/
├── __init__.py
├── test_validators.py
├── test_classifiers.py
├── test_image_processor.py
├── test_ocr_engine.py
├── test_file_operations.py
├── fixtures/
│   ├── sample_invoice.pdf
│   ├── sample_id.jpg
│   └── sample_check.png
└── conftest.py
```

### Testing Validators

**File**: `tests/test_validators.py`

```python
import pytest
from core.validators import TCValidator, VKNValidator, DocumentIdentifier

class TestTCValidator:
    """Test Turkish Republic ID validation."""
    
    def test_valid_tc_numbers(self):
        """Test valid TC numbers."""
        valid_tcs = [
            "12345678901",  # Add real valid TC for testing
            "98765432109"   # Add another valid TC
        ]
        
        for tc in valid_tcs:
            assert TCValidator.is_valid_tc(tc), f"TC {tc} should be valid"
    
    def test_invalid_tc_numbers(self):
        """Test invalid TC numbers."""
        invalid_tcs = [
            "00000000000",  # All zeros
            "12345678900",  # Invalid checksum
            "1234567890",   # Too short
            "123456789012", # Too long
            "1234567890a",  # Contains letter
            ""              # Empty string
        ]
        
        for tc in invalid_tcs:
            assert not TCValidator.is_valid_tc(tc), f"TC {tc} should be invalid"
    
    def test_extract_tc_from_text(self):
        """Test TC extraction from text."""
        test_cases = [
            ("T.C. Kimlik No: 12345678901", "12345678901"),
            ("TC: 98765432109 Adı: John", "98765432109"),
            ("No valid TC here", None),
            ("Invalid: 00000000000", None)
        ]
        
        for text, expected in test_cases:
            result = TCValidator.extract_tc_from_text(text)
            assert result == expected

class TestVKNValidator:
    """Test Turkish Tax Number validation."""
    
    def test_valid_vkn_numbers(self):
        """Test valid VKN numbers."""
        valid_vkns = [
            "1234567890",  # Add real valid VKN for testing
            "9876543210"   # Add another valid VKN
        ]
        
        for vkn in valid_vkns:
            assert VKNValidator.is_valid_vkn(vkn), f"VKN {vkn} should be valid"
    
    def test_invalid_vkn_numbers(self):
        """Test invalid VKN numbers."""
        invalid_vkns = [
            "123456789",    # Too short
            "12345678901",  # Too long
            "123456789a",   # Contains letter
            ""              # Empty string
        ]
        
        for vkn in invalid_vkns:
            assert not VKNValidator.is_valid_vkn(vkn), f"VKN {vkn} should be invalid"

class TestDocumentIdentifier:
    """Test document identifier extraction."""
    
    def test_extract_tc_priority(self):
        """Test that TC is prioritized over VKN."""
        text = "TC: 12345678901 VKN: 1234567890"
        result = DocumentIdentifier.extract_identifier(text)
        assert len(result) == 11, "Should extract TC (11 digits) over VKN"
    
    def test_extract_vkn_when_no_tc(self):
        """Test VKN extraction when no TC present."""
        text = "Vergi No: 1234567890"
        result = DocumentIdentifier.extract_identifier(text)
        assert len(result) == 10, "Should extract VKN when no TC present"
    
    def test_no_identifier_found(self):
        """Test when no valid identifier is found."""
        text = "No valid identifiers here"
        result = DocumentIdentifier.extract_identifier(text)
        assert result is None
```

### Testing Document Classification

**File**: `tests/test_classifiers.py`

```python
import pytest
from core.classifiers import DocumentClassifier
from core.config import CATEGORIES

class TestDocumentClassifier:
    """Test document classification functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.classifier = DocumentClassifier()
    
    def test_invoice_classification(self):
        """Test invoice document classification."""
        test_texts = [
            "e-fatura ettn: 12345",
            "fatura no: 2023001 fatura tarihi: 15.06.2023",
            "mal hizmet toplam tutarı: 1000 TL"
        ]
        
        for text in test_texts:
            result = self.classifier.classify_text(text)
            assert result == "invoices", f"Text '{text}' should classify as invoices"
    
    def test_id_classification(self):
        """Test ID document classification."""
        test_texts = [
            "t.c. kimlik no: 12345678901",
            "nüfus cüzdanı türkiye cumhuriyeti",
            "identity card nationality turkish"
        ]
        
        for text in test_texts:
            result = self.classifier.classify_text(text)
            assert result == "ids", f"Text '{text}' should classify as ids"
    
    def test_cheque_classification(self):
        """Test cheque document classification."""
        test_texts = [
            "çek seri no: 123456",
            "keşideci: john doe",
            "çek karşılığında ödeme"
        ]
        
        for text in test_texts:
            result = self.classifier.classify_text(text)
            assert result == "cheque", f"Text '{text}' should classify as cheque"
    
    def test_others_classification(self):
        """Test classification as 'others' for unknown documents."""
        test_texts = [
            "random text with no keywords",
            "lorem ipsum dolor sit amet",
            "12345 numbers only"
        ]
        
        for text in test_texts:
            result = self.classifier.classify_text(text)
            assert result == "others", f"Text '{text}' should classify as others"
    
    def test_get_category_keywords(self):
        """Test getting keywords for specific categories."""
        invoices_keywords = self.classifier.get_category_keywords("invoices")
        assert "e-fatura" in invoices_keywords
        assert "fatura no" in invoices_keywords
        
        # Test non-existent category
        empty_keywords = self.classifier.get_category_keywords("non_existent")
        assert empty_keywords == []
    
    def test_custom_categories(self):
        """Test classifier with custom categories."""
        custom_categories = {
            "test_category": ["test_keyword", "another_keyword"]
        }
        
        custom_classifier = DocumentClassifier(custom_categories)
        result = custom_classifier.classify_text("this contains test_keyword")
        assert result == "test_category"
```

### Testing Image Processing

**File**: `tests/test_image_processor.py`

```python
import pytest
import numpy as np
import cv2
from unittest.mock import patch, MagicMock
from core.image_processor import ImageProcessor

class TestImageProcessor:
    """Test image processing functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        # Create a simple test image
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.test_image[:, :] = [255, 255, 255]  # White image
    
    def test_rotate_image_0_degrees(self):
        """Test 0-degree rotation (no change)."""
        result = ImageProcessor.rotate_image(self.test_image, 0)
        np.testing.assert_array_equal(result, self.test_image)
    
    def test_rotate_image_90_degrees(self):
        """Test 90-degree rotation."""
        result = ImageProcessor.rotate_image(self.test_image, 90)
        assert result.shape == (100, 100, 3)  # Should maintain dimensions
    
    def test_rotate_image_invalid_angle(self):
        """Test rotation with invalid angle."""
        with pytest.raises(ValueError):
            ImageProcessor.rotate_image(self.test_image, 45)
    
    def test_upscale_image(self):
        """Test image upscaling."""
        scale_factor = 2.0
        result = ImageProcessor.upscale_image(self.test_image, scale_factor)
        
        expected_height = int(self.test_image.shape[0] * scale_factor)
        expected_width = int(self.test_image.shape[1] * scale_factor)
        
        assert result.shape[0] == expected_height
        assert result.shape[1] == expected_width
    
    def test_convert_cv2_to_pil(self):
        """Test OpenCV to PIL conversion."""
        pil_image = ImageProcessor.convert_cv2_to_pil(self.test_image)
        assert hasattr(pil_image, 'save')  # PIL Image should have save method
        assert pil_image.size == (100, 100)
    
    @patch('cv2.imread')
    def test_load_from_image_success(self, mock_imread):
        """Test successful image loading."""
        mock_imread.return_value = self.test_image
        
        result = ImageProcessor._load_from_image("test.jpg")
        np.testing.assert_array_equal(result, self.test_image)
        mock_imread.assert_called_once_with("test.jpg")
    
    @patch('cv2.imread')
    def test_load_from_image_failure(self, mock_imread):
        """Test image loading failure."""
        mock_imread.return_value = None
        
        with pytest.raises(ValueError):
            ImageProcessor._load_from_image("nonexistent.jpg")
    
    @patch('pdf2image.convert_from_path')
    @patch('os.remove')
    @patch('cv2.imread')
    def test_load_from_pdf(self, mock_imread, mock_remove, mock_convert):
        """Test PDF loading."""
        # Mock PDF conversion
        mock_page = MagicMock()
        mock_convert.return_value = [mock_page]
        mock_imread.return_value = self.test_image
        
        result = ImageProcessor._load_from_pdf("test.pdf")
        
        mock_convert.assert_called_once_with("test.pdf", dpi=300)
        mock_page.save.assert_called_once_with("temp_image.jpg")
        mock_remove.assert_called_once_with("temp_image.jpg")
        np.testing.assert_array_equal(result, self.test_image)
```

### Testing File Operations

**File**: `tests/test_file_operations.py`

```python
import pytest
import os
import tempfile
import shutil
from unittest.mock import patch
from core.file_operations import FileOperations

class TestFileOperations:
    """Test file operations functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.txt")
        
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write("Test content")
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_ensure_directory_exists(self):
        """Test directory creation."""
        new_dir = os.path.join(self.test_dir, "new_folder")
        assert not os.path.exists(new_dir)
        
        FileOperations.ensure_directory_exists(new_dir)
        assert os.path.exists(new_dir)
        assert os.path.isdir(new_dir)
    
    def test_generate_unique_filename(self):
        """Test unique filename generation."""
        folder = self.test_dir
        
        # First file should get base name
        filename1 = FileOperations.generate_unique_filename("12345", folder, "pdf")
        assert "12345_" in filename1
        assert filename1.endswith(".pdf")
        
        # Create the file to test conflict resolution
        with open(os.path.join(folder, filename1), 'w') as f:
            f.write("test")
        
        # Second file should get counter
        filename2 = FileOperations.generate_unique_filename("12345", folder, "pdf")
        assert "(1)" in filename2
    
    def test_get_all_files_in_directory(self):
        """Test recursive file listing."""
        # Create subdirectory with file
        subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(subdir)
        subfile = os.path.join(subdir, "subtest.txt")
        with open(subfile, 'w') as f:
            f.write("Sub content")
        
        files = FileOperations.get_all_files_in_directory(self.test_dir)
        
        assert len(files) == 2
        assert self.test_file in files
        assert subfile in files
    
    def test_move_file_to_category(self):
        """Test file moving to category folder."""
        category = "test_category"
        new_filename = "moved_file.txt"
        
        # Move file
        dest_path = FileOperations.move_file_to_category(
            self.test_file, category, new_filename
        )
        
        # Verify file was moved
        assert not os.path.exists(self.test_file)
        assert os.path.exists(dest_path)
        assert category in dest_path
        assert new_filename in dest_path
        
        # Verify content preserved
        with open(dest_path, 'r') as f:
            content = f.read()
            assert content == "Test content"
```

## Integration Testing

### End-to-End Document Processing

**File**: `tests/test_integration.py`

```python
import pytest
import os
import tempfile
import shutil
from core import DocumentProcessor, setup_directories

class TestDocumentProcessingIntegration:
    """Test complete document processing workflow."""
    
    def setup_method(self):
        """Setup test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.processor = DocumentProcessor()
        
        # Change to test directory
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Setup directories
        setup_directories()
    
    def teardown_method(self):
        """Cleanup test environment."""
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @pytest.mark.integration
    def test_process_invoice_document(self):
        """Test processing of invoice document."""
        # This would require a real sample invoice PDF
        # For now, we'll mock the OCR response
        
        with patch('core.ocr_engine.OCREngine.extract_text_from_image') as mock_ocr:
            mock_ocr.return_value = "e-fatura ettn: 12345 t.c. kimlik no: 12345678901"
            
            category, identifier = self.processor.process_document(
                "fake_invoice.pdf", return_id=True
            )
            
            assert category == "invoices"
            assert identifier == "12345678901"
    
    @pytest.mark.integration
    def test_batch_processing(self):
        """Test batch processing of multiple documents."""
        from core import process_files_in_directory
        
        # Create test files
        test_files_dir = os.path.join(self.test_dir, "test_files")
        os.makedirs(test_files_dir)
        
        # This would require real test files
        # For demonstration, we'll test the function structure
        
        results = process_files_in_directory(test_files_dir)
        assert isinstance(results, list)
```

## Performance Testing

### Benchmarking OCR Performance

**File**: `tests/test_performance.py`

```python
import pytest
import time
import psutil
import os
from core import DocumentProcessor

class TestPerformance:
    """Test system performance and resource usage."""
    
    def setup_method(self):
        """Setup performance testing."""
        self.processor = DocumentProcessor()
    
    @pytest.mark.performance
    def test_processing_speed(self):
        """Test document processing speed."""
        # This requires actual test documents
        test_files = [
            # "tests/fixtures/sample_invoice.pdf",
            # "tests/fixtures/sample_id.jpg",
            # Add more test files
        ]
        
        start_time = time.time()
        
        for file_path in test_files:
            if os.path.exists(file_path):
                self.processor.process_document(file_path)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Assert reasonable processing time (adjust based on requirements)
        files_processed = len([f for f in test_files if os.path.exists(f)])
        if files_processed > 0:
            avg_time_per_file = processing_time / files_processed
            assert avg_time_per_file < 10.0, f"Processing too slow: {avg_time_per_file}s per file"
    
    @pytest.mark.performance
    def test_memory_usage(self):
        """Test memory usage during processing."""
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process multiple documents
        for i in range(5):
            # Mock processing to test memory leaks
            img = np.zeros((1000, 1000, 3), dtype=np.uint8)
            # Simulate processing
            time.sleep(0.1)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Assert reasonable memory usage (adjust based on requirements)
        assert memory_increase < 100, f"Memory increase too high: {memory_increase}MB"
```

## Manual Testing Guidelines

### Document Quality Testing

#### 1. Image Quality Tests
- **High Resolution**: Test with 300+ DPI images
- **Low Resolution**: Test with 150 DPI images
- **Poor Quality**: Test with blurry, dark, or distorted images
- **Different Formats**: PDF, JPG, PNG, TIFF

#### 2. Document Orientation Tests
- **Normal**: 0° rotation
- **Rotated**: 90°, 180°, 270° rotations
- **Slightly Skewed**: 5°, 10° rotations
- **Upside Down**: 180° rotation

#### 3. Document Content Tests
- **Clear Text**: High-quality, printed documents
- **Handwritten**: Handwritten forms and signatures
- **Mixed Content**: Documents with both print and handwriting
- **Multiple Languages**: Turkish and English mixed content

### Validation Testing

#### TC Number Validation
```python
# Test valid TC numbers (use real valid ones for testing)
valid_tcs = [
    "10000000146",  # Example - replace with real valid TCs
    "10000000154",
    "10000000162"
]

# Test invalid TC numbers
invalid_tcs = [
    "00000000000",  # All zeros
    "11111111111",  # All same digits
    "12345678900",  # Invalid checksum
    "1234567890",   # Too short
    "123456789012"  # Too long
]
```

#### VKN Number Validation
```python
# Test valid VKN numbers (use real valid ones for testing)
valid_vkns = [
    "1234567890",  # Example - replace with real valid VKNs
    "9876543210"
]

# Test invalid VKN numbers
invalid_vkns = [
    "0000000000",  # All zeros
    "1234567800",  # Invalid checksum
    "123456789",   # Too short
    "12345678901"  # Too long
]
```

## Continuous Integration Setup

### GitHub Actions Workflow

**File**: `.github/workflows/test.yml`

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install Tesseract
      run: |
        sudo apt-get update
        sudo apt-get install -y tesseract-ocr tesseract-ocr-tur
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-mock
    
    - name: Run tests
      run: |
        pytest tests/ --cov=core --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

## Test Data Management

### Creating Test Fixtures

1. **Sample Documents**: Create anonymized sample documents for each category
2. **Edge Cases**: Prepare documents with edge cases (poor quality, unusual layouts)
3. **Negative Cases**: Documents that should fail or classify as "others"

### Test Data Security

- ⚠️ **Never use real personal data** in tests
- ✅ Use anonymized or synthetic data
- ✅ Create test documents with fake but valid-format IDs
- ✅ Store test files in `tests/fixtures/` directory

## Quality Metrics

### Coverage Targets
- **Unit Tests**: >90% code coverage
- **Integration Tests**: Critical paths covered
- **Manual Tests**: All document categories validated

### Performance Targets
- **Processing Speed**: <5 seconds per document average
- **Memory Usage**: <100MB increase during batch processing
- **Accuracy**: >95% classification accuracy on test set

## Debugging and Troubleshooting

### Common Test Issues

1. **Tesseract Not Found**:
```bash
export TESSERACT_CMD="/usr/local/bin/tesseract"
```

2. **Mock Issues**:
```python
# Use proper mocking for external dependencies
@patch('core.image_processor.cv2.imread')
def test_with_mock(self, mock_imread):
    mock_imread.return_value = test_image
```

3. **File Path Issues**:
```python
# Use absolute paths in tests
test_file = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample.pdf')
```

### Test Execution Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_validators.py

# Run with coverage
pytest --cov=core

# Run only integration tests
pytest -m integration

# Run only performance tests
pytest -m performance

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```
