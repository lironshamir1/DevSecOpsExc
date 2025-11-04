# DevSecOps Practice Repository - Node.js/JavaScript

Intentionally vulnerable Node.js/Express application for practicing DevSecOps security scanning and remediation with OpenShift deployment.

## Technology Stack

- **Runtime**: Node.js 18.x
- **Framework**: Express.js 4.x
- **Language**: JavaScript ES6+
- **Deployment**: OpenShift (Red Hat)
- **Secret Management**: HashiCorp Vault
- **Database**: MySQL, MongoDB
- **Security Tools**: SonarQube and Prisma Cloud

## Security Vulnerabilities Included

This application contains the following intentional security issues:

1. **SQL Injection** - String concatenation in MySQL queries
2. **NoSQL Injection** - Unvalidated MongoDB queries
3. **Command Injection** - Unsafe exec() and eval() usage
4. **Hardcoded Secrets** - API keys and passwords in code
5. **Insecure Deserialization** - Unsafe YAML parsing
6. **XXE (XML External Entity)** - Vulnerable XML parsing
7. **Path Traversal** - Unvalidated file paths
8. **Weak Cryptography** - MD5 hashing for passwords
9. **Code Injection** - Use of eval() with user input
10. **Information Disclosure** - Exposing error details and stack traces
11. **Vulnerable Dependencies** - Outdated npm packages with CVEs
12. **Missing Security Headers** - No helmet configuration
13. **Session Management Issues** - Insecure session configuration

## Getting Started

### Prerequisites

```bash
# Install Node.js 18+
node --version
npm --version

# Install OpenShift CLI
oc version
```

### Running Locally

```bash
cd nodejs

# Install dependencies
npm install

# Run the application
npm start

# Application will start on http://localhost:3000
```

### Development Mode

```bash
# Run with auto-reload
npm run dev
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/user/:username` - SQL injection vulnerability
- `POST /api/user/login` - Authentication with SQLi and weak crypto
- `POST /api/admin/execute` - Command injection
- `POST /api/admin/eval` - Code injection via eval()
- `GET /api/file/read?filename=` - Path traversal
- `POST /api/file/write` - Unrestricted file write
- `POST /api/admin/yaml` - Unsafe YAML deserialization
- `POST /api/admin/xml` - XXE vulnerability

## Deploying to OpenShift

```bash
# Login to OpenShift
oc login https://openshift.example.com

# Create project
oc new-project devsecops-nodejs

# Deploy from Git
oc new-app nodejs:18~https://github.com/your-org/DevSecOpsExc \
  --context-dir=nodejs \
  --name=vulnerable-nodejs-app

# Expose service
oc expose svc/vulnerable-nodejs-app
```

## CI/CD Pipeline

The pipeline includes:

1. **SonarQube** - Code quality and security analysis
3. **Prisma Cloud** - Container image security scanning

### Required GitHub Secrets

```
SONAR_TOKEN
SONAR_HOST_URL
PRISMA_API_URL
PRISMA_ACCESS_KEY
PRISMA_SECRET_KEY
```

## Security Scanning

```bash
# Install security tools
npm install -g snyk retire

# Scan for vulnerabilities
npm audit
snyk test
retire

# Run tests
npm test
```

## Common Vulnerabilities

### SQL Injection Example

```javascript
// VULNERABLE
const query = `SELECT * FROM users WHERE username = '${username}'`;

// SECURE
const query = 'SELECT * FROM users WHERE username = ?';
connection.query(query, [username], callback);
```

### Command Injection Example

```javascript
// VULNERABLE
exec(`ping ${host}`, callback);

// SECURE
const { spawn } = require('child_process');
const ping = spawn('ping', ['-c', '4', validatedHost]);
```

### eval() Injection Example

```javascript
// VULNERABLE
const result = eval(userCode);

// SECURE
// Don't use eval() with user input
// Use Function() with strict validation or sandboxing
```

## Vulnerable Dependencies

This `package.json` contains intentionally outdated packages with known CVEs:

- `express@4.17.1` - Outdated
- `lodash@4.17.19` - Prototype pollution
- `axios@0.21.1` - SSRF vulnerability
- `js-yaml@3.14.0` - Code execution
- `moment@2.29.1` - ReDoS
- And more...

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [npm Security](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities)

## Warning

**DO NOT use this code in production!** This application contains intentional security vulnerabilities for educational purposes only.

## Next Steps

After fixing vulnerabilities:
1. Update all dependencies to latest versions
2. Implement parameterized queries
3. Add input validation
4. Use Vault for secrets
5. Enable security headers
6. Implement proper error handling
7. Add authentication and authorization
8. Configure HTTPS
9. Set up rate limiting
10. Implement logging and monitoring
