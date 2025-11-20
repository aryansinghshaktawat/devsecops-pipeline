"""
Demo: Secure Code Examples
This shows the CORRECT way to write secure code
"""
import os
import sqlite3
import subprocess
import hashlib
from src.utils import sanitize_input

# ✅ SECURE 1: Load secrets from environment
API_KEY = os.getenv('API_KEY', 'default-for-dev')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

# ✅ SECURE 2: Parameterized SQL queries
def get_user_safe(user_id):
    """Protected against SQL injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # GOOD: Parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

# ✅ SECURE 3: No shell injection
def run_command_safe(filename):
    """Protected against command injection"""
    # GOOD: No shell=True, sanitized input
    safe_filename = sanitize_input(filename)
    result = subprocess.run(['cat', safe_filename], 
                           shell=False, 
                           check=True,
                           capture_output=True)
    return result.stdout

# ✅ SECURE 4: Strong cryptography
def hash_password_secure(password):
    """Using SHA256 (bcrypt is even better)"""
    # GOOD: SHA256 or better
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ SECURE 5: Safe expression evaluation
def calculate_safe(expression):
    """Safe mathematical evaluation"""
    # GOOD: Use ast.literal_eval or safer alternatives
    import ast
    try:
        # Only evaluates literals, not arbitrary code
        return ast.literal_eval(expression)
    except (ValueError, SyntaxError):
        return None

# ✅ SECURE 6: Proper exception handling
def check_permission_safe(user):
    """Proper error handling instead of assert"""
    if not user.is_admin:
        raise PermissionError("Not authorized")
    return True

# ✅ SECURE 7: Safe serialization
def load_data_safe(data):
    """Use JSON instead of pickle"""
    import json
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None

print("✅ This file contains secure code patterns!")
print("Run: bandit -r src/demo_secure.py -ll")
print("Expected: No HIGH severity issues!")
