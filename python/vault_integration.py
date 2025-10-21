"""
HashiCorp Vault Integration for Secret Management
This module demonstrates how to securely retrieve secrets from Vault
"""

import os
import hvac
from functools import lru_cache


class VaultClient:
    """HashiCorp Vault client for secret management"""

    def __init__(self, vault_url=None, vault_token=None, vault_role=None):
        """
        Initialize Vault client

        Args:
            vault_url: Vault server URL (default: from VAULT_ADDR env)
            vault_token: Vault token (default: from VAULT_TOKEN env)
            vault_role: Vault role for Kubernetes auth (default: from VAULT_ROLE env)
        """
        self.vault_url = vault_url or os.getenv('VAULT_ADDR', 'http://vault:8200')
        self.vault_token = vault_token or os.getenv('VAULT_TOKEN')
        self.vault_role = vault_role or os.getenv('VAULT_ROLE', 'default')

        # Initialize client
        self.client = hvac.Client(url=self.vault_url)

        # Authenticate
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Vault using available method"""

        # Method 1: Token authentication (for development)
        if self.vault_token:
            self.client.token = self.vault_token
            if not self.client.is_authenticated():
                raise Exception("Vault authentication failed with token")
            return

        # Method 2: Kubernetes authentication (for OpenShift/K8s)
        try:
            with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as f:
                jwt = f.read()

            response = self.client.auth.kubernetes.login(
                role=self.vault_role,
                jwt=jwt
            )

            self.client.token = response['auth']['client_token']
            print("Successfully authenticated with Vault using Kubernetes auth")
            return
        except FileNotFoundError:
            print("Kubernetes service account token not found")
        except Exception as e:
            print(f"Kubernetes authentication failed: {e}")

        # Method 3: AppRole authentication
        app_role_id = os.getenv('VAULT_ROLE_ID')
        app_secret_id = os.getenv('VAULT_SECRET_ID')

        if app_role_id and app_secret_id:
            response = self.client.auth.approle.login(
                role_id=app_role_id,
                secret_id=app_secret_id
            )
            self.client.token = response['auth']['client_token']
            print("Successfully authenticated with Vault using AppRole")
            return

        raise Exception("No valid Vault authentication method available")

    @lru_cache(maxsize=128)
    def get_secret(self, secret_path, key=None):
        """
        Retrieve secret from Vault

        Args:
            secret_path: Path to secret in Vault (e.g., 'secret/data/myapp/config')
            key: Specific key to retrieve (optional)

        Returns:
            Secret value(s)
        """
        try:
            # Read secret from Vault
            response = self.client.secrets.kv.v2.read_secret_version(
                path=secret_path.replace('secret/data/', ''),
                mount_point='secret'
            )

            secrets = response['data']['data']

            if key:
                return secrets.get(key)
            return secrets

        except Exception as e:
            print(f"Error retrieving secret from Vault: {e}")
            raise

    def get_database_credentials(self, db_path='database/creds/app-role'):
        """
        Get dynamic database credentials from Vault

        Args:
            db_path: Path to database role in Vault

        Returns:
            Dictionary with username and password
        """
        try:
            response = self.client.read(db_path)
            return {
                'username': response['data']['username'],
                'password': response['data']['password'],
                'lease_id': response['lease_id'],
                'lease_duration': response['lease_duration']
            }
        except Exception as e:
            print(f"Error retrieving database credentials: {e}")
            raise

    def renew_lease(self, lease_id):
        """Renew a Vault lease"""
        try:
            response = self.client.sys.renew_lease(lease_id)
            return response
        except Exception as e:
            print(f"Error renewing lease: {e}")
            raise

    def revoke_lease(self, lease_id):
        """Revoke a Vault lease"""
        try:
            self.client.sys.revoke_lease(lease_id)
            print(f"Successfully revoked lease: {lease_id}")
        except Exception as e:
            print(f"Error revoking lease: {e}")
            raise


class SecureConfig:
    """Configuration manager using Vault for secrets"""

    def __init__(self, vault_client=None):
        """Initialize secure configuration"""
        self.vault = vault_client or VaultClient()
        self._config = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from Vault"""
        try:
            # Load application secrets
            app_secrets = self.vault.get_secret('secure-app/config')

            self._config = {
                'SECRET_KEY': app_secrets.get('secret_key'),
                'API_KEY': app_secrets.get('api_key'),
                'DEBUG': False,
                'FLASK_ENV': 'production'
            }

            # Get database credentials
            db_creds = self.vault.get_database_credentials()
            self._config.update({
                'DB_USERNAME': db_creds['username'],
                'DB_PASSWORD': db_creds['password'],
                'DB_LEASE_ID': db_creds['lease_id']
            })

            print("Configuration loaded successfully from Vault")

        except Exception as e:
            print(f"Error loading configuration from Vault: {e}")
            # Fall back to environment variables (not recommended for production)
            self._load_from_env()

    def _load_from_env(self):
        """Fallback: Load from environment variables"""
        print("WARNING: Loading configuration from environment variables")
        self._config = {
            'SECRET_KEY': os.getenv('SECRET_KEY'),
            'API_KEY': os.getenv('API_KEY'),
            'DB_USERNAME': os.getenv('DB_USER'),
            'DB_PASSWORD': os.getenv('DB_PASSWORD'),
            'DEBUG': os.getenv('DEBUG', 'False') == 'True',
            'FLASK_ENV': os.getenv('FLASK_ENV', 'production')
        }

    def get(self, key, default=None):
        """Get configuration value"""
        return self._config.get(key, default)

    def __getitem__(self, key):
        """Get configuration value using dictionary syntax"""
        return self._config[key]


# Example usage for Flask application
def configure_app_with_vault(app):
    """
    Configure Flask application with Vault secrets

    Args:
        app: Flask application instance
    """
    try:
        # Initialize Vault client
        vault = VaultClient()

        # Get secrets from Vault
        secrets = vault.get_secret('secure-app/config')

        # Configure Flask app
        app.config['SECRET_KEY'] = secrets['secret_key']
        app.config['DEBUG'] = False
        app.config['TESTING'] = False

        # Get database credentials
        db_creds = vault.get_database_credentials()

        # Configure database connection
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"postgresql://{db_creds['username']}:{db_creds['password']}"
            f"@{os.getenv('DB_HOST', 'localhost')}:5432/appdb"
        )

        print("Application configured successfully with Vault")

    except Exception as e:
        print(f"Error configuring application with Vault: {e}")
        raise


# Example: Secure password retrieval
def get_secure_password(service_name):
    """
    Retrieve password securely from Vault

    Args:
        service_name: Name of the service

    Returns:
        Password string
    """
    vault = VaultClient()
    return vault.get_secret(f'passwords/{service_name}', 'password')


# Example: API key retrieval
def get_api_key(api_name):
    """
    Retrieve API key securely from Vault

    Args:
        api_name: Name of the API

    Returns:
        API key string
    """
    vault = VaultClient()
    return vault.get_secret(f'api-keys/{api_name}', 'key')


if __name__ == '__main__':
    # Example usage
    try:
        # Initialize Vault client
        vault = VaultClient()

        # Retrieve secrets
        secrets = vault.get_secret('secure-app/config')
        print("Retrieved secrets from Vault")

        # Get database credentials
        db_creds = vault.get_database_credentials()
        print(f"Database username: {db_creds['username']}")
        print(f"Lease ID: {db_creds['lease_id']}")

    except Exception as e:
        print(f"Error: {e}")
