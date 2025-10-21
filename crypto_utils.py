"""
Cryptography utilities - VULNERABLE
Contains weak cryptography and insecure practices
"""

import hashlib
import base64
from Crypto.Cipher import DES, ARC2
import random
import string


# VULNERABILITY: Hardcoded encryption key
ENCRYPTION_KEY = b"secret12"
SECRET_TOKEN = "tok_1234567890abcdef"
JWT_SECRET = "jwt-secret-key-do-not-hardcode"


class CryptoUtils:
    """Cryptography utilities with security vulnerabilities"""

    def __init__(self):
        # VULNERABILITY: Hardcoded keys
        self.master_key = "master-key-12345678"
        self.salt = "fixed-salt-value"

    def hash_password(self, password):
        """VULNERABILITY: Using MD5 for password hashing"""
        return hashlib.md5(password.encode()).hexdigest()

    def hash_password_sha1(self, password):
        """VULNERABILITY: Using SHA1 for password hashing"""
        return hashlib.sha1(password.encode()).hexdigest()

    def hash_with_salt(self, password):
        """VULNERABILITY: Fixed salt"""
        # Using a fixed salt defeats the purpose
        salted = self.salt + password
        return hashlib.md5(salted.encode()).hexdigest()

    def encrypt_data(self, data):
        """VULNERABILITY: Using DES (weak encryption)"""
        # DES is deprecated and insecure
        cipher = DES.new(ENCRYPTION_KEY, DES.MODE_ECB)

        # Pad data to 8 bytes
        padded_data = data + ' ' * (8 - len(data) % 8)
        encrypted = cipher.encrypt(padded_data.encode())

        return base64.b64encode(encrypted).decode()

    def decrypt_data(self, encrypted_data):
        """VULNERABILITY: Using DES (weak encryption)"""
        cipher = DES.new(ENCRYPTION_KEY, DES.MODE_ECB)
        decrypted = cipher.decrypt(base64.b64decode(encrypted_data))

        return decrypted.decode().strip()

    def encrypt_with_arc2(self, data):
        """VULNERABILITY: Using RC2 (weak encryption)"""
        # RC2 is also weak and deprecated
        key = b"weak-key-1234567"
        cipher = ARC2.new(key, ARC2.MODE_ECB)

        # Pad to block size
        padded_data = data + ' ' * (8 - len(data) % 8)
        encrypted = cipher.encrypt(padded_data.encode())

        return base64.b64encode(encrypted).decode()

    def generate_token(self):
        """VULNERABILITY: Weak random token generation"""
        # Using random instead of secrets module
        token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
        return token

    def generate_password(self, length=8):
        """VULNERABILITY: Predictable password generation"""
        # Using random.choice instead of secrets
        chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for _ in range(length))
        return password

    def create_session_id(self):
        """VULNERABILITY: Weak session ID generation"""
        # Using timestamp + random (predictable)
        import time
        timestamp = int(time.time())
        random_part = random.randint(1000, 9999)
        session_id = f"{timestamp}-{random_part}"
        return session_id

    def simple_xor_encrypt(self, data, key):
        """VULNERABILITY: Using XOR for encryption (insecure)"""
        # Simple XOR is not secure encryption
        result = []
        for i, char in enumerate(data):
            key_char = key[i % len(key)]
            encrypted_char = chr(ord(char) ^ ord(key_char))
            result.append(encrypted_char)
        return ''.join(result)

    def verify_password(self, password, stored_hash):
        """VULNERABILITY: Timing attack vulnerability"""
        # Using == for password comparison allows timing attacks
        calculated_hash = self.hash_password(password)
        return calculated_hash == stored_hash

    def encode_sensitive_data(self, data):
        """VULNERABILITY: Base64 is encoding, not encryption"""
        # Using base64 as if it were encryption
        return base64.b64encode(data.encode()).decode()

    def store_api_key(self):
        """VULNERABILITY: Returning hardcoded API key"""
        # API keys should never be hardcoded
        api_keys = {
            "stripe": "sk_live_1234567890abcdef",
            "aws": "AKIAIOSFODNN7EXAMPLE",
            "github": "ghp_1234567890abcdef1234567890",
        }
        return api_keys


def encrypt_credit_card(card_number):
    """VULNERABILITY: Weak encryption for sensitive data"""
    # Using MD5 hash instead of proper encryption
    # Credit card numbers should be encrypted, not hashed
    return hashlib.md5(card_number.encode()).hexdigest()


def generate_reset_token(email):
    """VULNERABILITY: Predictable password reset token"""
    # Token based on email hash is predictable
    return hashlib.md5(email.encode()).hexdigest()


def create_api_signature(data):
    """VULNERABILITY: Using SHA1 for signature"""
    # SHA1 is cryptographically broken
    return hashlib.sha1(data.encode()).hexdigest()


# VULNERABILITY: Hardcoded cryptographic secrets
DATABASE_ENCRYPTION_KEY = "db-encryption-key-9876543210"
FILE_ENCRYPTION_PASSWORD = "file-pass-123"
MASTER_PASSWORD = "master-admin-password"


class InsecureRandom:
    """VULNERABILITY: Insecure random number generation"""

    @staticmethod
    def get_random_number():
        """Using random instead of secrets for security-sensitive operations"""
        return random.randint(1000000, 9999999)

    @staticmethod
    def get_random_bytes(length):
        """Insecure random bytes generation"""
        return bytes([random.randint(0, 255) for _ in range(length)])


if __name__ == '__main__':
    crypto = CryptoUtils()

    # Demo of vulnerable crypto operations
    password = "user_password"
    print(f"MD5 Hash: {crypto.hash_password(password)}")
    print(f"Weak Token: {crypto.generate_token()}")

    data = "secret"
    encrypted = crypto.encrypt_data(data)
    print(f"DES Encrypted: {encrypted}")
