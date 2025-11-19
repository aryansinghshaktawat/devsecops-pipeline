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
