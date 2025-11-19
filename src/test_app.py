"""
Tests for the DevSecOps demo application
"""
import pytest
from src.app import app
from src.utils import validate_email, sanitize_input, hash_password

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_health(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_get_users(client):
    """Test get users endpoint"""
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_user(client):
    """Test get specific user endpoint"""
    response = client.get('/api/users/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert 'name' in data

def test_get_user_not_found(client):
    """Test get user that doesn't exist"""
    response = client.get('/api/users/999')
    assert response.status_code == 404

def test_validate_email():
    """Test email validation"""
    assert validate_email('test@example.com') is True
    assert validate_email('invalid-email') is False

def test_sanitize_input():
    """Test input sanitization"""
    assert sanitize_input('hello<script>') == 'helloscript'
    assert sanitize_input('test&data') == 'testdata'

def test_hash_password():
    """Test password hashing"""
    hashed = hash_password('test123')
    assert len(hashed) == 64  # SHA256 produces 64-char hex string
    assert hashed != 'test123'
