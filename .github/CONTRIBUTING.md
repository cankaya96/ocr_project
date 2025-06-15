# Contributing to OCR Project 🤝

Thank you for your interest in contributing to our OCR system! We welcome contributions from the community and are excited to see what you'll build.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Workflow](#contributing-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Community](#community)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- **Be respectful** and inclusive in your language and actions
- **Be collaborative** and help others learn
- **Be constructive** when providing feedback
- **Focus on what is best** for the community and project

## 🚀 Getting Started

### Prerequisites

Before you begin, make sure you have:

- Python 3.8 or higher
- Git installed and configured
- Tesseract OCR installed
- Familiarity with the project structure (see [Architecture Guide](guidances/02-architecture-guide.md))

### First Time Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ocr_project.git
   cd ocr_project
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/ocr_project.git
   ```
4. **Follow the development setup** below

## 🛠️ Development Setup

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov pytest-mock black isort flake8 mypy pre-commit
```

### 2. Install Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Test pre-commit setup
pre-commit run --all-files
```

### 3. Verify Setup

```bash
# Run tests to ensure everything works
pytest tests/

# Test OCR functionality
python main.py --help
```

## 🔄 Contributing Workflow

### 1. Create a Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow our [coding standards](#coding-standards)
- Write tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit with conventional format
git commit -m "feat(classifiers): add support for new document type"
```

### 4. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

## 🎨 Coding Standards

### Code Style

We use these tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
black core/ tests/
isort core/ tests/

# Check linting
flake8 core/ tests/

# Type checking
mypy core/
```

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples:**
```
feat(classifiers): add support for Turkish passport classification
fix(validators): handle edge case in TC validation
docs(guides): update troubleshooting guide with new solutions
test(ocr): add comprehensive OCR accuracy tests
```

### Code Structure

- **Modules**: Keep modules focused and cohesive
- **Functions**: Single responsibility, clear names
- **Classes**: Follow SOLID principles
- **Documentation**: Use clear docstrings and comments

## 🧪 Testing Guidelines

### Test Types

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows

### Writing Tests

```python
import pytest
from core.validators import validate_tc_number

def test_valid_tc_number():
    """Test TC number validation with valid input."""
    result = validate_tc_number("12345678901")
    assert result is True

def test_invalid_tc_number():
    """Test TC number validation with invalid input."""
    result = validate_tc_number("invalid")
    assert result is False
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core

# Run specific test file
pytest tests/test_validators.py

# Run tests matching pattern
pytest -k "test_tc"
```

## 📚 Documentation

### Documentation Standards

- **Clear and concise** language
- **Practical examples** with code snippets
- **Up-to-date** information
- **Cross-references** to related sections

### Documentation Types

1. **Code Documentation**: Docstrings and inline comments
2. **User Guides**: In the `guidances/` directory
3. **API Reference**: Auto-generated from docstrings
4. **README**: Project overview and quick start

### Updating Documentation

When making changes:

- Update relevant docstrings
- Update user guides if functionality changes
- Add examples for new features
- Update the README if needed

## 📤 Submitting Changes

### Pull Request Process

1. **Follow the PR template** - Fill out all sections
2. **Link related issues** - Reference issue numbers
3. **Describe changes** - Clear description of what and why
4. **Test thoroughly** - Ensure all tests pass
5. **Update documentation** - Keep docs current

### PR Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation review** for completeness
5. **Final approval** and merge

### PR Guidelines

- **Small, focused PRs** are easier to review
- **Clear titles** and descriptions
- **Respond to feedback** promptly and professionally
- **Update your PR** if the main branch changes

## 📊 Types of Contributions

### 🐛 Bug Fixes

- Fix existing functionality
- Improve error handling
- Resolve performance issues

### ✨ New Features

- Document classification improvements
- New validation algorithms
- OCR accuracy enhancements
- Performance optimizations

### 📚 Documentation

- User guide improvements
- API documentation
- Code examples
- Troubleshooting guides

### 🧪 Testing

- Increase test coverage
- Add integration tests
- Performance benchmarks
- Edge case testing

## 🤝 Community

### Getting Help

- **Read the guides** in `guidances/` directory
- **Check existing issues** for similar problems
- **Ask questions** in GitHub Discussions
- **Join community** discussions

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community chat
- **Pull Requests**: Code review and collaboration

### Recognition

We appreciate all contributions! Contributors will be:

- **Acknowledged** in our contributors list
- **Credited** in release notes for significant contributions
- **Invited** to become maintainers for sustained contributions

## 🏷️ Issue Labels

Understanding our label system:

- **bug**: Something isn't working
- **enhancement**: New feature or request
- **documentation**: Improvements or additions to docs
- **good first issue**: Good for newcomers
- **help wanted**: Extra attention is needed
- **question**: Further information is requested

## 📈 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Cycle

- **Regular releases** every 2-4 weeks
- **Hotfix releases** for critical bugs
- **Beta releases** for major features

## 🙏 Thank You

Every contribution, no matter how small, helps make this project better. We're grateful for your time and effort in improving the OCR system for everyone.

---

## 📞 Contact

- **Maintainers**: [List of current maintainers]
- **Project Lead**: [Project lead contact]
- **Security Issues**: [Security contact information]

**Happy Contributing! 🎉**
