# Developer Guides Index

## 📚 Complete Guide Collection for OCR Document Processing System

This directory contains comprehensive developer guides for understanding, using, and extending the OCR Document Processing System.

## 📖 Quick Navigation

### Getting Started
- **[01 - Quick Start Guide](01-quick-start-guide.md)** - Get up and running quickly
- **[02 - Architecture Guide](02-architecture-guide.md)** - Understand the system design

### Configuration & Customization  
- **[03 - Configuration Guide](03-configuration-guide.md)** - Customize and configure the system
- **[04 - API Reference](04-api-reference.md)** - Complete API documentation

### Quality Assurance
- **[05 - Testing Guide](05-testing-guide.md)** - Testing strategies and quality assurance
- **[06 - Troubleshooting Guide](06-troubleshooting-guide.md)** - Common issues and solutions

### Advanced Topics
- **[07 - Development Guide](07-development-guide.md)** - Development best practices and workflows
- **[08 - Performance Guide](08-performance-guide.md)** - Performance optimization and monitoring

## 🎯 Choose Your Path

### I'm New to the Project
1. Start with **[Quick Start Guide](01-quick-start-guide.md)** to get familiar
2. Read **[Architecture Guide](02-architecture-guide.md)** to understand the system
3. Check **[Troubleshooting Guide](06-troubleshooting-guide.md)** for common issues

### I Want to Use the System
1. **[Quick Start Guide](01-quick-start-guide.md)** - Basic usage
2. **[Configuration Guide](03-configuration-guide.md)** - Customize for your needs
3. **[API Reference](04-api-reference.md)** - Detailed method documentation

### I Want to Contribute
1. **[Architecture Guide](02-architecture-guide.md)** - Understand the design
2. **[Development Guide](07-development-guide.md)** - Setup development environment
3. **[Testing Guide](05-testing-guide.md)** - Write and run tests

### I Need to Optimize Performance
1. **[Performance Guide](08-performance-guide.md)** - Optimization strategies
2. **[Configuration Guide](03-configuration-guide.md)** - Performance settings
3. **[Troubleshooting Guide](06-troubleshooting-guide.md)** - Performance issues

### I'm Having Issues
1. **[Troubleshooting Guide](06-troubleshooting-guide.md)** - Common problems
2. **[Testing Guide](05-testing-guide.md)** - Verify your setup
3. **[Configuration Guide](03-configuration-guide.md)** - Check settings

## 📊 Guide Overview

| Guide | Focus | Target Audience | Time to Read |
|-------|-------|----------------|-------------|
| [Quick Start](01-quick-start-guide.md) | Getting started quickly | All users | 10 min |
| [Architecture](02-architecture-guide.md) | System design & structure | Developers | 20 min |
| [Configuration](03-configuration-guide.md) | Customization & settings | Power users | 25 min |
| [API Reference](04-api-reference.md) | Complete API docs | Developers | 30 min |
| [Testing](05-testing-guide.md) | Quality assurance | Developers | 35 min |
| [Troubleshooting](06-troubleshooting-guide.md) | Problem solving | All users | 15 min |
| [Development](07-development-guide.md) | Dev environment & practices | Contributors | 40 min |
| [Performance](08-performance-guide.md) | Optimization & monitoring | Advanced users | 30 min |

## 🚀 Key Features Covered

### Core Functionality
- **Document Classification** - Automatic categorization into 21+ document types
- **OCR Processing** - Text extraction with fallback strategies
- **ID Validation** - Turkish TC and VKN number extraction and validation
- **Batch Processing** - Handle multiple documents efficiently
- **File Management** - Organized folder structure and file operations

### Technical Features
- **Modular Architecture** - Clean separation of concerns
- **Error Handling** - Robust error recovery and logging
- **Performance Optimization** - Memory management and speed optimization
- **Extensibility** - Easy to add new document types and features
- **Testing Framework** - Comprehensive testing strategies

### Document Types Supported
- 📄 **Invoices** - E-fatura, delivery notes
- 🆔 **Identity Documents** - ID cards, population registry
- 💳 **Financial** - Checks, promissory notes
- 📋 **Contracts** - Various agreement types
- 🏢 **Business** - Trade registry, activity certificates
- 📑 **Legal** - Power of attorney, KVKK consent
- 🏠 **Personal** - Residence certificates, driver licenses
- 💰 **Tax** - Tax plates, audit certificates

## 🛠️ Quick Commands Reference

### Installation
```bash
# Install system dependencies
brew install tesseract tesseract-lang poppler  # macOS
sudo apt-get install tesseract-ocr tesseract-ocr-tur poppler-utils  # Ubuntu

# Install Python dependencies
pip install pytesseract opencv-python pillow pdf2image
```

### Basic Usage
```python
from core import DocumentProcessor, setup_directories

# Setup
setup_directories()
processor = DocumentProcessor()

# Process single document
category = processor.process_document("document.pdf")

# Process with ID extraction
category, identifier = processor.process_document("document.pdf", return_id=True)
```

### Batch Processing
```python
from core import process_files_in_directory

results = process_files_in_directory("Documents")
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core

# Run specific tests
pytest tests/test_validators.py
```

## 📁 Project Structure Reference

```
ocr_project/
├── main.py                    # Main execution script
├── ocr_processor.py          # Legacy compatibility layer
├── README.md                 # Project overview
├── guidances/                # This directory - all guides
│   ├── 01-quick-start-guide.md
│   ├── 02-architecture-guide.md
│   ├── 03-configuration-guide.md
│   ├── 04-api-reference.md
│   ├── 05-testing-guide.md
│   ├── 06-troubleshooting-guide.md
│   ├── 07-development-guide.md
│   ├── 08-performance-guide.md
│   └── README.md            # This file
└── core/                    # Core processing modules
    ├── __init__.py          # Module exports
    ├── config.py            # Configuration & categories
    ├── document_processor.py # Main orchestrator
    ├── image_processor.py   # Image operations
    ├── ocr_engine.py        # OCR text extraction
    ├── classifiers.py       # Document classification
    ├── validators.py        # TC/VKN validation
    ├── file_operations.py   # File system operations
    ├── processor.py         # Batch processing
    └── utils.py             # Utility functions
```

## 🎯 Common Use Cases

### Document Management System
1. Automatically classify incoming documents
2. Extract customer identifiers
3. Organize files in category folders
4. Generate processing reports

### Identity Verification
1. Extract TC/VKN numbers from documents
2. Validate identification numbers
3. Process ID documents and certificates
4. Handle various document formats

### Business Process Automation
1. Process invoices and financial documents
2. Handle legal document workflows
3. Automate document categorization
4. Integrate with existing systems

### Bulk Document Processing
1. Process large document archives
2. Migrate legacy document systems
3. Clean up unorganized document folders
4. Generate classification reports

## 🆘 Getting Help

### If You're Stuck
1. Check the **[Troubleshooting Guide](06-troubleshooting-guide.md)** first
2. Verify your setup with the **[Quick Start Guide](01-quick-start-guide.md)**
3. Review relevant configuration in **[Configuration Guide](03-configuration-guide.md)**
4. Run tests from **[Testing Guide](05-testing-guide.md)** to verify installation

### For Development Issues
1. Follow **[Development Guide](07-development-guide.md)** setup
2. Check **[Architecture Guide](02-architecture-guide.md)** for design patterns
3. Use **[API Reference](04-api-reference.md)** for method details
4. Review **[Performance Guide](08-performance-guide.md)** for optimization

### Performance Problems
1. Start with **[Performance Guide](08-performance-guide.md)**
2. Check system requirements in **[Quick Start Guide](01-quick-start-guide.md)**
3. Review configuration in **[Configuration Guide](03-configuration-guide.md)**
4. Use troubleshooting steps in **[Troubleshooting Guide](06-troubleshooting-guide.md)**

## 📝 Contributing to Documentation

### How to Improve These Guides
1. Follow the **[Development Guide](07-development-guide.md)** for setup
2. Each guide should be self-contained and focused
3. Include practical examples and code snippets
4. Test all code examples before submitting
5. Update this index when adding new guides

### Documentation Standards
- **Clear Structure** - Use consistent headings and formatting
- **Practical Examples** - Include working code samples
- **Cross References** - Link to related guides and sections
- **Up to Date** - Keep information current with code changes
- **User Focused** - Write for the target audience of each guide

---

*Last Updated: June 2025*  
*For the most current information, always refer to the individual guide files.*
