# DevSecOps Practice Repository - .NET/C#

Intentionally vulnerable ASP.NET Core application for practicing DevSecOps security scanning and remediation with OpenShift deployment.

## Technology Stack

- **Framework**: ASP.NET Core 6.0
- **Language**: C# 10
- **Deployment**: OpenShift (Red Hat)
- **Secret Management**: HashiCorp Vault
- **Database**: SQL Server
- **Security Tools**: SonarQube and Prisma Cloud

## Security Vulnerabilities Included

This application contains the following intentional security issues:

1. **SQL Injection** - String concatenation in queries
2. **Command Injection** - Unsafe Process.Start() usage
3. **Hardcoded Secrets** - Passwords and API keys in code
4. **Insecure Deserialization** - TypeNameHandling.All in JSON.NET
5. **XXE (XML External Entity)** - Unsafe XML parsing
6. **Path Traversal** - Unvalidated file paths
7. **Weak Cryptography** - MD5, DES encryption
8. **Information Disclosure** - Exposing stack traces and internal details
9. **Vulnerable Dependencies** - Outdated NuGet packages
10. **Missing Security Headers** - No HTTPS redirect, CORS issues

## Getting Started

### Prerequisites

```bash
# Install .NET 6 SDK
dotnet --version

# Install OpenShift CLI
oc version

# Access to Vault
export VAULT_ADDR=https://vault.example.com:8200
```

### Running Locally

```bash
cd dotnet

# Restore dependencies
dotnet restore

# Run the application
dotnet run

# Application will start on http://localhost:5000
```

### Building

```bash
# Build
dotnet build

# Publish
dotnet publish -c Release
```

## API Endpoints

- `GET /api/user/{username}` - SQL injection vulnerability
- `POST /api/user/login` - Authentication with SQL injection
- `POST /api/admin/execute` - Command injection
- `POST /api/admin/deserialize` - Insecure deserialization
- `GET /api/file/read?filename=` - Path traversal
- `POST /api/file/upload` - Unrestricted file upload

## Deploying to OpenShift

```bash
# Login to OpenShift
oc login https://openshift.example.com

# Create project
oc new-project devsecops-dotnet

# Deploy
oc apply -f openshift/deployment-config.yml

# Build from source
oc new-app dotnet:6.0~https://github.com/your-org/DevSecOpsExc \
  --context-dir=dotnet \
  --name=vulnerable-dotnet-app
```

## CI/CD Pipeline

The pipeline includes:

1. **SonarQube** - Code quality and security
3. **Prisma Cloud** - Container security

### Required Secrets

```
SONAR_TOKEN
SONAR_HOST_URL
PRISMA_API_URL
PRISMA_ACCESS_KEY
PRISMA_SECRET_KEY
```

## Security Scanning

```bash
# SonarQube scan
dotnet sonarscanner begin /k:"dotnet-vulnerable"
dotnet build
dotnet sonarscanner end

# Run locally
dotnet build
```

## Common Vulnerabilities

### SQL Injection Example

```csharp
// VULNERABLE
var query = $"SELECT * FROM Users WHERE Username = '{username}'";

// SECURE
var query = "SELECT * FROM Users WHERE Username = @Username";
command.Parameters.AddWithValue("@Username", username);
```

### Command Injection Example

```csharp
// VULNERABLE
Process.Start("cmd.exe", $"/c {userInput}");

// SECURE
// Use Process.Start() with argument array and validation
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [.NET Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html)
- [SonarQube C# Analysis](https://docs.sonarqube.org/latest/analysis/languages/csharp/)

## Warning

**DO NOT use this code in production!** This application contains intentional security vulnerabilities for educational purposes only.
