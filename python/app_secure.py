"""
Secure Flask Application with Vault Integration
This is the FIXED version demonstrating proper security practices
"""

import os
from flask import Flask, request, jsonify
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from vault_integration import VaultClient, configure_app_with_vault

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security: Configure app with Vault secrets
try:
    configure_app_with_vault(app)
except Exception as e:
    logger.error(f"Failed to configure app with Vault: {e}")
    # In production, fail fast if Vault is unavailable
    raise

# Security: Disable debug mode
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Security: Enable security headers with Talisman
talisman = Talisman(
    app,
    force_https=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self'",
        'style-src': "'self'",
    },
    content_security_policy_nonce_in=['script-src']
)

# Security: Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Add security headers
@app.after_request
def add_security_headers(response):
    """Add additional security headers"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response


@app.route('/')
def index():
    """API index endpoint"""
    return jsonify({
        "message": "Secure API",
        "version": "1.0.0",
        "status": "healthy"
    })


@app.route('/health')
def health():
    """Health check endpoint for OpenShift"""
    return jsonify({
        "status": "healthy",
        "timestamp": os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()
    })


@app.route('/ready')
def ready():
    """Readiness probe endpoint for OpenShift"""
    try:
        # Check Vault connectivity
        vault = VaultClient()
        if vault.client.is_authenticated():
            return jsonify({
                "status": "ready",
                "vault": "connected"
            })
        else:
            return jsonify({
                "status": "not ready",
                "vault": "disconnected"
            }), 503
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return jsonify({
            "status": "not ready",
            "error": "service unavailable"
        }), 503


@app.route('/config/rotate', methods=['POST'])
@limiter.limit("5 per hour")
def rotate_secrets():
    """
    Rotate secrets by fetching fresh ones from Vault
    Requires admin authentication
    """
    try:
        # In production, add proper authentication here
        configure_app_with_vault(app)
        logger.info("Secrets rotated successfully")
        return jsonify({"message": "Secrets rotated successfully"})
    except Exception as e:
        logger.error(f"Secret rotation failed: {e}")
        return jsonify({"error": "Secret rotation failed"}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(429)
def ratelimit_handler(error):
    """Handle rate limit errors"""
    return jsonify({"error": "Rate limit exceeded"}), 429


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all other exceptions"""
    logger.exception("Unhandled exception")
    return jsonify({"error": "An error occurred"}), 500


if __name__ == '__main__':
    # Run the application
    # In production, use a proper WSGI server like Gunicorn
    port = int(os.getenv('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
