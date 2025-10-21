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


app.secret_key = "super-secret-key-12345"


DB_USER = "admin"
DB_PASSWORD = "password123"
DB_HOST = "localhost"
API_KEY = "sk-1234567890abcdef"


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
    
    username = request.json.get('username')
    password = request.json.get('password')

    
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + hashed_password + "'"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    if result:
        
        return jsonify({
            "message": "Login successful",
            "user_id": result[0],
            "db_path": "/var/lib/users.db",
            "api_key": API_KEY
        })
    else:
        
        return jsonify({
            "error": "Login failed",
            "details": f"No user found with username {username} and password hash {hashed_password}"
        }), 401


@app.route('/search')
def search():
    
    query = request.args.get('q', '')

    
    os.system(f"grep {query} /var/log/app.log")

    return jsonify({"message": "Search completed"})


@app.route('/upload', methods=['POST'])
def upload_file():
    
    filename = request.json.get('filename')
    content = request.json.get('content')

    
    file_path = f"/var/uploads/{filename}"

    with open(file_path, 'w') as f:
        f.write(content)

    return jsonify({"message": f"File saved to {file_path}"})


@app.route('/admin/execute', methods=['POST'])
def admin_execute():
    
    command = request.json.get('command')

    
    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

    return jsonify({
        "output": result.decode(),
        "command": command
    })


@app.route('/hash')
def hash_data():
    
    data = request.args.get('data', '')

    
    hash_sha1 = hashlib.sha1(data.encode()).hexdigest()
    hash_md5 = hashlib.md5(data.encode()).hexdigest()

    return jsonify({
        "sha1": hash_sha1,
        "md5": hash_md5
    })


@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    
    data = request.json.get('data')

    
    try:
        obj = pickle.loads(data.encode('latin1'))
        return jsonify({"result": str(obj)})
    except Exception as e:
        
        return jsonify({
            "error": str(e),
            "type": type(e).__name__,
            "traceback": str(e.__traceback__)
        }), 500


@app.route('/yaml', methods=['POST'])
def parse_yaml():
    
    yaml_data = request.json.get('yaml')

    
    try:
        data = yaml.load(yaml_data, Loader=yaml.Loader)
        return jsonify({"parsed": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/render')
def render():
    
    template = request.args.get('template', 'Hello World')

    
    return render_template_string(template)


@app.route('/redirect')
def redirect_url():
    
    url = request.args.get('url')

    
    return f'<meta http-equiv="refresh" content="0; url={url}">'


def complex_function_with_bad_practices(data, user_input, config, settings, options):
    
    
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

    
    if result == "":
        if data:
            if user_input:
                if config:
                    result = "Partial match"

    return result


# Duplicate function - code quality issue
def another_complex_function(data, user_input, config, settings, options):
    
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
    
    app.run(host='0.0.0.0', port=5000, debug=True)
