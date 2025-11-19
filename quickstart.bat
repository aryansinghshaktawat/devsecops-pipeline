@echo off
REM Quick Start Script for DevSecOps Pipeline (Windows)
REM This script sets up the development environment

echo.
echo DevSecOps Pipeline - Quick Start
echo ====================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9 or higher.
    exit /b 1
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo pip upgraded
echo.

REM Install dependencies
echo Installing project dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed
echo.

REM Install development tools
echo Installing development tools...
pip install bandit pip-audit cyclonedx-bom --quiet
echo Development tools installed
echo.

REM Run tests
echo Running tests...
pytest src/test_app.py -v --cov=src
echo.

REM Run security scans
echo Running security scans...
echo.
echo   Running Bandit (SAST)...
bandit -r src/ -ll
echo.
echo   Running pip-audit...
pip-audit
echo.

REM Generate SBOM
echo Generating SBOM...
cyclonedx-py -r --format json -o sbom.json
echo SBOM generated: sbom.json
echo.

REM Complete
echo.
echo Setup complete!
echo.
echo Next steps:
echo    1. Activate the virtual environment: venv\Scripts\activate.bat
echo    2. Run the application: python src/app.py
echo    3. Access the API: http://localhost:5000
echo.
echo Documentation:
echo    - README.md - Project overview
echo    - DEVELOPMENT.md - Development guide
echo    - CONTRIBUTING.md - How to contribute
echo.
echo Happy coding!
pause
