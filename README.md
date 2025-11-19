# DevSecOps CI Pipeline

[![DevSecOps CI Pipeline](https://github.com/aryansinghshaktawat/devsecops-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/aryansinghshaktawat/devsecops-pipeline/actions/workflows/ci.yml)

A comprehensive DevSecOps pipeline demonstrating automated security scanning, SBOM generation, and policy enforcement using GitHub Actions.

## Overview

This project implements a production-ready DevSecOps pipeline that includes:
- **SAST (Static Application Security Testing)** with Bandit
- **Secret Scanning** with Gitleaks
- **Dependency Vulnerability Scanning** with pip-audit
- **SBOM Generation** with CycloneDX
- **Automated Dependency Updates** with Dependabot
- **Security Report Aggregation**
- **Policy-based Failure Conditions**

## Project Structure

```
devsecops-pipeline/
├── .github/
│   ├── workflows/
│   │   └── ci.yml           # Main CI/CD pipeline
│   └── dependabot.yml        # Dependabot configuration
├── src/                      # Python application code
├── tools/                    # Security tooling scripts
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Stack

- **CI/CD**: GitHub Actions
- **SAST**: Bandit (Python security scanner)
- **Secret Scanning**: Gitleaks
- **Dependency Scanning**: pip-audit, Dependabot
- **SBOM**: CycloneDX
- **Language**: Python 3.x

## Pipeline Architecture

The DevSecOps pipeline runs automatically on every push and pull request. It consists of multiple parallel security scanning jobs followed by report aggregation:

```
┌─────────────┐
│  Git Push   │
└──────┬──────┘
       │
       ├─────────────────┬─────────────────┬─────────────────┬──────────────┐
       ▼                 ▼                 ▼                 ▼              ▼
┌──────────┐     ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  ┌──────┐
│  Tests   │     │ Bandit SAST  │  │  Gitleaks    │  │  pip-audit  │  │ SBOM │
└──────────┘     └──────┬───────┘  └──────┬───────┘  └──────┬──────┘  └───┬──┘
                        │                  │                  │             │
                        └──────────────────┴──────────────────┴─────────────┘
                                           │
                                           ▼
                                ┌──────────────────────┐
                                │  Aggregate Reports   │
                                │  Policy Enforcement  │
                                └──────────────────────┘
```

### Pipeline Stages

1. **Test**: Runs unit tests with pytest and coverage reporting
2. **SAST (Bandit)**: Scans Python code for security vulnerabilities
3. **Secret Scanning (Gitleaks)**: Detects hardcoded secrets and credentials
4. **Dependency Scanning (pip-audit)**: Identifies vulnerable dependencies
5. **SBOM Generation**: Creates a Software Bill of Materials
6. **Report Aggregation**: Merges all security reports into a comprehensive summary

## Security Tools

### Bandit (SAST)
Bandit analyzes Python code to find common security issues such as:
- Use of insecure functions
- SQL injection vulnerabilities
- Hard-coded credentials
- Weak cryptographic practices

**Severity Levels**: LOW, MEDIUM, HIGH  
**Policy**: Pipeline fails if HIGH severity issues are detected

### Gitleaks (Secret Scanning)
Gitleaks scans the entire repository history for exposed secrets:
- API keys and tokens
- Passwords and credentials
- Private keys
- AWS keys and other cloud credentials

**Policy**: Pipeline fails if any secrets are detected

### pip-audit (Dependency Scanning)
Checks Python dependencies against known vulnerability databases:
- CVE database
- GitHub Security Advisories
- PyPI security advisories

**Policy**: Logs warnings for vulnerable dependencies (can be configured to fail)

### CycloneDX (SBOM)
Generates a complete Software Bill of Materials including:
- All direct and transitive dependencies
- Component versions and licenses
- Dependency relationships

## Running Locally

### Prerequisites
```bash
# Python 3.11+
python --version

# Install dependencies
pip install -r requirements.txt
```

### Run Tests
```bash
pytest src/test_app.py -v --cov=src
```

### Run Security Scans

**Bandit (SAST):**
```bash
pip install bandit[toml]
bandit -r src/ -f json -o bandit-report.json
```

**Gitleaks (Secret Scanning):**
```bash
# Install Gitleaks
# macOS
brew install gitleaks

# Linux
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.1/gitleaks_8.18.1_linux_x64.tar.gz
tar -xzf gitleaks_8.18.1_linux_x64.tar.gz

# Run scan
gitleaks detect --source . --report-format json --report-path gitleaks-report.json
```

**pip-audit (Dependency Scan):**
```bash
pip install pip-audit
pip-audit --format json --output pip-audit.json
```

**SBOM Generation:**
```bash
pip install cyclonedx-bom
cyclonedx-py -r --format json -o sbom.json
```

### Aggregate Reports
```bash
python tools/merge_reports.py
```

## Reading Security Reports

### Bandit Report Structure
```json
{
  "results": [
    {
      "issue_severity": "HIGH",
      "issue_confidence": "HIGH",
      "issue_text": "Description of the issue",
      "filename": "src/app.py",
      "line_number": 42,
      "code": "vulnerable code snippet"
    }
  ]
}
```

### Gitleaks Report Structure
```json
[
  {
    "Description": "Secret type detected",
    "File": "config.py",
    "StartLine": 10,
    "RuleID": "generic-api-key",
    "Secret": "exposed-secret-value"
  }
]
```

### Security Summary Structure
```json
{
  "summary": {
    "total_security_issues": 5,
    "critical_issues_count": 2,
    "status": "FAIL"
  },
  "critical_issues": [...],
  "reports": {
    "bandit": {...},
    "gitleaks": {...},
    "pip_audit": {...},
    "sbom": {...}
  }
}
```

## CI/CD Artifacts

Each pipeline run produces the following artifacts:
- `bandit-report.json` - SAST scan results
- `gitleaks-report.json` - Secret scanning results
- `pip-audit.json` - Dependency vulnerability results
- `sbom.json` - Software Bill of Materials
- `security-summary.json` - Aggregated security report

Access artifacts from the GitHub Actions "Summary" page for each workflow run.

## Extending the Pipeline

### Adding New Security Tools

1. **Add tool installation** in `.github/workflows/ci.yml`:
```yaml
- name: Install new-tool
  run: |
    pip install new-tool
```

2. **Add scan step**:
```yaml
- name: Run new-tool scan
  run: |
    new-tool scan --output report.json
```

3. **Update merge_reports.py** to parse the new tool's output

### Customizing Policy Rules

Edit `.github/workflows/ci.yml` to adjust failure conditions:

```yaml
# Example: Fail on MEDIUM or higher severity
if [ "$MEDIUM_COUNT" -gt "0" ] || [ "$HIGH_COUNT" -gt "0" ]; then
  exit 1
fi
```

### Adding Custom Checks

Create additional jobs in the workflow:
```yaml
custom-check:
  name: Custom Security Check
  runs-on: ubuntu-latest
  steps:
    - name: Run custom check
      run: |
        # Your custom security checks
```

## Dependabot Configuration

Dependabot automatically creates pull requests for:
- **Python dependencies**: Weekly updates for pip packages
- **GitHub Actions**: Weekly updates for action versions

Configure in `.github/dependabot.yml`:
```yaml
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Best Practices

1. **Review Security Reports**: Always check security-summary.json after each run
2. **Fix HIGH Severity Issues**: Address high-severity findings immediately
3. **Rotate Secrets**: If Gitleaks detects secrets, rotate them immediately
4. **Update Dependencies**: Keep dependencies up-to-date to avoid vulnerabilities
5. **Run Locally**: Test security scans before pushing to catch issues early
6. **Monitor SBOM**: Regularly review your SBOM for supply chain risks

## Troubleshooting

### Pipeline Fails on Bandit Check
- Review `bandit-report.json` artifact
- Fix HIGH severity issues in the code
- Re-run the pipeline

### Gitleaks Detects False Positives
- Add exceptions to `.gitleaksignore` file
- Use inline comments to suppress specific findings

### pip-audit Finds Vulnerabilities
- Update dependencies: `pip install --upgrade package-name`
- Check for available patches or workarounds
- Document accepted risks if no fix is available

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all security scans pass
5. Submit a pull request

## License

This project is provided as-is for educational and demonstration purposes.

## Resources

- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [pip-audit Documentation](https://pypi.org/project/pip-audit/)
- [CycloneDX Documentation](https://cyclonedx.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OWASP DevSecOps Guidelines](https://owasp.org/www-project-devsecops-guideline/)

