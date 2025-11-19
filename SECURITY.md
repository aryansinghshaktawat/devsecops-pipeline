# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of our project seriously. If you have discovered a security vulnerability, we appreciate your help in disclosing it to us in a responsible manner.

### Please DO NOT:
- Open a public GitHub issue for security vulnerabilities
- Publicly disclose the vulnerability before it has been addressed

### Please DO:

**Option 1: GitHub Security Advisories (Recommended)**
1. Go to the [Security Advisories page](https://github.com/aryansinghshaktawat/devsecops-pipeline/security/advisories)
2. Click "Report a vulnerability"
3. Fill out the form with details about the vulnerability

**Option 2: Email**
Send an email to: **aryansinghshaktawat@example.com**

Include the following information:
- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability, including how an attacker might exploit it

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Investigation**: We will investigate and validate the vulnerability within 5 business days
- **Communication**: We will keep you informed about our progress
- **Fix**: We will work on a fix and release it as soon as possible
- **Credit**: We will credit you in the security advisory (unless you prefer to remain anonymous)

### Security Update Process

1. Security vulnerability is reported and confirmed
2. A fix is prepared in a private repository
3. A security advisory is drafted
4. The fix is released and the advisory is published
5. Users are notified through GitHub releases and security advisories

## Security Best Practices for Users

### When Using This Project:

1. **Keep Dependencies Updated**
   - Regularly run `pip install --upgrade -r requirements.txt`
   - Monitor Dependabot alerts
   - Review and merge security updates promptly

2. **Run Security Scans Locally**
   ```bash
   # SAST scanning
   pip install bandit
   bandit -r src/
   
   # Dependency scanning
   pip install pip-audit
   pip-audit
   
   # Secret scanning
   # Install gitleaks from https://github.com/gitleaks/gitleaks
   gitleaks detect --source .
   ```

3. **Environment Security**
   - Never commit secrets, API keys, or credentials
   - Use environment variables for sensitive data
   - Keep your `.env` files in `.gitignore`
   - Use secrets management tools in production

4. **CI/CD Security**
   - Review GitHub Actions workflows for security
   - Use pinned versions for actions (with SHA)
   - Protect sensitive branches
   - Enable required status checks

5. **Code Review**
   - Review all dependencies before adding them
   - Check for known vulnerabilities in dependencies
   - Review code changes for security implications
   - Use the security checklist in PR template

## Security Features in This Project

This project includes several security measures:

- ✅ **SAST Scanning**: Bandit analyzes code for security issues
- ✅ **Secret Scanning**: Gitleaks detects hardcoded secrets
- ✅ **Dependency Scanning**: pip-audit checks for vulnerable packages
- ✅ **SBOM Generation**: Track all dependencies
- ✅ **Automated Updates**: Dependabot keeps dependencies current
- ✅ **Policy Enforcement**: Pipeline fails on critical security issues

## Known Security Considerations

### Current Limitations:
- This is a demonstration project and should not be used in production without proper security review
- The sample Flask application does not include authentication or authorization
- The application should not be exposed to the internet without additional security measures

### Production Recommendations:
- Implement proper authentication and authorization
- Use HTTPS/TLS for all communications
- Implement rate limiting and input validation
- Use a Web Application Firewall (WAF)
- Implement proper logging and monitoring
- Follow OWASP security guidelines
- Conduct regular security audits

## Security Hall of Fame

We appreciate the following individuals who have responsibly disclosed security issues:

<!-- Names will be added here as security researchers help improve our project -->

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)

## Questions?

If you have questions about this security policy, please open an issue with the label `security-question`.

---

**Last Updated**: November 2025
