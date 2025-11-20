"""
Simple Flask API for DevSecOps Pipeline Demo
"""
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Welcome to DevSecOps Pipeline Demo",
        "version": "1.0.0",
        "status": "healthy"
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "devsecops-demo"
    }), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get users endpoint"""
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]
    return jsonify(users), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user by ID"""
    users = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
        3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    }
    
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')
    app.run(host=host, port=port, debug=False)
