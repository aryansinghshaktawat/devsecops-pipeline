"""
Utility functions for the DevSecOps demo application
"""
import hashlib
import json
from datetime import datetime

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Basic email validation"""
    return '@' in email and '.' in email.split('@')[1]

def format_timestamp(timestamp=None):
    """Format timestamp to ISO format"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.isoformat()

def safe_json_loads(data):
    """Safely load JSON data"""
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None

def sanitize_input(user_input):
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(user_input, str):
        return str(user_input)
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '|']
    sanitized = user_input
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized
