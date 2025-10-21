"""
Admin module - VULNERABLE
Contains command injection and other admin-related vulnerabilities
"""

import os
import subprocess
import shlex


# VULNERABILITY: Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ROOT_PASSWORD = "root_pass_456"


class AdminTools:
    """Administrative tools with command injection vulnerabilities"""

    def __init__(self):
        # VULNERABILITY: Hardcoded credentials
        self.admin_token = "admin_token_xyz123"
        self.api_secret = "secret_api_key_789"

    def execute_system_command(self, command):
        """VULNERABILITY: Direct command execution"""
        # No validation or sanitization
        result = os.system(command)
        return result

    def run_diagnostic(self, host):
        """VULNERABILITY: Command injection via ping"""
        # User input directly in command
        cmd = f"ping -c 4 {host}"
        output = subprocess.check_output(cmd, shell=True)
        return output.decode()

    def check_disk_usage(self, path):
        """VULNERABILITY: Command injection in disk check"""
        # Path not validated
        cmd = f"du -sh {path}"
        result = os.popen(cmd).read()
        return result

    def search_logs(self, pattern):
        """VULNERABILITY: Command injection via grep"""
        # Pattern can contain malicious commands
        cmd = f"grep -r '{pattern}' /var/log/"
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return output.decode()

    def backup_database(self, db_name):
        """VULNERABILITY: Command injection in backup"""
        # db_name not sanitized
        backup_file = f"/backups/{db_name}.sql"
        cmd = f"mysqldump -u root -p{ROOT_PASSWORD} {db_name} > {backup_file}"

        os.system(cmd)
        return backup_file

    def restart_service(self, service_name):
        """VULNERABILITY: Command injection in service management"""
        cmd = f"systemctl restart {service_name}"
        return subprocess.call(cmd, shell=True)

    def kill_process(self, process_name):
        """VULNERABILITY: Command injection via pkill"""
        cmd = f"pkill -9 {process_name}"
        os.system(cmd)

    def compress_files(self, directory, output_file):
        """VULNERABILITY: Command injection with multiple parameters"""
        # Both parameters can be exploited
        cmd = f"tar -czf {output_file} {directory}"
        subprocess.call(cmd, shell=True)

    def get_user_info(self, username):
        """VULNERABILITY: Command injection via finger/id"""
        cmd = f"id {username}"
        output = subprocess.check_output(cmd, shell=True)
        return output.decode()

    def download_file(self, url):
        """VULNERABILITY: Command injection via wget/curl"""
        # URL not validated, can contain command injection
        cmd = f"wget {url} -O /tmp/downloaded_file"
        os.system(cmd)

    def schedule_task(self, time, command):
        """VULNERABILITY: Command injection in cron/at"""
        # Scheduling arbitrary commands
        cmd = f"echo '{command}' | at {time}"
        subprocess.call(cmd, shell=True)

    def change_permissions(self, file_path, permissions):
        """VULNERABILITY: Command injection in chmod"""
        cmd = f"chmod {permissions} {file_path}"
        os.system(cmd)

    def add_user(self, username, password):
        """VULNERABILITY: Command injection in user creation"""
        # VULNERABILITY: Also exposes password in command
        cmd = f"useradd {username} -p {password}"
        subprocess.call(cmd, shell=True)

    def send_email(self, recipient, subject, body):
        """VULNERABILITY: Command injection via mail command"""
        cmd = f"echo '{body}' | mail -s '{subject}' {recipient}"
        os.system(cmd)

    def check_network(self, interface):
        """VULNERABILITY: Command injection in ifconfig"""
        cmd = f"ifconfig {interface}"
        output = subprocess.check_output(cmd, shell=True)
        return output.decode()


def run_shell_command(user_command):
    """VULNERABILITY: Direct shell execution of user input"""
    # Extremely dangerous - executes any command
    output = subprocess.check_output(user_command, shell=True, stderr=subprocess.STDOUT)
    return output.decode()


def execute_script(script_path, *args):
    """VULNERABILITY: Script execution with arguments"""
    # No validation on script path or arguments
    cmd = f"{script_path} {' '.join(args)}"
    os.system(cmd)


def tail_log(log_file, lines=10):
    """VULNERABILITY: Command injection via tail"""
    cmd = f"tail -n {lines} {log_file}"
    output = subprocess.check_output(cmd, shell=True)
    return output.decode()


def find_files(directory, pattern):
    """VULNERABILITY: Command injection in find"""
    cmd = f"find {directory} -name '{pattern}'"
    output = subprocess.check_output(cmd, shell=True)
    return output.decode()


def git_clone_repo(repo_url, destination):
    """VULNERABILITY: Command injection via git clone"""
    cmd = f"git clone {repo_url} {destination}"
    subprocess.call(cmd, shell=True)


def process_csv(input_file, output_file):
    """VULNERABILITY: Command injection in file processing"""
    # Using awk/sed with user input
    cmd = f"awk -F',' '{{print $1}}' {input_file} > {output_file}"
    os.system(cmd)


def convert_image(input_image, output_image, format):
    """VULNERABILITY: Command injection in ImageMagick"""
    cmd = f"convert {input_image} -format {format} {output_image}"
    subprocess.call(cmd, shell=True)


class DatabaseAdmin:
    """Database admin with injection vulnerabilities"""

    def __init__(self):
        # VULNERABILITY: Hardcoded DB credentials
        self.db_user = "dbadmin"
        self.db_pass = "dbpass123"

    def run_sql_file(self, sql_file):
        """VULNERABILITY: Command injection in SQL execution"""
        cmd = f"mysql -u {self.db_user} -p{self.db_pass} < {sql_file}"
        os.system(cmd)

    def export_table(self, table_name, output_file):
        """VULNERABILITY: Command injection in data export"""
        cmd = f"mysql -u {self.db_user} -p{self.db_pass} -e 'SELECT * FROM {table_name}' > {output_file}"
        subprocess.call(cmd, shell=True)


class ServerManager:
    """Server management with vulnerabilities"""

    def deploy_app(self, app_name, version):
        """VULNERABILITY: Command injection in deployment"""
        cmd = f"docker run -d --name {app_name} app:{version}"
        subprocess.call(cmd, shell=True)

    def view_container_logs(self, container_id):
        """VULNERABILITY: Command injection in docker logs"""
        cmd = f"docker logs {container_id}"
        output = subprocess.check_output(cmd, shell=True)
        return output.decode()

    def stop_container(self, container_name):
        """VULNERABILITY: Command injection in docker stop"""
        cmd = f"docker stop {container_name} && docker rm {container_name}"
        os.system(cmd)


if __name__ == '__main__':
    admin = AdminTools()
    print("Admin tools loaded with vulnerabilities")
    print(f"Admin token: {admin.admin_token}")
