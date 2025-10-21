"""
File handling module - VULNERABLE
Contains path traversal and insecure file operation vulnerabilities
"""

import os
import pickle
import tempfile


class FileHandler:
    """File operations with path traversal vulnerabilities"""

    def __init__(self, base_dir='/var/uploads'):
        self.base_dir = base_dir

    def read_file(self, filename):
        """VULNERABILITY: Path traversal - no validation"""
        # Attacker can use ../../../etc/passwd
        file_path = os.path.join(self.base_dir, filename)

        with open(file_path, 'r') as f:
            return f.read()

    def write_file(self, filename, content):
        """VULNERABILITY: Path traversal in write operation"""
        # No validation allows writing anywhere
        file_path = f"{self.base_dir}/{filename}"

        with open(file_path, 'w') as f:
            f.write(content)

        return file_path

    def delete_file(self, filename):
        """VULNERABILITY: Path traversal in delete operation"""
        file_path = self.base_dir + "/" + filename
        os.remove(file_path)

    def read_user_file(self, user_id, filename):
        """VULNERABILITY: Path traversal with multiple parameters"""
        # User can manipulate both user_id and filename
        path = f"/data/users/{user_id}/files/{filename}"

        with open(path, 'r') as f:
            return f.read()

    def save_upload(self, filename, data):
        """VULNERABILITY: No filename sanitization"""
        # Filename can contain path traversal sequences
        full_path = os.path.join('/tmp/uploads', filename)

        with open(full_path, 'wb') as f:
            f.write(data)

        return full_path

    def get_file_content(self, filepath):
        """VULNERABILITY: Direct file access without validation"""
        # No restriction on which files can be accessed
        with open(filepath, 'r') as f:
            return f.read()

    def load_config(self, config_name):
        """VULNERABILITY: Path traversal in config loading"""
        config_path = f"./configs/{config_name}.conf"

        with open(config_path, 'r') as f:
            return f.read()

    def save_serialized_data(self, filename, data):
        """VULNERABILITY: Insecure deserialization with pickle"""
        file_path = os.path.join(self.base_dir, filename)

        with open(file_path, 'wb') as f:
            # pickle is unsafe for untrusted data
            pickle.dump(data, f)

    def load_serialized_data(self, filename):
        """VULNERABILITY: Loading pickle from untrusted source"""
        file_path = os.path.join(self.base_dir, filename)

        with open(file_path, 'rb') as f:
            # Unsafe deserialization
            return pickle.load(f)

    def extract_archive(self, archive_path, destination):
        """VULNERABILITY: Unsafe archive extraction"""
        import zipfile

        # No validation of archive contents
        # Malicious archives can write outside destination
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(destination)

    def create_temp_file(self, content):
        """VULNERABILITY: Insecure temp file creation"""
        # Using predictable temp file name
        temp_path = f"/tmp/upload_{os.getpid()}.tmp"

        with open(temp_path, 'w') as f:
            f.write(content)

        return temp_path


def read_log_file(log_name):
    """VULNERABILITY: Path traversal in standalone function"""
    # No validation on log_name parameter
    log_path = f"/var/log/app/{log_name}"

    try:
        with open(log_path, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def download_user_data(user_id, data_type):
    """VULNERABILITY: Path traversal with formatted string"""
    # Both parameters can be manipulated
    file_path = f"/data/exports/{user_id}/{data_type}.csv"

    with open(file_path, 'r') as f:
        return f.read()


def backup_file(source_file):
    """VULNERABILITY: Command injection via filename"""
    import subprocess

    # Filename not sanitized before use in command
    backup_path = f"/backups/{source_file}.bak"

    # VULNERABILITY: Also has command injection
    subprocess.call(f"cp {source_file} {backup_path}", shell=True)

    return backup_path


def get_image(image_id):
    """VULNERABILITY: Path traversal in image serving"""
    # image_id can contain ../
    image_path = f"./static/images/{image_id}.jpg"

    with open(image_path, 'rb') as f:
        return f.read()


def write_to_log(log_type, message):
    """VULNERABILITY: Log injection"""
    # User-controlled log_type allows writing to arbitrary files
    log_file = f"/var/log/{log_type}.log"

    with open(log_file, 'a') as f:
        # Also vulnerable to log injection in message
        f.write(f"{message}\n")


class DocumentManager:
    """Document management with file vulnerabilities"""

    def __init__(self):
        self.docs_dir = "/var/documents"

    def get_document(self, doc_id, format='pdf'):
        """VULNERABILITY: Multiple path traversal points"""
        # Both doc_id and format can be manipulated
        doc_path = f"{self.docs_dir}/{doc_id}.{format}"

        with open(doc_path, 'rb') as f:
            return f.read()

    def save_document(self, category, filename, content):
        """VULNERABILITY: No path validation on category or filename"""
        full_path = f"{self.docs_dir}/{category}/{filename}"

        # Create directory if it doesn't exist (can create anywhere)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'w') as f:
            f.write(content)

    def include_template(self, template_name):
        """VULNERABILITY: Template path traversal"""
        template_path = f"templates/{template_name}.html"

        with open(template_path, 'r') as f:
            template_content = f.read()

        # VULNERABILITY: Also has SSTI potential
        return eval(f"f'''{template_content}'''")


if __name__ == '__main__':
    handler = FileHandler()
    print("File handler initialized with vulnerabilities")
