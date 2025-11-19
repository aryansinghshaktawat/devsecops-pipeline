#!/usr/bin/env python3
"""
Security Report Aggregation Script
Merges reports from multiple security scanning tools into a single summary
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

def load_json_report(file_path):
    """Load a JSON report file safely"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse {file_path}: {e}")
    except Exception as e:
        print(f"Warning: Error reading {file_path}: {e}")
    return None

def parse_bandit_report(bandit_data):
    """Parse Bandit SAST report"""
    if not bandit_data:
        return {"tool": "Bandit", "status": "no_report", "findings": []}
    
    results = bandit_data.get('results', [])
    findings = []
    
    for result in results:
        findings.append({
            "severity": result.get('issue_severity', 'UNKNOWN'),
            "confidence": result.get('issue_confidence', 'UNKNOWN'),
            "issue": result.get('issue_text', 'No description'),
            "file": result.get('filename', 'unknown'),
            "line": result.get('line_number', 0),
            "code": result.get('code', '')
        })
    
    metrics = bandit_data.get('metrics', {})
    total_issues = sum(metrics.get('_totals', {}).values())
    
    return {
        "tool": "Bandit",
        "status": "completed",
        "total_findings": len(findings),
        "severity_breakdown": {
            "HIGH": len([f for f in findings if f['severity'] == 'HIGH']),
            "MEDIUM": len([f for f in findings if f['severity'] == 'MEDIUM']),
            "LOW": len([f for f in findings if f['severity'] == 'LOW'])
        },
        "findings": findings
    }

def parse_gitleaks_report(gitleaks_data):
    """Parse Gitleaks secret scanning report"""
    if not gitleaks_data:
        return {"tool": "Gitleaks", "status": "no_report", "findings": []}
    
    findings = []
    
    if isinstance(gitleaks_data, list):
        for result in gitleaks_data:
            findings.append({
                "description": result.get('Description', 'Secret detected'),
                "file": result.get('File', 'unknown'),
                "line": result.get('StartLine', 0),
                "rule": result.get('RuleID', 'unknown'),
                "secret": result.get('Secret', '')[:20] + "..." if result.get('Secret') else ''
            })
    
    return {
        "tool": "Gitleaks",
        "status": "completed",
        "total_findings": len(findings),
        "findings": findings
    }

def parse_pip_audit_report(pip_audit_data):
    """Parse pip-audit vulnerability report"""
    if not pip_audit_data:
        return {"tool": "pip-audit", "status": "no_report", "findings": []}
    
    dependencies = pip_audit_data.get('dependencies', [])
    findings = []
    
    for dep in dependencies:
        vulnerabilities = dep.get('vulns', [])
        for vuln in vulnerabilities:
            findings.append({
                "package": dep.get('name', 'unknown'),
                "version": dep.get('version', 'unknown'),
                "vulnerability_id": vuln.get('id', 'unknown'),
                "description": vuln.get('description', 'No description'),
                "fix_versions": vuln.get('fix_versions', [])
            })
    
    return {
        "tool": "pip-audit",
        "status": "completed",
        "total_findings": len(findings),
        "findings": findings
    }

def parse_sbom(sbom_data):
    """Parse SBOM data"""
    if not sbom_data:
        return {"tool": "SBOM", "status": "no_report"}
    
    components = sbom_data.get('components', [])
    
    return {
        "tool": "SBOM (CycloneDX)",
        "status": "completed",
        "format": sbom_data.get('bomFormat', 'CycloneDX'),
        "spec_version": sbom_data.get('specVersion', 'unknown'),
        "total_components": len(components),
        "components": [
            {
                "name": comp.get('name', 'unknown'),
                "version": comp.get('version', 'unknown'),
                "type": comp.get('type', 'library')
            }
            for comp in components[:10]  # Limit to first 10 for summary
        ]
    }

def generate_summary(bandit_report, gitleaks_report, pip_audit_report, sbom_report):
    """Generate comprehensive security summary"""
    
    total_security_issues = (
        bandit_report.get('total_findings', 0) +
        gitleaks_report.get('total_findings', 0) +
        pip_audit_report.get('total_findings', 0)
    )
    
    critical_issues = []
    
    # Check for critical Bandit findings
    if bandit_report.get('severity_breakdown', {}).get('HIGH', 0) > 0:
        critical_issues.append({
            "tool": "Bandit",
            "issue": f"Found {bandit_report['severity_breakdown']['HIGH']} HIGH severity security issues"
        })
    
    # Check for secrets
    if gitleaks_report.get('total_findings', 0) > 0:
        critical_issues.append({
            "tool": "Gitleaks",
            "issue": f"Found {gitleaks_report['total_findings']} potential secrets in code"
        })
    
    # Check for vulnerable dependencies
    if pip_audit_report.get('total_findings', 0) > 0:
        critical_issues.append({
            "tool": "pip-audit",
            "issue": f"Found {pip_audit_report['total_findings']} vulnerable dependencies"
        })
    
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "pipeline_version": "1.0.0",
        "summary": {
            "total_security_issues": total_security_issues,
            "critical_issues_count": len(critical_issues),
            "status": "FAIL" if critical_issues else "PASS"
        },
        "critical_issues": critical_issues,
        "reports": {
            "bandit": bandit_report,
            "gitleaks": gitleaks_report,
            "pip_audit": pip_audit_report,
            "sbom": sbom_report
        }
    }

def main():
    """Main function to merge security reports"""
    print("🔍 Starting security report aggregation...")
    
    # Load reports
    bandit_data = load_json_report('bandit-report.json')
    gitleaks_data = load_json_report('gitleaks-report.json')
    pip_audit_data = load_json_report('pip-audit.json')
    sbom_data = load_json_report('sbom.json')
    
    # Parse reports
    print("📊 Parsing Bandit report...")
    bandit_report = parse_bandit_report(bandit_data)
    
    print("🔐 Parsing Gitleaks report...")
    gitleaks_report = parse_gitleaks_report(gitleaks_data)
    
    print("📦 Parsing pip-audit report...")
    pip_audit_report = parse_pip_audit_report(pip_audit_data)
    
    print("📋 Parsing SBOM...")
    sbom_report = parse_sbom(sbom_data)
    
    # Generate summary
    print("📝 Generating security summary...")
    summary = generate_summary(bandit_report, gitleaks_report, pip_audit_report, sbom_report)
    
    # Write output
    output_file = 'security-summary.json'
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Security summary generated: {output_file}")
    print(f"   Total security issues: {summary['summary']['total_security_issues']}")
    print(f"   Critical issues: {summary['summary']['critical_issues_count']}")
    print(f"   Overall status: {summary['summary']['status']}")
    
    return 0 if summary['summary']['status'] == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())
