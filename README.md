# DevSecOps Practice Repository - Python

This repository contains intentionally vulnerable Python code designed for practicing DevSecOps security scanning and remediation workflows.

## Purpose

This is a training repository that contains multiple security vulnerabilities and code quality issues. The CI/CD pipeline is configured to fail when these issues are detected by:
- **SonarQube** - Code quality and security analysis
- **Prisma Cloud** - Container and IaC security scanning
- **Bandit** - Python security linter
- **Safety** - Dependency vulnerability scanner

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

### Running Security Scans Locally

```bash
# Run Bandit for security issues
bandit -r . -f json -o bandit-report.json

# Check for vulnerable dependencies
safety check --json

# Run pytest
pytest tests/
```

## CI/CD Pipeline

The GitHub Actions pipeline (`.github/workflows/security-scan.yml`) includes:

1. **Code Quality Analysis** - SonarQube scan
2. **Security Scanning** - Bandit, Safety
3. **Container Scanning** - Prisma Cloud (Twistlock)
4. **Unit Tests** - pytest with coverage
5. **SAST Analysis** - Static Application Security Testing

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
├── app.py                          # Main vulnerable Flask application
├── database.py                     # Database operations (SQL injection)
├── crypto_utils.py                 # Cryptography utilities (weak crypto)
├── file_handler.py                 # File operations (path traversal)
├── admin.py                        # Admin functions (command injection)
├── requirements.txt                # Vulnerable dependencies
├── tests/                          # Unit tests
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── security-scan.yml       # CI/CD pipeline
├── sonar-project.properties        # SonarQube configuration
├── .bandit                         # Bandit configuration
├── README.md                       # This file
└── SOLUTIONS.md                    # Solutions and explanations
```

## Learning Objectives

By completing this exercise, you will learn:

- How to identify common security vulnerabilities in Python code
- How to use security scanning tools (SonarQube, Bandit, Safety)
- How to remediate security issues following best practices
- How to implement secure coding practices
- How to configure CI/CD pipelines for security
- How to use secrets management properly
- How to write secure database queries
- How to handle user input safely

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [SonarQube Python Analysis](https://docs.sonarqube.org/latest/analysis/languages/python/)
- [Prisma Cloud Documentation](https://docs.paloaltonetworks.com/prisma/prisma-cloud)

## Warning

**DO NOT deploy this application to production or any public environment!**

This code contains intentional security vulnerabilities for educational purposes only.

## Next Steps

Once you complete the Python repository:
- **.NET Repository** - Similar exercises in C#/.NET
- **JavaScript Repository** - Similar exercises in Node.js/JavaScript

## License

This is an educational repository for security training purposes.