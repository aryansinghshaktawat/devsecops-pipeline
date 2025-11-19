# DevSecOps Pipeline - Quick Reference

## 🚀 Quick Start

```bash
# Automated setup (recommended)
./quickstart.sh           # macOS/Linux
quickstart.bat            # Windows

# Manual setup
python3 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

## 🏃 Running the Application

```bash
python src/app.py
# Access at: http://localhost:5000
```

## 🧪 Testing

```bash
# Run all tests
pytest src/test_app.py -v

# With coverage
pytest src/test_app.py --cov=src --cov-report=term-missing
```

## 🔒 Security Scans

```bash
# SAST (Bandit)
bandit -r src/ -ll

# Secrets (Gitleaks)
gitleaks detect --source . --report-format json --report-path gitleaks-report.json

# Dependencies (pip-audit)
pip-audit

# SBOM (CycloneDX)
cyclonedx-py -r --format json -o sbom.json

# Aggregate all reports
python tools/merge_reports.py
```

## 📊 View Reports

```bash
# Security summary
cat security-summary.json | python -m json.tool

# Individual reports
cat bandit-report.json | python -m json.tool
cat gitleaks-report.json | python -m json.tool
cat pip-audit.json | python -m json.tool
cat sbom.json | python -m json.tool
```

## 🌐 API Endpoints

```bash
# Home
curl http://localhost:5000/

# Health check
curl http://localhost:5000/api/health

# Get all users
curl http://localhost:5000/api/users

# Get specific user
curl http://localhost:5000/api/users/1
```

## 📝 Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, then
git add .
git commit -m "feat: description"
git push origin feature/my-feature

# Create PR on GitHub
# Pipeline runs automatically
```

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements.txt` |
| Tests fail | `pytest src/test_app.py -vv` |
| Import errors | `deactivate && rm -rf venv && python3 -m venv venv` |
| HIGH severity | Check `bandit-report.json` and fix issues |
| Secrets detected | Remove secrets, use environment variables |

## 📚 Full Documentation

- **[USAGE.md](USAGE.md)** - Complete usage guide
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[SECURITY.md](SECURITY.md)** - Security policy

## 🛠️ Development Tools

```bash
# Code style check
pip install flake8
flake8 src/ --max-line-length=100

# Security tools
pip install bandit pip-audit cyclonedx-bom

# All dev dependencies
pip install -e ".[dev]"  # if using pyproject.toml
```

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project metadata & config |
| `.github/workflows/ci.yml` | CI/CD pipeline |
| `.github/dependabot.yml` | Auto dependency updates |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Ignored files |

## 📦 Project Structure

```
devsecops-pipeline/
├── .github/          # GitHub configs & workflows
├── src/              # Application code
│   ├── app.py        # Flask API
│   ├── utils.py      # Utilities
│   └── test_app.py   # Tests
├── tools/            # Security scripts
│   └── merge_reports.py
├── requirements.txt  # Dependencies
└── *.md             # Documentation
```

## 🎯 Pipeline Triggers

- ✅ Push to `main` or `develop`
- ✅ Pull requests to `main`
- ✅ Manual trigger (Actions tab)

## ⚠️ Pipeline Failure Conditions

- ❌ HIGH severity issues in Bandit
- ❌ Secrets detected by Gitleaks
- ⚠️ Vulnerable dependencies (warning only)

## 💡 Pro Tips

1. **Run scans before pushing**: `bandit -r src/ && pip-audit`
2. **Use virtual environments**: Always activate venv
3. **Check pipeline status**: Monitor GitHub Actions tab
4. **Update dependencies**: Review Dependabot PRs weekly
5. **Read security summary**: `cat security-summary.json | python -m json.tool`

## 📞 Get Help

- 📖 Read [USAGE.md](USAGE.md) for detailed instructions
- 🐛 [Open an issue](https://github.com/aryansinghshaktawat/devsecops-pipeline/issues)
- 📧 Email: aryansinghshaktawat@example.com

---

**For complete documentation, see [USAGE.md](USAGE.md)**
