"""
Demo: Insecure Code Examples
This file intentionally contains security vulnerabilities for demonstration
"""

# ❌ VULNERABILITY 1: Hardcoded Secret (Gitleaks will catch this)
API_KEY = "sk-1234567890abcdefghijklmnop"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
DATABASE_PASSWORD = "MyS3cr3tP@ssw0rd!"

# ❌ VULNERABILITY 2: SQL Injection
def get_user_unsafe(user_id):
    """SQL Injection vulnerability - Bandit will flag this"""
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # BAD: String formatting in SQL query
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)  # B608: SQL injection possible
    return cursor.fetchone()

# ❌ VULNERABILITY 3: Command Injection
def run_command_unsafe(filename):
    """Command injection vulnerability"""
    import subprocess
    # BAD: Using shell=True with user input
    result = subprocess.call(f"cat {filename}", shell=True)  # B602
    return result

# ❌ VULNERABILITY 4: Weak Cryptography
def hash_password_weak(password):
    """Using broken MD5 algorithm"""
    import hashlib
    # BAD: MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()  # B303

# ❌ VULNERABILITY 5: Using eval()
def calculate_unsafe(expression):
    """Using eval - extremely dangerous!"""
    # BAD: eval can execute arbitrary code
    return eval(expression)  # B307

# ❌ VULNERABILITY 6: Assert used for security
def check_permission(user):
    """Using assert for security checks"""
    assert user.is_admin, "Not authorized"  # B101
    return True

# ❌ VULNERABILITY 7: Pickle deserialization
def load_data_unsafe(data):
    """Insecure deserialization"""
    import pickle
    # BAD: Unpickling untrusted data
    return pickle.loads(data)  # B301

print("⚠️  This file contains 7+ security vulnerabilities!")
print("Run: bandit -r src/demo_insecure.py -ll")
