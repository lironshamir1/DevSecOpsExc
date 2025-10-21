"""
Basic tests for the vulnerable application
These tests demonstrate the vulnerabilities but should pass
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database import DatabaseManager
from crypto_utils import CryptoUtils


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test the index route returns correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Vulnerable API' in response.data


def test_hash_endpoint(client):
    """Test the hash endpoint (demonstrates weak hashing)"""
    response = client.get('/hash?data=test')
    assert response.status_code == 200
    data = response.get_json()
    assert 'md5' in data
    assert 'sha1' in data


def test_crypto_utils():
    """Test crypto utilities (demonstrates weak crypto)"""
    crypto = CryptoUtils()

    # Test weak password hashing
    password = "test123"
    hash1 = crypto.hash_password(password)
    assert len(hash1) == 32  # MD5 hash length

    # Test token generation
    token = crypto.generate_token()
    assert len(token) == 16


def test_database_manager():
    """Test database manager (demonstrates SQL injection vulnerability)"""
    db = DatabaseManager(':memory:')

    # This test demonstrates the vulnerability exists
    # In real security testing, you would test for the exploit
    assert db.db_path == ':memory:'


def test_render_endpoint(client):
    """Test render endpoint (demonstrates SSTI vulnerability)"""
    response = client.get('/render?template=Hello')
    assert response.status_code == 200


def test_yaml_endpoint(client):
    """Test YAML endpoint (demonstrates unsafe YAML loading)"""
    response = client.post('/yaml',
                          json={'yaml': 'test: value'})
    assert response.status_code == 200


class TestSecurityIssues:
    """Tests that document known security issues"""

    def test_hardcoded_secrets_exist(self):
        """Document that hardcoded secrets exist in the code"""
        # This test passes but highlights the vulnerability
        from app import API_KEY, DB_PASSWORD
        assert API_KEY is not None
        assert DB_PASSWORD is not None

    def test_debug_mode_enabled(self):
        """Document that debug mode is enabled"""
        assert app.config['DEBUG'] is True

    def test_weak_secret_key(self):
        """Document that a weak secret key is used"""
        assert app.secret_key == "super-secret-key-12345"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
