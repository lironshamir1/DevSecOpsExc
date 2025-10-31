# DevSecOps Training Presentation
## Practical Security Vulnerability Detection and Remediation

---

## Slide 1: Title Slide

**DevSecOps Practice Workshop**
*Building Security into the Development Lifecycle*

- Hands-on vulnerability detection and remediation
- Industry-standard security tools
- Real-world scenarios

---

## Slide 2: Agenda

1. **What is DevSecOps?**
2. **Why Security Matters**
3. **Common Security Vulnerabilities (OWASP Top 10)**
4. **Security Tools Overview**
5. **The DevSecOps Workflow**
6. **Hands-on Practice - Repository Overview**
7. **Exercise Workflow**
8. **Best Practices & Tips**

---

## Slide 3: What is DevSecOps?

**DevSecOps = Development + Security + Operations**

Traditional approach:
```
Development → Testing → Security → Operations
```

DevSecOps approach:
```
Development + Security + Testing + Operations (integrated)
```

**Key Principle:** "Shift Security Left"
- Integrate security early in the development process
- Automate security testing
- Make security everyone's responsibility

---

## Slide 4: Why DevSecOps?

**The Problem:**
- 70% of security breaches are due to application vulnerabilities
- Average cost of a data breach: $4.45 million (2023)
- Traditional security testing is too late and too slow

**The Solution:**
- **Automated Security Scanning** - Find issues early
- **Continuous Monitoring** - Detect problems in real-time
- **Fast Feedback** - Developers fix issues immediately
- **Reduced Risk** - Less vulnerable code in production

---

## Slide 5: The Shift Left Concept

```
Traditional (Shift Right):
Plan → Code → Build → Test → Deploy → [Security Scan] ❌ Too Late!

DevSecOps (Shift Left):
Plan → [Security Review] → Code → [SAST] → Build → [SCA] →
Test → [DAST] → Deploy → [Monitor] ✅ Security at Every Stage!
```

**Benefits:**
- Find vulnerabilities early (cheaper to fix)
- Reduce technical security debt
- Faster time to market (no security bottlenecks)
- Better security posture

---

## Slide 6: OWASP Top 10 - 2021

The most critical web application security risks:

1. **Broken Access Control** - Users can act outside intended permissions
2. **Cryptographic Failures** - Weak or missing encryption
3. **Injection** - SQL, Command, LDAP injection attacks
4. **Insecure Design** - Missing security controls
5. **Security Misconfiguration** - Default passwords, unnecessary features
6. **Vulnerable Components** - Outdated libraries with known CVEs
7. **Authentication Failures** - Weak password policies, session issues
8. **Data Integrity Failures** - Insecure deserialization
9. **Logging & Monitoring Failures** - Insufficient audit trails
10. **Server-Side Request Forgery (SSRF)** - Force server to make requests

---

## Slide 7: SQL Injection - Example

**What is it?**
Attacker injects malicious SQL code through user input

**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
```

**Attack:**
```
username = "admin' OR '1'='1"
Result: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```
→ Returns all users! 🚨

**Secure Code:**
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```
→ Parameterized queries prevent injection ✅

---

## Slide 8: Command Injection - Example

**What is it?**
Attacker executes arbitrary system commands

**Vulnerable Code:**
```python
os.system(f"ping {host}")
```

**Attack:**
```
host = "google.com; rm -rf /"
Result: ping google.com; rm -rf /
```
→ Deletes all files! 🚨

**Secure Code:**
```python
subprocess.run(['ping', '-c', '4', validated_host], shell=False)
```
→ No shell interpretation ✅

---

## Slide 9: Hardcoded Secrets - Example

**What is it?**
Sensitive credentials stored in source code

**Vulnerable Code:**
```python
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "password123"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG"
```
→ Anyone with code access sees secrets! 🚨

**Secure Code:**
```python
import os
API_KEY = os.environ.get('API_KEY')
# Or use HashiCorp Vault
from vault_integration import VaultClient
vault = VaultClient()
API_KEY = vault.get_secret('app/api_key')
```
→ Secrets managed externally ✅

---

## Slide 10: Vulnerable Dependencies - Example

**What is it?**
Using libraries with known security vulnerabilities

**Example:**
```json
{
  "dependencies": {
    "lodash": "4.17.15",  // CVE-2019-10744 - Prototype Pollution
    "axios": "0.21.1",    // CVE-2021-3749 - SSRF
    "moment": "2.29.1"    // CVE-2022-31129 - ReDoS
  }
}
```

**Impact:**
- Remote Code Execution
- Data Theft
- Denial of Service

**Solution:**
- Keep dependencies updated
- Use security scanning tools
- Monitor CVE databases

---

## Slide 11: Security Tools Overview

### **1. SonarQube**
**Static Application Security Testing (SAST)**

What it does:
- Analyzes source code without running it
- Detects code quality issues
- Finds security vulnerabilities
- Tracks technical debt

Finds:
- SQL Injection
- Hardcoded secrets
- Weak cryptography
- Code smells

---

## Slide 12: Security Tools Overview (continued)

### **2. Prisma Cloud (Twistlock)**
**Container & Infrastructure Security**

What it does:
- Scans Docker images for vulnerabilities
- Analyzes Infrastructure as Code (IaC)
- Runtime protection
- Compliance checking

Finds:
- Vulnerable base images
- Misconfigured containers
- Exposed ports
- Insecure Dockerfile practices

---

## Slide 13: The DevSecOps Workflow

```
┌─────────────────────────────────────────────────┐
│  1. Developer writes code                       │
│     └─> Commits to Git                          │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│  2. CI/CD Pipeline Triggered                    │
│     ├─> Build application                       │
│     ├─> Run unit tests                          │
│     ├─> SonarQube scan (code analysis)          │
│     └─> Prisma Cloud scan (container)           │
└──────────────┬──────────────────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
┌─────▼──────┐   ┌──────▼──────┐
│ PASS ✅    │   │  FAIL ❌    │
│ Deploy     │   │  Fix Issues │
└────────────┘   └──────┬──────┘
                        │
                 ┌──────▼───────────────────────┐
                 │ 3. Developer reviews reports │
                 │    └─> Fixes vulnerabilities │
                 └──────┬───────────────────────┘
                        │
                 ┌──────▼──────────┐
                 │ 4. Commit fixes │
                 │    └─> Go to #2 │
                 └─────────────────┘
```

---

## Slide 14: Your Practice Repository

**Three Language Versions:**
- **Python** - Flask application
- **.NET/C#** - ASP.NET Core application
- **Node.js** - Express.js application

**Each contains 10+ vulnerability types:**
- SQL Injection
- Command Injection
- Hardcoded Secrets
- Weak Cryptography
- Path Traversal
- Insecure Deserialization
- XXE vulnerabilities
- Vulnerable Dependencies
- Information Disclosure
- Poor Code Quality

---

## Slide 15: Repository Structure

```
DevSecOpsExc/
├── python/           # Python/Flask vulnerable app
│   ├── app.py
│   ├── database.py
│   ├── crypto_utils.py
│   ├── openshift/    # OpenShift configs
│   └── .github/      # CI/CD pipeline
├── dotnet/           # .NET/C# vulnerable app
│   ├── Controllers/
│   ├── Services/
│   └── .github/      # CI/CD pipeline
└── nodejs/           # Node.js vulnerable app
    ├── routes/
    ├── server.js
    └── .github/      # CI/CD pipeline
```

---

## Slide 16: Exercise Workflow - Step by Step

**Step 1: Choose Your Language**
```bash
cd python   # or dotnet or nodejs
```

**Step 2: Run the Application Locally**
```bash
# Python
pip install -r requirements.txt
python app.py

# .NET
dotnet restore && dotnet run

# Node.js
npm install && npm start
```

---

## Slide 17: Exercise Workflow (continued)

**Step 3: Trigger CI/CD Pipeline**
```bash
git add .
git commit -m "Initial commit"
git push
```

**Result:** Pipeline will **FAIL** 🚨

**Step 4: Review Security Reports**
- Go to GitHub Actions
- View failed pipeline
- Download artifacts:
  - SonarQube report
  - Prisma Cloud report

---

## Slide 18: Exercise Workflow (continued)

**Step 5: Analyze Vulnerabilities**

Open reports and identify:
- **What** is the vulnerability?
- **Where** is it in the code?
- **Why** is it dangerous?
- **How** to fix it?

**Step 6: Fix Issues**
- Read `SOLUTIONS.md` for guidance (but try yourself first!)
- Update code with secure implementations
- Test fixes locally

---

## Slide 19: Exercise Workflow (continued)

**Step 7: Verify Fixes**
```bash
git add .
git commit -m "Fix SQL injection in user.py"
git push
```

**Step 8: Repeat Until All Pass**
- Pipeline should turn green ✅
- All security checks pass
- Application is secure

---

## Slide 20: Example - Fixing SQL Injection

**1. SonarQube Report Says:**
```
SQL Injection vulnerability in database.py line 42
Severity: CRITICAL
```

**2. Review the Code:**
```python
# Line 42 - database.py
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
```

**3. Identify the Problem:**
- String concatenation with user input
- No input validation
- Direct query execution

---

## Slide 21: Example - Fixing SQL Injection (continued)

**4. Apply the Fix:**
```python
def get_user(username):
    # Use parameterized query
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
```

**5. Verify:**
```bash
# Run tests
pytest tests/

# Commit and push
git add database.py
git commit -m "Fix SQL injection in get_user()"
git push
```

**6. Check Pipeline:**
- SonarQube scan: PASS ✅
- Prisma Cloud scan: PASS ✅

---

## Slide 22: Tips for Success

**1. Read the Error Messages**
- Security tools give detailed explanations
- They often include fix recommendations

**2. Use SOLUTIONS.md as Last Resort**
- Try to fix issues yourself first
- Learn by doing, not by copying

**3. Test Locally Before Pushing**
- Run the application
- Test the vulnerable endpoint
- Verify the fix works

**4. Fix One Category at a Time**
- Don't try to fix everything at once
- Start with critical issues first

---

## Slide 23: Common Mistakes to Avoid

❌ **Don't:**
- Delete vulnerable code without replacing it
- Disable security checks to make pipeline pass
- Copy solutions without understanding
- Ignore medium/low severity issues

✅ **Do:**
- Understand WHY code is vulnerable
- Implement proper fixes
- Add input validation
- Keep dependencies updated
- Use secure cryptography
- Follow the principle of least privilege

---

## Slide 24: OpenShift Deployment

**What is OpenShift?**
- Enterprise Kubernetes platform by Red Hat
- Container orchestration
- Built-in security features

**Your Repository Includes:**
- Deployment configurations
- Service definitions
- Route configurations
- Build configs for S2I (Source-to-Image)

**Deployment Command:**
```bash
oc login https://openshift.example.com
oc new-project devsecops-practice
oc apply -f openshift/deployment-config.yml
```

---

## Slide 25: HashiCorp Vault Integration

**What is Vault?**
- Secrets management platform
- Dynamic secrets generation
- Encryption as a service

**Your Repository Includes:**
- Vault client integration
- Kubernetes authentication
- Dynamic database credentials
- Secret rotation examples

**Benefits:**
- No hardcoded secrets
- Centralized secret management
- Audit trail for secret access
- Automatic secret rotation

---

## Slide 26: Security Best Practices

**Input Validation**
- Validate all user input
- Use whitelists, not blacklists
- Sanitize data before use

**Authentication & Authorization**
- Strong password policies
- Multi-factor authentication
- Principle of least privilege

**Cryptography**
- Use industry-standard algorithms
- Never roll your own crypto
- Proper key management

**Dependencies**
- Keep libraries updated
- Monitor CVE databases
- Use dependency scanning tools

---

## Slide 27: Security in Production

**Defense in Depth**
Multiple layers of security:

1. **Application Level**
   - Input validation
   - Secure coding practices

2. **Infrastructure Level**
   - Container security
   - Network policies

3. **Platform Level**
   - OpenShift security features
   - Service mesh

4. **Monitoring Level**
   - Logging and auditing
   - Intrusion detection

---

## Slide 28: Measuring Success

**Key Metrics:**

1. **Vulnerability Detection Time**
   - Goal: < 1 hour after code commit

2. **Vulnerability Fix Time**
   - Goal: Critical issues < 24 hours
   - Goal: High issues < 7 days

3. **False Positive Rate**
   - Goal: < 10%

4. **Pipeline Pass Rate**
   - Goal: > 80% on first try (after training)

5. **Security Debt**
   - Goal: Zero critical/high issues in production

---

## Slide 29: Learning Resources

**Documentation:**
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
- SonarQube Docs: https://docs.sonarqube.org/
- Prisma Cloud Docs: https://docs.paloaltonetworks.com/prisma

**Practice:**
- OWASP WebGoat: https://owasp.org/www-project-webgoat/
- HackTheBox: https://www.hackthebox.com/
- TryHackMe: https://tryhackme.com/

**Communities:**
- OWASP Community
- DevSecOps Reddit
- Security Stack Exchange

---

## Slide 30: Exercise Goals

By the end of this exercise, you will:

✅ Understand common security vulnerabilities
✅ Know how to use security scanning tools
✅ Be able to read and interpret security reports
✅ Fix vulnerabilities using secure coding practices
✅ Implement DevSecOps in CI/CD pipelines
✅ Deploy secure applications to OpenShift
✅ Use Vault for secrets management

**Remember:** Security is everyone's responsibility! 🔒

---

## Slide 31: Getting Help

**During the Exercise:**

1. **Check SOLUTIONS.md** - Detailed fixes for each vulnerability
2. **Review Tool Documentation** - SonarQube and Prisma Cloud docs
3. **Ask Questions** - Your instructors are here to help
4. **Collaborate** - Discuss with teammates
5. **Search Online** - OWASP, Stack Overflow

**Repository Issues:**
- GitHub Issues: Report bugs or ask questions
- Documentation: All READMEs in each language folder

---

## Slide 32: Let's Get Started!

**Pre-Exercise Checklist:**

□ GitHub account created
□ Git installed locally
□ Development environment set up:
  - Python 3.9+ OR
  - .NET 6.0 SDK OR
  - Node.js 14.x
□ Access to SonarQube instance
□ Access to Prisma Cloud console
□ OpenShift CLI installed (optional)
□ Repository forked/cloned

**Ready? Let's build secure applications! 🚀**

---

## Slide 33: Q&A

**Questions?**

---

## Slide 34: Additional Slides - Python Specific Vulnerabilities

**Python-Specific Issues:**

1. **pickle Deserialization**
   ```python
   # Vulnerable
   import pickle
   obj = pickle.loads(user_data)  # 🚨 RCE possible

   # Secure
   import json
   obj = json.loads(user_data)  # ✅ Safe
   ```

2. **SSTI (Server-Side Template Injection)**
   ```python
   # Vulnerable
   return render_template_string(user_input)  # 🚨

   # Secure
   return render_template('template.html', data=user_input)  # ✅
   ```

---

## Slide 35: Additional Slides - .NET Specific Vulnerabilities

**.NET-Specific Issues:**

1. **TypeNameHandling.All**
   ```csharp
   // Vulnerable
   JsonConvert.DeserializeObject(data,
     new JsonSerializerSettings {
       TypeNameHandling = TypeNameHandling.All  // 🚨 RCE
     });

   // Secure
   JsonConvert.DeserializeObject<MyType>(data);  // ✅
   ```

2. **Process.Start with shell=true**
   ```csharp
   // Vulnerable
   Process.Start("cmd.exe", $"/c {userInput}");  // 🚨

   // Secure
   Process.Start(new ProcessStartInfo {
     FileName = "ping",
     Arguments = validatedHost,
     UseShellExecute = false  // ✅
   });
   ```

---

## Slide 36: Additional Slides - Node.js Specific Vulnerabilities

**Node.js-Specific Issues:**

1. **eval() with User Input**
   ```javascript
   // Vulnerable
   eval(userCode);  // 🚨 RCE

   // Secure
   // Don't use eval! Use safer alternatives or validation
   ```

2. **NoSQL Injection**
   ```javascript
   // Vulnerable
   db.users.find({ username: req.body.username });  // 🚨

   // Secure
   db.users.find({
     username: { $eq: String(req.body.username) }
   });  // ✅
   ```

3. **Prototype Pollution**
   ```javascript
   // Vulnerable - lodash < 4.17.21
   _.merge({}, userInput);  // 🚨

   // Secure - Update lodash to latest version
   ```

---

## Backup Slide: Timeline

**Suggested Exercise Timeline:**

- **Day 1 Morning:** Theory presentation (2 hours)
- **Day 1 Afternoon:** Setup and first vulnerabilities (3 hours)
- **Day 2 Morning:** Continue fixing vulnerabilities (3 hours)
- **Day 2 Afternoon:** OpenShift deployment and Vault (2 hours)
- **Day 3:** Advanced topics and wrap-up (1-2 hours)

Adjust based on your team's pace!

---

## Backup Slide: Scoring System (Optional)

**Gamification Idea:**

| Achievement | Points |
|-------------|--------|
| Fix Critical Vulnerability | 10 |
| Fix High Vulnerability | 7 |
| Fix Medium Vulnerability | 5 |
| Pipeline Passes | 20 |
| Deploy to OpenShift | 15 |
| Integrate Vault | 15 |
| Complete All Languages | 50 |

**Leaderboard:** Track progress across teams!

---

