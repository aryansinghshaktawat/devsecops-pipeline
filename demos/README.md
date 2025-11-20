# Demo Files - Security Testing Examples

## ⚠️ Important Notice

The files in this directory contain **intentional security vulnerabilities** for demonstration and educational purposes.

## 📁 Files

### `demo_insecure.py`
Contains examples of **insecure code** including:
- ❌ SQL Injection vulnerabilities
- ❌ Command Injection vulnerabilities
- ❌ Hardcoded API keys and secrets
- ❌ Weak cryptography (MD5)
- ❌ Use of eval()
- ❌ Insecure deserialization

**Purpose:** Demonstrate what security scanners detect

### `demo_secure.py`
Contains examples of **secure code** showing:
- ✅ Parameterized SQL queries
- ✅ Safe command execution
- ✅ Environment variables for secrets
- ✅ Strong cryptography (SHA256+)
- ✅ Safe expression evaluation
- ✅ Secure serialization

**Purpose:** Demonstrate security best practices

## 🎯 Why Are These Files Here?

These files are **educational demonstrations** that show:

1. **How security vulnerabilities look in real code**
2. **What security scanners detect**
3. **How to fix security issues**
4. **The difference between secure and insecure code**

## 🚫 Why Not in `src/` Directory?

The CI/CD pipeline scans the `src/` directory for security issues and **blocks code with HIGH severity vulnerabilities**.

Since `demo_insecure.py` contains intentional vulnerabilities, it would cause the pipeline to fail. By keeping these files in the `demos/` directory, they:
- ✅ Are available for learning purposes
- ✅ Don't interfere with CI/CD pipeline
- ✅ Can be run manually for demonstrations

## 🎬 Running the Demos

### Run All Demos:
```bash
./run_demo.sh
```

### Run Individual Scans:

**Scan Insecure Code (will find issues):**
```bash
bandit -r demos/demo_insecure.py -ll
```

**Scan Secure Code (will pass):**
```bash
bandit -r demos/demo_secure.py -ll
```

**Detect Secrets:**
```bash
gitleaks detect --source demos/ --no-git
```

## 📚 Learning From These Files

### Step 1: Read the Insecure Code
Open `demo_insecure.py` and identify the security issues.

### Step 2: Run Security Scans
See how Bandit and Gitleaks detect these issues automatically.

### Step 3: Compare with Secure Code
Open `demo_secure.py` to see the correct implementation.

### Step 4: Apply to Your Code
Use these patterns in your own projects.

## ⚠️ Security Warning

**DO NOT** use code from `demo_insecure.py` in production applications!

These examples are intentionally vulnerable and are for **educational purposes only**.

## 🎓 What You'll Learn

- How to identify security vulnerabilities
- What patterns to avoid
- How to write secure code
- How automated security scanning works
- Why DevSecOps pipelines are important

## 📖 Additional Resources

- See [DEMO_RESULTS.md](../DEMO_RESULTS.md) for complete demo results
- See [USAGE.md](../USAGE.md) for usage instructions
- See [SECURITY.md](../SECURITY.md) for security policy

---

**Remember:** The best way to learn security is to understand what **NOT** to do, then learn the right way! 🔒
