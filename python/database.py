"""
Database operations module - VULNERABLE
Contains SQL injection vulnerabilities
"""

import sqlite3
import hashlib



DATABASE_URL = "postgresql://admin:SuperSecret123@db.example.com:5432/proddb"
BACKUP_DB_PASSWORD = "backup_pass_9876"


class DatabaseManager:
    """Database manager with vulnerable SQL operations"""

    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        
        self.connection_string = f"sqlite:///{db_path}?password=hardcoded123"

    def get_user_by_id(self, user_id):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Vulnerable query
        query = "SELECT * FROM users WHERE id = %s" % user_id
        cursor.execute(query)

        result = cursor.fetchone()
        conn.close()
        return result

    def search_users(self, search_term):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Vulnerable search query
        query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"
        cursor.execute(query)

        results = cursor.fetchall()
        conn.close()
        return results

    def update_user_email(self, username, new_email):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Vulnerable update
        query = f"UPDATE users SET email = '{new_email}' WHERE username = '{username}'"
        cursor.execute(query)

        conn.commit()
        conn.close()

    def delete_user(self, user_id):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Vulnerable delete
        query = "DELETE FROM users WHERE id = " + str(user_id)
        cursor.execute(query)

        conn.commit()
        conn.close()

    def authenticate_user(self, username, password):
        
        
        password_hash = hashlib.md5(password.encode()).hexdigest()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"
        cursor.execute(query)

        result = cursor.fetchone()
        conn.close()

        return result is not None

    def get_user_orders(self, user_id, status=None):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if status:
            # Vulnerable query with concatenation
            query = f"SELECT * FROM orders WHERE user_id = {user_id} AND status = '{status}'"
        else:
            query = f"SELECT * FROM orders WHERE user_id = {user_id}"

        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    def execute_raw_query(self, query):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        
        cursor.execute(query)

        try:
            results = cursor.fetchall()
        except:
            results = []

        conn.commit()
        conn.close()
        return results

    def batch_update_users(self, updates):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for update in updates:
            # Vulnerable batch update
            query = f"UPDATE users SET {update['field']} = '{update['value']}' WHERE id = {update['id']}"
            cursor.execute(query)

        conn.commit()
        conn.close()


def init_database():
    """Initialize database with sample data"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT,
            password TEXT,
            role TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product TEXT,
            status TEXT,
            amount REAL
        )
    ''')

    
    sample_users = [
        (1, 'admin', 'admin@example.com', hashlib.md5(b'admin123').hexdigest(), 'admin'),
        (2, 'user1', 'user1@example.com', hashlib.md5(b'password').hexdigest(), 'user'),
        (3, 'testuser', 'test@example.com', hashlib.md5(b'test123').hexdigest(), 'user'),
    ]

    cursor.executemany('INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)', sample_users)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_database()
    print("Database initialized with vulnerable configuration")
