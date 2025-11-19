# Usage Guide - DevSecOps Pipeline

This guide explains how to use the DevSecOps CI/CD pipeline in your project.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Running Locally](#running-locally)
3. [Understanding the Pipeline](#understanding-the-pipeline)
4. [Using Security Tools](#using-security-tools)
5. [Viewing Reports](#viewing-reports)
6. [Common Workflows](#common-workflows)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- **Python 3.9+** installed
- **Git** installed
- **GitHub account** (for CI/CD)

### Quick Setup

#### Option 1: Using Quick Start Script (Recommended)

**On macOS/Linux:**
```bash
./quickstart.sh
```

**On Windows:**
```cmd
quickstart.bat
```

This script will:
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Run tests
- ✅ Execute security scans
- ✅ Generate SBOM

#### Option 2: Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/aryansinghshaktawat/devsecops-pipeline.git
cd devsecops-pipeline

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install security tools
pip install bandit pip-audit cyclonedx-bom
```

---

## Running Locally

### Start the Application

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run the Flask application
python src/app.py
```

The API will be available at: **http://localhost:5000**

### Test the API

#### Home Endpoint
```bash
curl http://localhost:5000/
```

**Expected Response:**
```json
{
  "message": "Welcome to DevSecOps Pipeline Demo",
  "version": "1.0.0",
  "status": "healthy"
}
```

#### Health Check
```bash
curl http://localhost:5000/api/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "service": "devsecops-demo"
}
```

#### Get All Users
```bash
curl http://localhost:5000/api/users
```

#### Get Specific User
```bash
curl http://localhost:5000/api/users/1
```

### Run Tests

```bash
# Run all tests
pytest src/test_app.py -v

# Run with coverage
pytest src/test_app.py -v --cov=src --cov-report=term-missing

# Run specific test
pytest src/test_app.py::test_home -v

# Generate HTML coverage report
pytest src/test_app.py --cov=src --cov-report=html
open htmlcov/index.html  # View in browser
```

---

## Understanding the Pipeline

### Pipeline Flow

```
┌─────────────────┐
│   Git Push      │
│   to main       │
└────────┬────────┘
         │
         ├──────────────┬─────────────────┬──────────────────┬─────────────────┐
         │              │                 │                  │                 │
    ┌────▼────┐   ┌────▼─────┐    ┌─────▼──────┐    ┌──────▼──────┐   ┌─────▼──────┐
    │  Tests  │   │  Bandit  │    │  Gitleaks  │    │  pip-audit  │   │    SBOM    │
    │         │   │  (SAST)  │    │ (Secrets)  │    │   (Deps)    │   │ Generation │
    └────┬────┘   └────┬─────┘    └─────┬──────┘    └──────┬──────┘   └─────┬──────┘
         │              │                 │                  │                 │
         └──────────────┴─────────────────┴──────────────────┴─────────────────┘
                                          │
                                    ┌─────▼──────┐
                                    │  Aggregate │
                                    │  Reports   │
                                    └─────┬──────┘
                                          │
                                    ┌─────▼──────┐
                                    │   Policy   │
                                    │   Check    │
                                    └────────────┘
```

### When the Pipeline Runs

The CI/CD pipeline automatically runs on:
- ✅ Push to `main` branch
- ✅ Push to `develop` branch
- ✅ Pull requests to `main` branch
- ✅ Manual trigger (workflow_dispatch)

### What Each Job Does

#### 1. **Test Job**
- Checks out code
- Sets up Python 3.11
- Installs dependencies
- Runs pytest with coverage

#### 2. **Security SAST (Bandit)**
- Scans Python code for security issues
- Generates JSON report
- **FAILS** if HIGH severity issues found
- Uploads `bandit-report.json` artifact

#### 3. **Secret Scanning (Gitleaks)**
- Scans repository for hardcoded secrets
- Checks API keys, passwords, tokens
- **FAILS** if secrets detected
- Uploads `gitleaks-report.json` artifact

#### 4. **Dependency Scan (pip-audit)**
- Checks dependencies for known vulnerabilities
- Uses National Vulnerability Database
- Warns about vulnerable packages
- Uploads `pip-audit.json` artifact

#### 5. **SBOM Generation**
- Creates Software Bill of Materials
- Lists all dependencies and versions
- Uses CycloneDX format
- Uploads `sbom.json` artifact

#### 6. **Aggregate Reports**
- Downloads all security reports
- Merges into single summary
- Creates `security-summary.json`
- Displays consolidated findings

---

## Using Security Tools

### 1. Bandit (SAST Scanner)

**Run Basic Scan:**
```bash
bandit -r src/
```

**Generate JSON Report:**
```bash
bandit -r src/ -f json -o bandit-report.json
```

**Filter by Severity:**
```bash
# Only HIGH and MEDIUM
bandit -r src/ -ll

# Only HIGH
bandit -r src/ -lll
```

**Common Issues Detected:**
- Hardcoded passwords
- SQL injection vulnerabilities
- Use of `exec()` or `eval()`
- Insecure cryptographic practices
- Path traversal vulnerabilities

### 2. Gitleaks (Secret Scanner)

**First, install Gitleaks:**
```bash
# macOS
brew install gitleaks

# Linux
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.1/gitleaks_8.18.1_linux_x64.tar.gz
tar -xzf gitleaks_8.18.1_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/

# Windows
# Download from: https://github.com/gitleaks/gitleaks/releases
```

**Run Scan:**
```bash
# Scan current repository
gitleaks detect --source . --report-format json --report-path gitleaks-report.json

# Scan with verbose output
gitleaks detect --source . -v

# Scan specific commit
gitleaks detect --source . --log-opts="HEAD^..HEAD"
```

**Common Secrets Detected:**
- AWS access keys
- API tokens
- Private keys
- Database passwords
- OAuth secrets

### 3. pip-audit (Dependency Scanner)

**Run Basic Audit:**
```bash
pip-audit
```

**Generate JSON Report:**
```bash
pip-audit --format json --output pip-audit.json
```

**Fix Vulnerabilities:**
```bash
# Show fixes
pip-audit --fix --dry-run

# Apply fixes (upgrades packages)
pip-audit --fix
```

**Audit Specific Requirements File:**
```bash
pip-audit -r requirements.txt
```

### 4. CycloneDX (SBOM Generator)

**Generate SBOM:**
```bash
# JSON format (recommended)
cyclonedx-py -r --format json -o sbom.json

# XML format
cyclonedx-py -r --format xml -o sbom.xml

# Include dev dependencies
cyclonedx-py -r --format json -o sbom-dev.json
```

**View SBOM:**
```bash
# Pretty print JSON
cat sbom.json | python -m json.tool

# Count dependencies
cat sbom.json | python -c "import sys, json; data=json.load(sys.stdin); print(f'Total dependencies: {len(data.get(\"components\", []))}')"
```

### 5. Aggregate Security Reports

**Run the aggregation script:**
```bash
python tools/merge_reports.py
```

This creates `security-summary.json` with:
- Total issue count
- Breakdown by tool
- Severity distribution
- Timestamp
- SBOM component count

**View Summary:**
```bash
cat security-summary.json | python -m json.tool
```

---

## Viewing Reports

### In GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Click on a workflow run
4. Scroll to **Artifacts** section
5. Download reports:
   - `bandit-report`
   - `gitleaks-report`
   - `pip-audit-report`
   - `sbom`
   - `security-summary`

### Locally

After running security scans, reports are in the root directory:

```bash
# View Bandit report
cat bandit-report.json | python -m json.tool

# View Gitleaks report
cat gitleaks-report.json | python -m json.tool

# View pip-audit report
cat pip-audit.json | python -m json.tool

# View SBOM
cat sbom.json | python -m json.tool

# View security summary
cat security-summary.json | python -m json.tool
```

---

## Common Workflows

### Workflow 1: Adding New Code

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make your changes
# Edit files...

# 3. Run tests locally
pytest src/test_app.py -v

# 4. Run security scans
bandit -r src/ -ll
pip-audit

# 5. Commit changes
git add .
git commit -m "feat: add new feature"

# 6. Push and create PR
git push origin feature/new-feature
# Create pull request on GitHub

# 7. Pipeline runs automatically
# Review pipeline results in PR

# 8. Fix any issues found
# Update code and push again

# 9. Merge PR when pipeline passes
```

### Workflow 2: Fixing Security Issues

```bash
# 1. Check security summary
cat security-summary.json | python -m json.tool

# 2. Review specific report (e.g., Bandit)
cat bandit-report.json | python -m json.tool

# 3. Fix the issue in code
# Edit affected files...

# 4. Re-run scan to verify fix
bandit -r src/ -ll

# 5. Run all tests
pytest src/test_app.py -v

# 6. Commit and push
git add .
git commit -m "fix: resolve HIGH severity security issue"
git push
```

### Workflow 3: Updating Dependencies

```bash
# 1. Check for vulnerabilities
pip-audit

# 2. Update specific package
pip install --upgrade package-name

# 3. Update requirements.txt
pip freeze > requirements.txt

# 4. Test application
pytest src/test_app.py -v

# 5. Re-run security audit
pip-audit

# 6. Commit changes
git add requirements.txt
git commit -m "deps: update package-name to fix vulnerability"
git push
```

### Workflow 4: Reviewing Dependabot PRs

1. Dependabot creates PR for dependency update
2. Review the PR description
3. Check which vulnerability it fixes
4. Review the changelog of updated package
5. Wait for CI pipeline to complete
6. If tests pass, merge the PR
7. If tests fail, investigate and fix

---

## Troubleshooting

### Pipeline Failing on Bandit

**Problem:** HIGH severity issues detected

**Solution:**
```bash
# View detailed report
bandit -r src/ -f json -o bandit-report.json
cat bandit-report.json | python -m json.tool

# Fix the code based on recommendations
# Common fixes:
# - Remove hardcoded passwords
# - Use parameterized queries for SQL
# - Avoid eval() and exec()
# - Use secure random number generators
```

### Pipeline Failing on Gitleaks

**Problem:** Secrets detected in code

**Solution:**
```bash
# View what was detected
cat gitleaks-report.json | python -m json.tool

# Remove secrets from code
# Use environment variables instead:
# BAD:  api_key = "sk-12345"
# GOOD: api_key = os.getenv('API_KEY')

# Remove from git history if already committed:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all
```

### Dependency Vulnerabilities

**Problem:** pip-audit finds vulnerable packages

**Solution:**
```bash
# Check for available updates
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Or update requirements.txt to specific version
# Example: flask>=2.3.3

# Re-run audit
pip-audit
```

### Virtual Environment Issues

**Problem:** Import errors or module not found

**Solution:**
```bash
# Deactivate current environment
deactivate

# Remove venv
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Create fresh environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Tests Failing

**Problem:** Tests not passing

**Solution:**
```bash
# Run tests with verbose output
pytest src/test_app.py -vv

# Run specific failing test
pytest src/test_app.py::test_name -vv

# Check for import errors
python -c "import src.app; print('OK')"

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## Advanced Usage

### Running Specific Pipeline Jobs Locally

**Simulate the test job:**
```bash
pip install -r requirements.txt
pytest src/test_app.py -v --cov=src --cov-report=term-missing
```

**Simulate security-sast job:**
```bash
pip install bandit[toml]
bandit -r src/ -f json -o bandit-report.json
```

**Simulate secret-scanning job:**
```bash
gitleaks detect --source . --report-format json --report-path gitleaks-report.json
```

**Simulate dependency-scan job:**
```bash
pip install -r requirements.txt
pip install pip-audit
pip-audit --format json --output pip-audit.json
```

**Simulate sbom-generation job:**
```bash
pip install -r requirements.txt
pip install cyclonedx-bom
cyclonedx-py -r --format json -o sbom.json
```

**Simulate aggregate-reports job:**
```bash
python tools/merge_reports.py
cat security-summary.json | python -m json.tool
```

### Customizing the Pipeline

Edit `.github/workflows/ci.yml` to:
- Add more security tools
- Change Python version
- Modify failure conditions
- Add deployment steps
- Configure notifications

---

## Getting Help

- 📖 [README.md](README.md) - Project overview
- 🛠️ [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- 🔒 [SECURITY.md](SECURITY.md) - Security policy
- 📝 [CHANGELOG.md](CHANGELOG.md) - Version history

**Need more help?**
- Open an issue: https://github.com/aryansinghshaktawat/devsecops-pipeline/issues
- Check existing issues for similar problems
- Contact: aryansinghshaktawat@example.com

---

**Happy DevSecOps! 🚀🔒**
