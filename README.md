# GTO (Git-based Tracking of Data Changes)

GTO is a Python package for tracking and managing data changes in Git repositories. It provides tools for:
- Data change detection and tracking
- Performance benchmarking
- Code optimization
- Documentation generation

## Features

- **Data Tracking**: Monitor and track changes in your data files
- **Benchmarking**: Compare performance across different frameworks
- **Code Optimization**: Automatically optimize code for better performance
- **Documentation**: Generate comprehensive documentation

## Installation

### For Users

```bash
pip install gto
```

### For Developers

```bash
# Clone the repository
git clone https://github.com/sdevisch/gto.git
cd gto

# Install in development mode with all dev dependencies
pip install -e ".[dev]"
```

## Quick Start

1. Initialize GTO in your project:
```python
from gto import GTO
gto = GTO()
```

2. Track data changes:
```python
gto.track_data("data.csv")
```

3. Generate documentation:
```python
gto.generate_docs()
```

## Development

### Running Tests

```bash
# Run tests with coverage
pytest --cov=src tests/ -v

# Run specific test file
pytest tests/test_hash_utils.py -v
```

### Code Style

We use:
- black for code formatting
- isort for import sorting
- mypy for type checking
- flake8 for linting

```bash
# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

## Documentation

For detailed documentation, see the [docs](docs/build/html/index.html) directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## License

MIT License 