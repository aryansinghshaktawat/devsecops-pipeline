#!/bin/bash

# Quick Start Script for DevSecOps Pipeline
# This script sets up the development environment

set -e

echo "🚀 DevSecOps Pipeline - Quick Start"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version found"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📚 Installing project dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Install development tools
echo "🛠️  Installing development tools..."
pip install bandit pip-audit cyclonedx-bom flake8 --quiet
echo "✅ Development tools installed"
echo ""

# Run tests
echo "🧪 Running tests..."
pytest src/test_app.py -v --cov=src
echo ""

# Run security scans
echo "🔒 Running security scans..."
echo ""
echo "  Running Bandit (SAST)..."
bandit -r src/ -ll || true
echo ""
echo "  Running pip-audit..."
pip-audit || true
echo ""

# Generate SBOM
echo "📋 Generating SBOM..."
cyclonedx-py requirements requirements.txt --output-format JSON --output-file sbom.json
echo "✅ SBOM generated: sbom.json"
echo ""

# Start application
echo "🎉 Setup complete!"
echo ""
echo "📖 Next steps:"
echo "   1. Activate the virtual environment: source venv/bin/activate"
echo "   2. Run the application: python src/app.py"
echo "   3. Access the API: http://localhost:5000"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Project overview"
echo "   - DEVELOPMENT.md - Development guide"
echo "   - CONTRIBUTING.md - How to contribute"
echo ""
echo "Happy coding! 🚀"
