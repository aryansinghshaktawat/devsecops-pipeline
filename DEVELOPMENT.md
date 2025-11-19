# Development Guide

## Quick Start

### Prerequisites
- Python 3.9 or higher
- Git
- pip (Python package manager)

### Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/aryansinghshaktawat/devsecops-pipeline.git
   cd devsecops-pipeline
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install bandit pip-audit cyclonedx-bom
   ```

4. **Run the application**
   ```bash
   python src/app.py
   ```
   
   The API will be available at `http://localhost:5000`

5. **Run tests**
   ```bash
   pytest src/test_app.py -v --cov=src
   ```

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Get All Users
```bash
curl http://localhost:5000/api/users
```

### Get Specific User
```bash
curl http://localhost:5000/api/users/1
```

## Running Security Scans Locally

### SAST with Bandit
```bash
bandit -r src/ -f json -o bandit-report.json
```

### Secret Scanning with Gitleaks
```bash
# Install gitleaks first: https://github.com/gitleaks/gitleaks
gitleaks detect --source . --report-format json --report-path gitleaks-report.json
```

### Dependency Scanning with pip-audit
```bash
pip-audit --format json --output pip-audit.json
```

### Generate SBOM
```bash
cyclonedx-py -r --format json -o sbom.json
```

### Aggregate Reports
```bash
python tools/merge_reports.py
```

## Project Structure

```
devsecops-pipeline/
├── .github/
│   ├── workflows/
│   │   └── ci.yml              # GitHub Actions CI/CD pipeline
│   ├── ISSUE_TEMPLATE/         # Issue templates
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml          # Dependabot configuration
├── src/
│   ├── __init__.py
│   ├── app.py                  # Flask application
│   ├── utils.py                # Utility functions
│   └── test_app.py             # Unit tests
├── tools/
│   ├── __init__.py
│   └── merge_reports.py        # Security report aggregator
├── .gitignore
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml              # Project configuration
├── README.md
├── requirements.txt
└── SECURITY.md
```

## Testing

### Run All Tests
```bash
pytest src/test_app.py -v
```

### Run with Coverage
```bash
pytest src/test_app.py --cov=src --cov-report=term-missing --cov-report=html
```

### View Coverage Report
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Code Style

This project follows PEP 8 style guidelines. To check your code:

```bash
# Install flake8
pip install flake8

# Run linter
flake8 src/ --max-line-length=100
```

## Common Tasks

### Add a New Dependency
1. Add to `requirements.txt`
2. Update `pyproject.toml` dependencies
3. Run `pip install -r requirements.txt`
4. Test that everything works
5. Commit both files

### Add a New API Endpoint
1. Add route handler in `src/app.py`
2. Add tests in `src/test_app.py`
3. Update README documentation
4. Run tests to verify
5. Run security scans

### Debug Issues
```bash
# Run Flask in debug mode
export FLASK_ENV=development  # macOS/Linux
set FLASK_ENV=development     # Windows
python src/app.py
```

## Troubleshooting

### Virtual Environment Issues
```bash
# Remove old venv
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Create new venv
python -m venv venv
```

### Dependency Conflicts
```bash
# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Test Failures
```bash
# Run tests in verbose mode
pytest src/test_app.py -vv

# Run specific test
pytest src/test_app.py::test_home -v
```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [DevSecOps Best Practices](https://www.devsecops.org/)
