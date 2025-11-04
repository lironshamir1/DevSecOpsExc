# Solutions Guide - DevSecOps Practice Repository

This guide provides detailed solutions for fixing all security vulnerabilities and code quality issues in this repository.

## Table of Contents

1. [Hardcoded Secrets](#1-hardcoded-secrets)
2. [SQL Injection](#2-sql-injection)
3. [Command Injection](#3-command-injection)
4. [Insecure Cryptography](#4-insecure-cryptography)
5. [Path Traversal](#5-path-traversal)
6. [Insecure Deserialization](#6-insecure-deserialization)
7. [Vulnerable Dependencies](#7-vulnerable-dependencies)
8. [Missing Security Headers](#8-missing-security-headers)
9. [Code Quality Issues](#9-code-quality-issues)
10. [Information Disclosure](#10-information-disclosure)

---

## 1. Hardcoded Secrets

### Problem
Secrets, API keys, and credentials are hardcoded in the source code.

**Vulnerable Code (app.py):**
```python
app.secret_key = "super-secret-key-12345"
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "password123"
```

### Solution
Use environment variables and secure secret management.

**Fixed Code:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.secret_key = os.environ.get('SECRET_KEY')
API_KEY = os.environ.get('API_KEY')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Validate that required secrets are present
if not app.secret_key:
    raise ValueError("SECRET_KEY environment variable is required")
```

**Create .env file (and add to .gitignore):**
```bash
SECRET_KEY=your-random-secret-key-here
API_KEY=your-api-key-here
DB_PASSWORD=your-secure-password-here
```

**Best Practices:**
- Use environment variables for all secrets
- Use secret management tools (AWS Secrets Manager, Azure Key Vault, or OpenShift Secrets)
- Never commit .env files to version control
- Use strong, randomly generated secrets
- Rotate secrets regularly
- Use different secrets for different environments

---

## 2. SQL Injection

### Problem
SQL queries are constructed using string concatenation or f-strings with user input.

**Vulnerable Code (database.py):**
```python
def get_user_by_id(self, user_id):
    query = "SELECT * FROM users WHERE id = %s" % user_id
    cursor.execute(query)
```

**Vulnerable Code (app.py):**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

### Solution
Use parameterized queries (prepared statements).

**Fixed Code:**
```python
def get_user_by_id(self, user_id):
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()

    # Use parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))

    result = cursor.fetchone()
    conn.close()
    return result

def search_users(self, search_term):
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()

    # Use parameterized query with LIKE
    query = "SELECT * FROM users WHERE username LIKE ? OR email LIKE ?"
    cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))

    results = cursor.fetchall()
    conn.close()
    return results
```

**Using SQLAlchemy (recommended):**
```python
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///users.db')

# Safe parameterized query
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT * FROM users WHERE id = :id"),
        {"id": user_id}
    )
```

**Best Practices:**
- Always use parameterized queries
- Never concatenate user input into SQL
- Use ORM frameworks (SQLAlchemy, Django ORM)
- Implement input validation
- Use least privilege database accounts
- Enable database query logging for monitoring

---

## 3. Command Injection

### Problem
User input is passed directly to shell commands without validation.

**Vulnerable Code (admin.py):**
```python
def run_diagnostic(self, host):
    cmd = f"ping -c 4 {host}"
    output = subprocess.check_output(cmd, shell=True)
    return output.decode()
```

### Solution
Use subprocess with argument lists and avoid shell=True.

**Fixed Code:**
```python
import subprocess
import shlex
import re

def run_diagnostic(self, host):
    # Validate input
    if not self._is_valid_hostname(host):
        raise ValueError("Invalid hostname")

    # Use argument list instead of shell string
    cmd = ['ping', '-c', '4', host]

    try:
        # shell=False prevents command injection
        output = subprocess.check_output(
            cmd,
            shell=False,
            timeout=10,
            stderr=subprocess.STDOUT
        )
        return output.decode()
    except subprocess.TimeoutExpired:
        return "Ping timeout"
    except subprocess.CalledProcessError as e:
        return f"Ping failed: {e}"

def _is_valid_hostname(self, hostname):
    # Validate hostname format
    pattern = r'^[a-zA-Z0-9.-]+$'
    return re.match(pattern, hostname) is not None
```

**Alternative - Using shlex for safe parsing:**
```python
def execute_safe_command(self, command_parts):
    # Whitelist allowed commands
    ALLOWED_COMMANDS = ['ls', 'cat', 'grep']

    if command_parts[0] not in ALLOWED_COMMANDS:
        raise ValueError(f"Command not allowed: {command_parts[0]}")

    # Use argument list
    result = subprocess.run(
        command_parts,
        shell=False,
        capture_output=True,
        timeout=5
    )
    return result.stdout.decode()
```

**Best Practices:**
- Never use shell=True with user input
- Always use argument lists
- Validate and sanitize all input
- Use whitelists for allowed commands/parameters
- Implement timeouts
- Run with least privilege
- Consider using libraries instead of shell commands

---

## 4. Insecure Cryptography

### Problem
Weak hashing algorithms (MD5, SHA1) used for passwords and sensitive data.

**Vulnerable Code (crypto_utils.py):**
```python
def hash_password(self, password):
    return hashlib.md5(password.encode()).hexdigest()
```

### Solution
Use strong, modern cryptographic algorithms.

**Fixed Code:**
```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets

# For password hashing
class SecureCrypto:
    def __init__(self):
        self.ph = PasswordHasher()

    def hash_password(self, password):
        """Use Argon2 for password hashing"""
        return self.ph.hash(password)

    def verify_password(self, password, hash):
        """Verify password against hash"""
        try:
            self.ph.verify(hash, password)
            return True
        except VerifyMismatchError:
            return False

    def generate_token(self):
        """Generate cryptographically secure random token"""
        return secrets.token_urlsafe(32)

    def generate_salt(self):
        """Generate random salt"""
        return secrets.token_bytes(16)
```

**Using bcrypt (alternative):**
```python
import bcrypt

def hash_password(password):
    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
```

**For encryption (not hashing):**
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

def encrypt_data(data, password):
    """Encrypt data using Fernet (AES-128)"""
    # Derive key from password
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return encrypted

def decrypt_data(encrypted_data, password):
    """Decrypt data"""
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    f = Fernet(key)
    decrypted = f.decrypt(encrypted_data)
    return decrypted.decode()
```

**Best Practices:**
- Use Argon2, bcrypt, or scrypt for password hashing
- Never use MD5 or SHA1 for security purposes
- Use AES-256 for encryption
- Generate random salts for each password
- Use secrets module for random generation
- Implement constant-time comparison for password verification
- Keep cryptographic libraries updated

---

## 5. Path Traversal

### Problem
File paths constructed using user input without validation.

**Vulnerable Code (file_handler.py):**
```python
def read_file(self, filename):
    file_path = os.path.join(self.base_dir, filename)
    with open(file_path, 'r') as f:
        return f.read()
```

### Solution
Validate and sanitize file paths.

**Fixed Code:**
```python
import os
from pathlib import Path

class SecureFileHandler:
    def __init__(self, base_dir='/var/uploads'):
        self.base_dir = Path(base_dir).resolve()

    def read_file(self, filename):
        """Safely read file with path traversal protection"""
        # Remove any path traversal sequences
        safe_filename = os.path.basename(filename)

        # Construct full path
        file_path = (self.base_dir / safe_filename).resolve()

        # Verify the file is within base_dir
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        # Check file exists and is a file
        if not file_path.is_file():
            raise FileNotFoundError("File not found")

        with open(file_path, 'r') as f:
            return f.read()

    def _is_safe_path(self, path):
        """Verify path is within base directory"""
        try:
            path = path.resolve()
            return path.is_relative_to(self.base_dir)
        except (ValueError, OSError):
            return False

    def write_file(self, filename, content):
        """Safely write file"""
        # Validate filename
        if not self._is_valid_filename(filename):
            raise ValueError("Invalid filename")

        safe_filename = os.path.basename(filename)
        file_path = (self.base_dir / safe_filename).resolve()

        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        with open(file_path, 'w') as f:
            f.write(content)

        return str(file_path)

    def _is_valid_filename(self, filename):
        """Validate filename characters"""
        import re
        # Allow only alphanumeric, dots, underscores, hyphens
        pattern = r'^[a-zA-Z0-9._-]+$'
        return re.match(pattern, filename) is not None
```

**Best Practices:**
- Always use os.path.basename() to strip directory components
- Use pathlib.Path.resolve() and validate with is_relative_to()
- Whitelist allowed characters in filenames
- Never trust user input for file paths
- Implement file type validation
- Use separate directories for user uploads
- Set proper file permissions

---

## 6. Insecure Deserialization

### Problem
Using pickle or unsafe YAML loading with untrusted data.

**Vulnerable Code (app.py):**
```python
def deserialize_data():
    data = request.json.get('data')
    obj = pickle.loads(data.encode('latin1'))
    return jsonify({"result": str(obj)})
```

**Vulnerable Code (YAML):**
```python
data = yaml.load(yaml_data, Loader=yaml.Loader)
```

### Solution
Use safe serialization formats and methods.

**Fixed Code:**
```python
import json
import yaml

# Use JSON instead of pickle
@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    """Use JSON for safe deserialization"""
    data = request.json.get('data')

    try:
        # JSON is safe for deserialization
        obj = json.loads(data)
        return jsonify({"result": obj})
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON"}), 400

# For YAML, use SafeLoader
@app.route('/yaml', methods=['POST'])
def parse_yaml():
    """Use safe YAML loading"""
    yaml_data = request.json.get('yaml')

    try:
        # Use SafeLoader to prevent code execution
        data = yaml.safe_load(yaml_data)
        return jsonify({"parsed": data})
    except yaml.YAMLError as e:
        return jsonify({"error": str(e)}), 400
```

**If you must use pickle (not recommended):**
```python
import hmac
import hashlib

def safe_pickle_loads(data, secret_key):
    """Pickle with HMAC verification"""
    # Split signature and data
    signature = data[:32]
    pickled_data = data[32:]

    # Verify signature
    expected_sig = hmac.new(
        secret_key.encode(),
        pickled_data,
        hashlib.sha256
    ).digest()

    if not hmac.compare_digest(signature, expected_sig):
        raise ValueError("Invalid signature")

    return pickle.loads(pickled_data)
```

**Best Practices:**
- Prefer JSON over pickle for serialization
- Use yaml.safe_load() instead of yaml.load()
- Never deserialize untrusted data with pickle
- Implement integrity checks (HMAC)
- Use schemas to validate deserialized data
- Consider MessagePack or Protocol Buffers as alternatives

---

## 7. Vulnerable Dependencies

### Problem
Using outdated packages with known security vulnerabilities.

**Vulnerable requirements.txt:**
```
Flask==2.0.1
PyYAML==5.3.1
Pillow==8.1.0
```

### Solution
Update to latest secure versions.

**Fixed requirements.txt:**
```
# Updated secure dependencies
Flask==3.0.0
Werkzeug==3.0.1
Jinja2==3.1.2
requests==2.31.0
PyYAML==6.0.1
pycryptodome==3.19.0
SQLAlchemy==2.0.23
Pillow==10.1.0
lxml==4.9.3
urllib3==2.1.0
paramiko==3.4.0

# Security tools
bandit==1.7.5
safety==2.3.5

# Password hashing
argon2-cffi==23.1.0
bcrypt==4.1.1

# Secure crypto
cryptography==41.0.7

# Environment management
python-dotenv==1.0.0

# Testing
pytest==7.4.3
pytest-cov==4.1.0

# Code quality
pylint==3.0.3
flake8==6.1.0
```

**Automate dependency updates:**
```bash
# Use pip-audit to check for vulnerabilities
pip install pip-audit
pip-audit

# Use safety
safety check

# Update dependencies
pip install --upgrade pip
pip list --outdated
pip install --upgrade <package>
```

**GitHub Dependabot configuration (.github/dependabot.yml):**
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

**Best Practices:**
- Regularly update dependencies
- Use automated tools (Dependabot, Renovate)
- Monitor security advisories
- Pin versions in production
- Use virtual environments
- Run security scans in CI/CD
- Keep Python itself updated

---

## 8. Missing Security Headers

### Problem
Application doesn't implement security headers or CSRF protection.

**Vulnerable Code:**
```python
app = Flask(__name__)
app.config['DEBUG'] = True
```

### Solution
Implement security headers and protections.

**Fixed Code:**
```python
from flask import Flask
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['DEBUG'] = False

# Enable CSRF protection
csrf = CSRFProtect(app)

# Enable security headers with Talisman
Talisman(app,
    force_https=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self'",
        'style-src': "'self'",
        'img-src': "'self'",
    },
    content_security_policy_nonce_in=['script-src'],
    feature_policy={
        'geolocation': "'none'",
        'camera': "'none'",
        'microphone': "'none'",
    }
)

# Custom security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# Session configuration
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800
)
```

**Best Practices:**
- Enable HTTPS only
- Implement HSTS
- Use CSP headers
- Enable CSRF protection
- Set secure cookie flags
- Implement rate limiting
- Use security middleware

---

## 9. Code Quality Issues

### Problem
High complexity functions, code duplication.

**Vulnerable Code:**
```python
def complex_function_with_bad_practices(data, user_input, config, settings, options):
    result = ""
    if data:
        if user_input:
            if config:
                if settings:
                    if options:
                        # Many nested conditions...
```

### Solution
Refactor for simplicity and maintainability.

**Fixed Code:**
```python
def process_request(data, user_input, config, settings, options):
    """Simplified function with guard clauses"""

    # Use guard clauses to reduce nesting
    if not data:
        return ""

    if not user_input:
        return ""

    if not config or not config.get('enabled'):
        return "Disabled"

    if not settings or not options:
        return ""

    # Process based on type
    return _process_by_type(data, user_input, settings, options)

def _process_by_type(data, user_input, settings, options):
    """Separate function for type-specific processing"""
    data_type = data.get('type')

    processors = {
        'A': _process_type_a,
        'B': _process_type_b,
    }

    processor = processors.get(data_type)
    if processor:
        return processor(user_input, settings, options)

    return "Unknown type"

def _process_type_a(user_input, settings, options):
    """Process type A"""
    if not user_input.startswith('admin'):
        return "Not admin A"

    if settings['mode'] != 'production':
        return "Dev mode A"

    return "All conditions met for A" if options['verbose'] else "Silent mode A"

def _process_type_b(user_input, settings, options):
    """Process type B"""
    return "User B" if user_input.startswith('user') else "Other B"
```

**Best Practices:**
- Keep functions small and focused
- Use guard clauses to reduce nesting
- Extract complex logic into separate functions
- Use meaningful variable and function names
- Follow DRY principle
- Limit cyclomatic complexity to < 10
- Add docstrings to all functions
- Use type hints

---

## 10. Information Disclosure

### Problem
Debug mode enabled, verbose error messages, exposing internal details.

**Vulnerable Code:**
```python
app.config['DEBUG'] = True

@app.route('/login', methods=['POST'])
def login():
    # ...
    return jsonify({
        "error": "Login failed",
        "details": f"No user found with username {username} and password hash {hashed_password}",
        "db_path": "/var/lib/users.db",
        "api_key": API_KEY
    }), 401
```

### Solution
Disable debug mode and implement proper error handling.

**Fixed Code:**
```python
import logging
from flask import Flask, jsonify

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Custom error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    # Don't expose internal details
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(Exception)
def handle_exception(error):
    logger.exception("Unhandled exception")
    # Generic error message
    return jsonify({"error": "An error occurred"}), 500

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Authenticate user
    user = authenticate_user(username, password)

    if user:
        # Log successful login (don't log sensitive data)
        logger.info(f"User logged in: {username}")

        return jsonify({
            "message": "Login successful",
            "token": generate_session_token(user)
        })
    else:
        # Generic error message
        # Log failed attempt for security monitoring
        logger.warning(f"Failed login attempt for: {username}")

        return jsonify({
            "error": "Invalid credentials"
        }), 401
```

**Best Practices:**
- Disable debug mode in production
- Use generic error messages for users
- Log detailed errors server-side only
- Don't expose stack traces
- Don't reveal internal paths or structure
- Implement rate limiting on authentication
- Monitor and alert on suspicious activity
- Use proper log levels

---

## Additional Security Improvements

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
    pass
```

### Input Validation
```python
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50)
    )
    email = fields.Email(required=True)
    age = fields.Int(validate=validate.Range(min=18, max=120))

@app.route('/user', methods=['POST'])
def create_user():
    schema = UserSchema()
    errors = schema.validate(request.json)

    if errors:
        return jsonify({"errors": errors}), 400

    # Process valid data
    user_data = schema.load(request.json)
```

### Database Connection Pooling
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

---

## Testing Your Fixes

After implementing fixes, verify with:

```bash
# Run security scans
bandit -r . -f json
safety check

# Run tests
pytest tests/ -v --cov=.

# Check code quality
pylint *.py
flake8 .

# Run the CI/CD pipeline
git push origin main
```

## Summary Checklist

- [ ] All secrets moved to environment variables
- [ ] All SQL queries use parameterization
- [ ] No shell=True in subprocess calls
- [ ] Strong cryptography (Argon2/bcrypt for passwords)
- [ ] Path traversal protections implemented
- [ ] No pickle/unsafe YAML loading
- [ ] All dependencies updated
- [ ] Security headers configured
- [ ] Code refactored for quality
- [ ] Debug mode disabled
- [ ] Error handling doesn't leak information
- [ ] Input validation implemented
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] Logging properly configured

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices-cheat-sheet/)
- [Flask Security](https://flask.palletsprojects.com/en/latest/security/)
- [bandit Documentation](https://bandit.readthedocs.io/)
