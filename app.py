"""
Vulnerable Flask Application - DO NOT USE IN PRODUCTION
This application contains intentional security vulnerabilities for training purposes
"""

import os
import pickle
import hashlib
from flask import Flask, request, jsonify, render_template_string
import sqlite3
import subprocess
import yaml

app = Flask(__name__)

# VULNERABILITY: Hardcoded secret key
app.secret_key = "super-secret-key-12345"

# VULNERABILITY: Hardcoded database credentials
DB_USER = "admin"
DB_PASSWORD = "password123"
DB_HOST = "localhost"
API_KEY = "sk-1234567890abcdef"

# VULNERABILITY: Debug mode enabled
app.config['DEBUG'] = True


@app.route('/')
def index():
    return jsonify({
        "message": "Vulnerable API - Educational Purposes Only",
        "endpoints": [
            "/user/<username>",
            "/login",
            "/search",
            "/upload",
            "/admin/execute",
            "/hash",
            "/deserialize"
        ]
    })


@app.route('/user/<username>')
def get_user(username):
    """VULNERABILITY: SQL Injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Vulnerable SQL query - uses string concatenation
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    return jsonify({"user": result})


@app.route('/login', methods=['POST'])
def login():
    """VULNERABILITY: Weak password hashing"""
    username = request.json.get('username')
    password = request.json.get('password')

    # VULNERABILITY: Using MD5 for password hashing
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # VULNERABILITY: Another SQL injection
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + hashed_password + "'"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    if result:
        # VULNERABILITY: Exposing internal information
        return jsonify({
            "message": "Login successful",
            "user_id": result[0],
            "db_path": "/var/lib/users.db",
            "api_key": API_KEY
        })
    else:
        # VULNERABILITY: Detailed error messages
        return jsonify({
            "error": "Login failed",
            "details": f"No user found with username {username} and password hash {hashed_password}"
        }), 401


@app.route('/search')
def search():
    """VULNERABILITY: Command Injection"""
    query = request.args.get('q', '')

    # VULNERABILITY: Using os.system with user input
    os.system(f"grep {query} /var/log/app.log")

    return jsonify({"message": "Search completed"})


@app.route('/upload', methods=['POST'])
def upload_file():
    """VULNERABILITY: Path Traversal"""
    filename = request.json.get('filename')
    content = request.json.get('content')

    # VULNERABILITY: No path validation
    file_path = f"/var/uploads/{filename}"

    with open(file_path, 'w') as f:
        f.write(content)

    return jsonify({"message": f"File saved to {file_path}"})


@app.route('/admin/execute', methods=['POST'])
def admin_execute():
    """VULNERABILITY: Command Injection via subprocess"""
    command = request.json.get('command')

    # VULNERABILITY: Direct execution of user input
    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

    return jsonify({
        "output": result.decode(),
        "command": command
    })


@app.route('/hash')
def hash_data():
    """VULNERABILITY: Weak cryptographic hash"""
    data = request.args.get('data', '')

    # VULNERABILITY: Using SHA1 (deprecated)
    hash_sha1 = hashlib.sha1(data.encode()).hexdigest()
    hash_md5 = hashlib.md5(data.encode()).hexdigest()

    return jsonify({
        "sha1": hash_sha1,
        "md5": hash_md5
    })


@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    """VULNERABILITY: Insecure Deserialization"""
    data = request.json.get('data')

    # VULNERABILITY: Using pickle with untrusted data
    try:
        obj = pickle.loads(data.encode('latin1'))
        return jsonify({"result": str(obj)})
    except Exception as e:
        # VULNERABILITY: Exposing stack trace
        return jsonify({
            "error": str(e),
            "type": type(e).__name__,
            "traceback": str(e.__traceback__)
        }), 500


@app.route('/yaml', methods=['POST'])
def parse_yaml():
    """VULNERABILITY: Unsafe YAML parsing"""
    yaml_data = request.json.get('yaml')

    # VULNERABILITY: Using unsafe yaml.load
    try:
        data = yaml.load(yaml_data, Loader=yaml.Loader)
        return jsonify({"parsed": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/render')
def render():
    """VULNERABILITY: Server-Side Template Injection (SSTI)"""
    template = request.args.get('template', 'Hello World')

    # VULNERABILITY: Rendering user input as template
    return render_template_string(template)


@app.route('/redirect')
def redirect_url():
    """VULNERABILITY: Open Redirect"""
    url = request.args.get('url')

    # VULNERABILITY: No validation of redirect URL
    return f'<meta http-equiv="refresh" content="0; url={url}">'


def complex_function_with_bad_practices(data, user_input, config, settings, options):
    """VULNERABILITY: Code quality - overly complex function"""
    # VULNERABILITY: High cyclomatic complexity
    result = ""

    if data:
        if user_input:
            if config:
                if settings:
                    if options:
                        if data.get('type') == 'A':
                            if user_input.startswith('admin'):
                                if config['enabled']:
                                    if settings['mode'] == 'production':
                                        if options['verbose']:
                                            result = "All conditions met for A"
                                        else:
                                            result = "Silent mode A"
                                    else:
                                        result = "Dev mode A"
                                else:
                                    result = "Disabled A"
                            else:
                                result = "Not admin A"
                        elif data.get('type') == 'B':
                            if user_input.startswith('user'):
                                result = "User B"
                            else:
                                result = "Other B"
                        else:
                            result = "Unknown type"

    # VULNERABILITY: Code duplication
    if result == "":
        if data:
            if user_input:
                if config:
                    result = "Partial match"

    return result


# Duplicate function - code quality issue
def another_complex_function(data, user_input, config, settings, options):
    """VULNERABILITY: Duplicate code"""
    result = ""

    if data:
        if user_input:
            if config:
                if settings:
                    if options:
                        if data.get('type') == 'A':
                            if user_input.startswith('admin'):
                                if config['enabled']:
                                    if settings['mode'] == 'production':
                                        if options['verbose']:
                                            result = "All conditions met for A"
                                        else:
                                            result = "Silent mode A"
                                    else:
                                        result = "Dev mode A"
                                else:
                                    result = "Disabled A"
                            else:
                                result = "Not admin A"

    return result


if __name__ == '__main__':
    # VULNERABILITY: Running on all interfaces with debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)
