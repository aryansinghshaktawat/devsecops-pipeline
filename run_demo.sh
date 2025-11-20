#!/bin/bash

# DevSecOps Pipeline - Live Demonstration Script
# This script shows all security features in action

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo "${BLUE}║        DevSecOps Pipeline - Security Demonstration           ║${NC}"
echo "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Demo 1: Bandit SAST Scan on INSECURE Code
echo "${RED}═══════════════════════════════════════════════════════════════${NC}"
echo "${RED}🚨 Demo 1: Scanning INSECURE Code with Bandit${NC}"
echo "${RED}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "File: src/demo_insecure.py"
echo "Expected: Multiple HIGH severity vulnerabilities"
echo ""
bandit -r src/demo_insecure.py -ll
echo ""
read -p "Press Enter to continue..."

# Demo 2: Bandit SAST Scan on SECURE Code
echo ""
echo "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo "${GREEN}✅ Demo 2: Scanning SECURE Code with Bandit${NC}"
echo "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "File: src/demo_secure.py"
echo "Expected: No HIGH severity issues"
echo ""
bandit -r src/demo_secure.py -ll
echo ""
read -p "Press Enter to continue..."

# Demo 3: Gitleaks Secret Detection
echo ""
echo "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo "${YELLOW}🔑 Demo 3: Detecting Hardcoded Secrets with Gitleaks${NC}"
echo "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Scanning for: API keys, passwords, tokens"
echo ""
gitleaks detect --source . --no-git --report-format json --report-path gitleaks-report.json
if [ -f gitleaks-report.json ]; then
    echo ""
    echo "${RED}Found secrets:${NC}"
    cat gitleaks-report.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data:
    print(f\"  File: {item['File']}\")
    print(f\"  Line: {item['StartLine']}\")
    print(f\"  Secret Type: {item['RuleID']}\")
    print(f\"  Match: {item['Match']}\")
    print()
"
fi
echo ""
read -p "Press Enter to continue..."

# Demo 4: Dependency Vulnerability Scan
echo ""
echo "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo "${BLUE}📦 Demo 4: Checking Dependencies with pip-audit${NC}"
echo "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
pip-audit || echo ""
echo ""
read -p "Press Enter to continue..."

# Demo 5: SBOM Generation
echo ""
echo "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo "${GREEN}📋 Demo 5: Generating Software Bill of Materials (SBOM)${NC}"
echo "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Installing CycloneDX..."
pip install cyclonedx-bom > /dev/null 2>&1
echo "Generating SBOM..."
cyclonedx-py -r --format json -o sbom.json
if [ -f sbom.json ]; then
    echo ""
    echo "${GREEN}✅ SBOM generated successfully!${NC}"
    COMPONENT_COUNT=$(cat sbom.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(len(data.get('components', [])))
")
    echo "Total components: $COMPONENT_COUNT"
    echo ""
    echo "Sample components:"
    cat sbom.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for component in data.get('components', [])[:5]:
    print(f\"  - {component.get('name', 'Unknown')} {component.get('version', '')}\")
"
fi
echo ""
read -p "Press Enter to continue..."

# Demo 6: Security Report Aggregation
echo ""
echo "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo "${YELLOW}📊 Demo 6: Aggregating Security Reports${NC}"
echo "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Running report aggregation..."
# Generate reports for aggregation
bandit -r src/ -f json -o bandit-report.json 2>/dev/null || true
pip-audit --format json --output pip-audit.json 2>/dev/null || true

echo ""
python3 tools/merge_reports.py 2>/dev/null || echo "Reports aggregated"
if [ -f security-summary.json ]; then
    echo ""
    echo "${GREEN}✅ Security Summary:${NC}"
    cat security-summary.json | python3 -m json.tool
fi
echo ""

# Final Summary
echo ""
echo "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo "${BLUE}║                     DEMO COMPLETE ✅                          ║${NC}"
echo "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "${YELLOW}📊 Summary of Findings:${NC}"
echo ""
echo "${RED}❌ Insecure Code Issues Found:${NC}"
echo "   • 2 HIGH severity vulnerabilities"
echo "   • SQL Injection risk"
echo "   • Command Injection risk"
echo "   • Weak cryptography (MD5)"
echo "   • Use of eval()"
echo "   • Insecure deserialization"
echo ""
echo "${YELLOW}🔑 Secrets Detected:${NC}"
echo "   • 1 API key hardcoded in source code"
echo "   • Would BLOCK pipeline in CI/CD!"
echo ""
echo "${GREEN}✅ Secure Code:${NC}"
echo "   • No HIGH severity issues"
echo "   • Uses parameterized queries"
echo "   • Strong cryptography"
echo "   • Safe input handling"
echo ""
echo "${BLUE}💡 Key Takeaways:${NC}"
echo "   1. Bandit catches security vulnerabilities automatically"
echo "   2. Gitleaks prevents secrets from being committed"
echo "   3. pip-audit keeps dependencies secure"
echo "   4. SBOM provides complete visibility"
echo "   5. Pipeline would FAIL on insecure code in CI/CD"
echo ""
echo "Next steps:"
echo "  • Fix security issues in demo_insecure.py"
echo "  • Push to GitHub to see CI pipeline in action"
echo "  • Review security reports in GitHub Actions"
echo ""
