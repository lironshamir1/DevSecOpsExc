# VULNERABLE Dockerfile - DO NOT USE IN PRODUCTION
# This Dockerfile contains intentional security issues for training

# VULNERABILITY: Using outdated base image
FROM python:3.8

# VULNERABILITY: Running as root (no USER directive)

# VULNERABILITY: Hardcoded secrets in build args
ARG SECRET_KEY=hardcoded-secret-123
ARG API_KEY=api-key-xyz-789

# Set working directory
WORKDIR /app

# VULNERABILITY: Copying everything including sensitive files
COPY . /app

# VULNERABILITY: Installing with pip as root
RUN pip install --no-cache-dir -r requirements.txt

# VULNERABILITY: Exposing secrets as environment variables
ENV SECRET_KEY=$SECRET_KEY
ENV API_KEY=$API_KEY
ENV DEBUG=True

# VULNERABILITY: Installing unnecessary packages
RUN apt-get update && \
    apt-get install -y \
    vim \
    curl \
    wget \
    netcat \
    telnet \
    && rm -rf /var/lib/apt/lists/*

# VULNERABILITY: Wide open permissions
RUN chmod 777 /app

# VULNERABILITY: Exposing non-standard port without documentation
EXPOSE 5000

# VULNERABILITY: Running application as root
CMD ["python", "app.py"]

# Additional vulnerabilities:
# - No health check
# - No volume for data persistence
# - No security scanning
# - Outdated Python version
# - No multi-stage build
# - Large image size
# - Unnecessary packages installed
