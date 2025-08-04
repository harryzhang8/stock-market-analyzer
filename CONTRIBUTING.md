# Contributing to Stock Market Analyzer

First off, thank you for considering contributing to Stock Market Analyzer! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots if applicable**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Steps

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-market-analyzer.git
   cd stock-market-analyzer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Run tests to ensure everything works**
   ```bash
   pytest
   ```

## Coding Standards

### Python Code Style
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maximum line length: 88 characters (Black formatter standard)

### Code Formatting
We use several tools to maintain code quality:

```bash
# Format code with Black
black stock_analyzer.py

# Check code style with flake8
flake8 stock_analyzer.py

# Type checking with mypy
mypy stock_analyzer.py
```

### Documentation
- Use Google-style docstrings
- Update README.md if you change functionality
- Comment complex algorithms and business logic

Example docstring:
```python
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI) for a price series.
    
    Args:
        prices: Series of closing prices
        period: Number of periods for RSI calculation (default: 14)
        
    Returns:
        Series of RSI values (0-100 scale)
        
    Raises:
        ValueError: If period is less than 1
    """
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=stock_analyzer

# Run specific test file
pytest tests/test_indicators.py
```

### Writing Tests
- Write unit tests for new functions
- Test edge cases and error conditions
- Use descriptive test names
- Mock external API calls

Example test:
```python
def test_calculate_rsi_normal_case():
    """Test RSI calculation with normal price data."""
    prices = pd.Series([100, 102, 101, 103, 105, 104, 106])
    rsi = calculate_rsi(prices, period=6)
    
    assert isinstance(rsi, pd.Series)
    assert 0 <= rsi.iloc[-1] <= 100
```

## Commit Messages

Use clear and meaningful commit messages:

```
feat: add support for custom time periods
fix: resolve RSI calculation bug for small datasets
docs: update README with new installation instructions
test: add unit tests for MACD indicator
refactor: improve code organization in StockAnalyzer class
```

## Branch Naming

Use descriptive branch names:
- `feature/add-new-indicator`
- `bugfix/fix-rsi-calculation`
- `docs/update-readme`
- `refactor/improve-code-structure`

## Pull Request Process

1. **Update documentation** if you change functionality
2. **Add tests** for new features
3. **Ensure all tests pass** locally before submitting
4. **Update the README.md** with details of changes if applicable
5. **Request review** from maintainers

### Pull Request Template
When creating a PR, please include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

## Development Environment

### Recommended Tools
- **IDE**: VS Code, PyCharm, or similar
- **Python**: 3.8+ (use pyenv for version management)
- **Git**: Latest version
- **Terminal**: With good Python support

### VS Code Extensions
If using VS Code, these extensions are helpful:
- Python
- Pylance
- GitLens
- Black Formatter
- autoDocstring

## Questions?

Don't hesitate to ask questions! You can:
- Open an issue for discussion
- Contact maintainers directly
- Check existing issues and PRs for similar questions

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes for their contributions
- Special thanks for significant contributions

Thank you for contributing to Stock Market Analyzer! 🚀