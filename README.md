# DevSecOps Practice Repository - Multi-Language

Intentionally vulnerable applications in **Python**, **.NET/C#**, and **Node.js/JavaScript** for practicing DevSecOps security scanning and remediation with **OpenShift** deployment.

## 🎯 Purpose

Train developers to identify and fix security vulnerabilities using industry-standard tools:
- **SonarQube** - Code quality and security analysis
- **Prisma Cloud** - Container and infrastructure scanning

All applications are designed to **fail** CI/CD pipelines until vulnerabilities are fixed!

## 📁 Repository Structure

```
DevSecOpsExc/
├── python/          # Python/Flask vulnerable application
├── dotnet/          # .NET/C# ASP.NET Core vulnerable application
├── nodejs/          # Node.js/Express vulnerable application
└── README.md        # This file
```

## 🚀 Quick Start

### Choose Your Language

<table>
<tr>
<th>Python</th>
<th>.NET/C#</th>
<th>Node.js</th>
</tr>
<tr>
<td>

```bash
cd python
pip install -r requirements.txt
python app.py
```

</td>
<td>

```bash
cd dotnet
dotnet restore
dotnet run
```

</td>
<td>

```bash
cd nodejs
npm install
npm start
```

</td>
</tr>
<tr>
<td>http://localhost:5000</td>
<td>http://localhost:5000</td>
<td>http://localhost:3000</td>
</tr>
<tr>
<td><a href="python/README.md">Python README →</a></td>
<td><a href="dotnet/README.md">.NET README →</a></td>
<td><a href="nodejs/README.md">Node.js README →</a></td>
</tr>
</table>

## 🔒 Security Vulnerabilities Included

Each language version contains **the same vulnerability categories** adapted to the technology stack:

| Category | Python | .NET | Node.js |
|----------|--------|------|---------|
| **SQL Injection** | ✓ | ✓ | ✓ |
| **Command Injection** | ✓ | ✓ | ✓ |
| **Hardcoded Secrets** | ✓ | ✓ | ✓ |
| **Weak Cryptography** | ✓ | ✓ | ✓ |
| **Path Traversal** | ✓ | ✓ | ✓ |
| **Insecure Deserialization** | ✓ | ✓ | ✓ |
| **XXE** | ✓ | ✓ | ✓ |
| **Vulnerable Dependencies** | ✓ | ✓ | ✓ |
| **Information Disclosure** | ✓ | ✓ | ✓ |
| **Code Quality Issues** | ✓ | ✓ | ✓ |

### Language-Specific Vulnerabilities

**Python:**
- SSTI (Server-Side Template Injection)
- pickle deserialization
- unsafe `subprocess` usage

**.NET/C#:**
- TypeNameHandling.All (JSON.NET)
- Entity Framework injection
- unsafe `Process.Start()`

**Node.js:**
- NoSQL injection (MongoDB)
- `eval()` and `exec()` vulnerabilities
- Prototype pollution

## 🔧 Technology Stack

| Component | Python | .NET | Node.js |
|-----------|--------|------|---------|
| **Framework** | Flask | ASP.NET Core 6.0 | Express.js 4.x |
| **Runtime** | Python 3.9 | .NET 6.0 | Node.js 14.x |
| **Database** | SQLite/PostgreSQL | SQL Server | MySQL/MongoDB |
| **Secrets** | Environment Variables | Environment Variables | Environment Variables |
| **Deployment** | OpenShift | OpenShift | OpenShift |

## 🔍 Security Tools Integration

### SonarQube
- Static code analysis
- Security hotspot detection
- Code quality metrics
- Quality gate enforcement

### Prisma Cloud (Twistlock)
- Container image scanning
- Infrastructure as Code analysis
- Runtime protection
- Compliance checking

## 🏗️ Deployment to OpenShift

Each language has OpenShift deployment configurations:

```bash
# Python
oc apply -f python/openshift/deployment-config.yml

# .NET
oc new-app dotnet:6.0~. --context-dir=dotnet --name=vulnerable-dotnet-app

# Node.js
oc new-app nodejs:14~. --context-dir=nodejs --name=vulnerable-nodejs-app
```

## 📊 CI/CD Pipeline

Each language has a dedicated GitHub Actions workflow:

- `python/.github/workflows/security-scan.yml`
- `dotnet/.github/workflows/security-scan.yml`
- `nodejs/.github/workflows/security-scan.yml`

### Pipeline Steps:

1. **Build & Test** - Compile and run unit tests
2. **SonarQube Scan** - Code quality and security analysis
3. **Prisma Cloud Scan** - Container security scanning
4. **Quality Gate** - **FAILS** if vulnerabilities found

### Required GitHub Secrets:

```bash
SONAR_TOKEN=<your-sonarqube-token>
SONAR_HOST_URL=<your-sonarqube-url>

PRISMA_API_URL=<your-prisma-cloud-api-url>
PRISMA_ACCESS_KEY=<your-prisma-access-key>
PRISMA_SECRET_KEY=<your-prisma-secret-key>
```

## 🎓 Learning Path

### 1. Choose a Language
Pick the language you want to practice with (Python, .NET, or Node.js)

### 2. Run Locally
```bash
cd <language>
# Install dependencies
# Run the application
# Explore the vulnerable endpoints
```

### 3. Run Security Scans
```bash
# Push code to trigger CI/CD
git add .
git commit -m "Initial commit"
git push

# Pipeline will FAIL - review the scan results
```

### 4. Fix Vulnerabilities
- Review SonarQube findings
- Check Prisma Cloud reports
- Read the SOLUTIONS.md in each language folder
- Fix issues one by one

### 5. Verify Fixes
```bash
# Push fixes
git push

# Pipeline should PASS when all issues fixed ✅
```

## 📚 Documentation

Each language folder contains comprehensive documentation:

- **README.md** - Getting started guide
- **SOLUTIONS.md** - Detailed fixes for all vulnerabilities
- **CONTRIBUTING.md** - Exercise workflow

## ⚠️ Warning

**DO NOT deploy these applications to production or any public environment!**

This code contains **intentional security vulnerabilities** for educational purposes only.

## 🔗 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OpenShift Documentation](https://docs.openshift.com/)
- [SonarQube](https://docs.sonarqube.org/)
- [Prisma Cloud](https://docs.paloaltonetworks.com/prisma/prisma-cloud)

## 📄 License

Educational repository for security training purposes.

---

**Choose your language and start practicing DevSecOps! 🚀**

