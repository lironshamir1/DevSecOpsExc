# DevSecOps Practice Repository - Python

Intentionally vulnerable Python/Flask application for practicing DevSecOps security scanning and remediation with OpenShift deployment.

> **Note:** This repository also includes [.NET](../dotnet/) and [Node.js](../nodejs/) versions. [See main README](../README.md) for all languages.

## Purpose

This is a training repository that contains multiple security vulnerabilities and code quality issues. The CI/CD pipeline is configured to fail when these issues are detected by:
- **SonarQube** - Code quality and security analysis
- **Prisma Cloud** - Container and IaC security scanning


**Deployment Platform**: OpenShift (Red Hat)
**Secret Management**: Environment Variables

## The Challenge

1. Fork or clone this repository
2. Run the CI/CD pipeline - it will **FAIL** due to security issues
3. Fix the vulnerabilities one by one
4. Push your changes and verify the pipeline passes
5. Learn DevSecOps best practices along the way!

## Intentional Vulnerabilities Included

This repository contains the following categories of security issues:

### 1. **Hardcoded Secrets**
- Database credentials in source code
- API keys embedded in code
- Hardcoded encryption keys

### 2. **SQL Injection**
- Unsafe database queries using string concatenation
- Missing input validation

### 3. **Command Injection**
- Unsafe use of `os.system()` and `subprocess` with user input
- Missing input sanitization

### 4. **Insecure Cryptography**
- Use of weak hashing algorithms (MD5, SHA1)
- Insecure password storage
- Weak encryption methods

### 5. **Path Traversal**
- Unsafe file operations with user-controlled input
- Missing path validation

### 6. **Insecure Deserialization**
- Using `pickle` with untrusted data
- Unsafe YAML loading

### 7. **Vulnerable Dependencies**
- Outdated packages with known CVEs
- Insecure package versions

### 8. **Missing Security Headers**
- No CSRF protection
- Missing security headers
- Insecure session configuration

### 9. **Code Quality Issues**
- High complexity functions
- Code duplication
- Poor error handling

### 10. **Information Disclosure**
- Debug mode enabled in production
- Verbose error messages
- Exposed internal paths

## Getting Started

### Prerequisites
```bash
# Install Python 3.8+
python3 --version

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run the vulnerable application (DO NOT USE IN PRODUCTION!)
python app.py
```

### Deploying to OpenShift

```bash
# Login to OpenShift
oc login https://openshift.example.com

# Create new project
oc new-project devsecops-practice

# Deploy the vulnerable application
oc apply -f openshift/deployment-config.yml

# Build from source
oc apply -f openshift/build-config.yml
oc start-build vulnerable-app

# View logs
oc logs -f dc/vulnerable-app
```

## CI/CD Pipeline

The GitHub Actions pipeline (`.github/workflows/security-scan.yml`) includes:

1. **SonarQube Scan** - Code quality and security analysis
2. **Prisma Cloud Scan** - Container image and IaC scanning
3. **Unit Tests** - pytest with coverage

### Required GitHub Secrets

```
SONAR_TOKEN=<your-sonarqube-token>
SONAR_HOST_URL=<your-sonarqube-url>

PRISMA_API_URL=<your-prisma-cloud-api-url>
PRISMA_ACCESS_KEY=<your-prisma-access-key>
PRISMA_SECRET_KEY=<your-prisma-secret-key>
```

All scans must pass for the pipeline to succeed.

## How to Fix the Issues

See `SOLUTIONS.md` for detailed explanations and fixes for each vulnerability category. Try to fix them yourself first before checking the solutions!

### Recommended Fix Order

1. Start with **hardcoded secrets** - move to environment variables
2. Fix **SQL injection** - use parameterized queries
3. Fix **command injection** - validate and sanitize inputs
4. Update **vulnerable dependencies** - upgrade to secure versions
5. Fix **cryptography issues** - use strong algorithms
6. Add **input validation** - validate all user inputs
7. Improve **code quality** - refactor complex functions
8. Add **security headers** - implement proper security controls

## Repository Structure

```
.
├── app.py                              # Vulnerable Flask application
├── database.py                         # Database operations
├── crypto_utils.py                     # Cryptography utilities
├── file_handler.py                     # File operations
├── admin.py                            # Admin functions
├── requirements.txt                    # Dependencies
├── Dockerfile                          # Vulnerable container image
├── Dockerfile.secure                   # Secure OpenShift-compatible image
├── docker-compose.yml                  # Local development environment
├── openshift/
│   ├── deployment-config.yml           # OpenShift deployment (vulnerable)
│   ├── deployment-config-secure.yml    # Secure deployment
│   └── build-config.yml                # OpenShift build configuration
├── tests/
│   └── test_app.py                     # Unit tests
├── .github/
│   └── workflows/
│       └── security-scan.yml           # CI/CD pipeline (SonarQube, Prisma)
├── sonar-project.properties            # SonarQube configuration
├── .env.example                        # Environment variables template
├── README.md                           # This file
├── SOLUTIONS.md                        # Fixes for all vulnerabilities
└── CONTRIBUTING.md                     # Exercise workflow guide
```

## Learning Objectives

By completing this exercise, you will learn:

- How to identify security vulnerabilities using SonarQube and Prisma Cloud
- How to deploy applications securely on OpenShift
- How to manage secrets securely using environment variables
- How to implement secure coding practices in Python
- How to configure CI/CD pipelines for DevSecOps
- How to run containers as non-root users
- How to write secure database queries
- How to handle user input safely
- How to fix dependency vulnerabilities
- How to implement security headers and rate limiting

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [SonarQube Python Analysis](https://docs.sonarqube.org/latest/analysis/languages/python/)
- [Prisma Cloud Documentation](https://docs.paloaltonetworks.com/prisma/prisma-cloud)
- [OpenShift Documentation](https://docs.openshift.com/)
- [Container Security Best Practices](https://cloud.google.com/architecture/best-practices-for-building-containers)

## Warning

**DO NOT deploy this application to production or any public environment!**

This code contains intentional security vulnerabilities for educational purposes only.

## Other Languages

This repository also includes **.NET/C#** and **Node.js/JavaScript** versions with the same vulnerability categories.

See the [main README](../README.md) for all languages.

## License

This is an educational repository for security training purposes.