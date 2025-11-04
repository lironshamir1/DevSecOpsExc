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
# Or use external secrets management solution
```
→ Secrets managed externally ✅

---

## Slide 10: Broken Access Control - Example

**What is it?**
Users can access resources or perform actions they shouldn't be allowed to

**Vulnerable Code:**
```python
@app.route('/admin/user/<user_id>')
def get_user_details(user_id):
    # No authorization check!
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    return jsonify(user)
```

**Attack:**
```
User with role "guest" accesses: /admin/user/1
→ Gets admin user details! 🚨
```

**Secure Code:**
```python
@app.route('/admin/user/<user_id>')
@require_role('admin')  # Authorization decorator
def get_user_details(user_id):
    if not current_user.is_admin:
        abort(403)
    user = db.query("SELECT * FROM users WHERE id = ?", (user_id,))
    return jsonify(user)
```
→ Proper authorization checks ✅

---

## Slide 11: Cryptographic Failures - Example

**What is it?**
Using weak or broken cryptographic algorithms

**Vulnerable Code:**
```python
import hashlib
from Crypto.Cipher import DES

# Weak hashing
password_hash = hashlib.md5(password.encode()).hexdigest()

# Weak encryption
cipher = DES.new(b'8bytekey', DES.MODE_ECB)
encrypted = cipher.encrypt(data)
```
→ MD5 is broken, DES is obsolete! 🚨

**Secure Code:**
```python
import bcrypt
from cryptography.fernet import Fernet

# Strong password hashing
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Strong encryption (AES-256)
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(data.encode())
```
→ Industry-standard algorithms ✅

---

## Slide 12: Insecure Design - Example

**What is it?**
Missing or ineffective security controls in the application design

**Vulnerable Design:**
```python
# Password reset without rate limiting
@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.json['email']
    token = generate_token()  # 6-digit numeric code
    send_email(email, token)
    return jsonify({"message": "Reset code sent"})
```
→ Attacker can brute-force 6-digit codes! 🚨

**Secure Design:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/reset-password', methods=['POST'])
@limiter.limit("3 per hour")  # Rate limiting
def reset_password():
    email = request.json['email']
    token = secrets.token_urlsafe(32)  # Cryptographically secure
    store_token_with_expiry(email, token, expires_in=15*60)  # 15 min
    send_email(email, token)
    return jsonify({"message": "Reset link sent"})
```
→ Rate limiting + strong tokens + expiration ✅

---

## Slide 13: Security Misconfiguration - Example

**What is it?**
Insecure default configurations, incomplete setups, or exposed debug info

**Vulnerable Configuration:**
```python
# Flask app in production
app = Flask(__name__)
app.config['DEBUG'] = True  # 🚨 Debug mode in production!
app.config['SECRET_KEY'] = 'dev'  # 🚨 Weak secret

# Dockerfile
FROM python:3.8
EXPOSE 5000
ENV FLASK_ENV=development  # 🚨
RUN chmod 777 /app  # 🚨 World-writable
```

**Secure Configuration:**
```python
# Flask app in production
app = Flask(__name__)
app.config['DEBUG'] = False  # ✅
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # ✅

# Dockerfile
FROM python:3.11-slim
EXPOSE 5000
ENV FLASK_ENV=production  # ✅
USER 1001  # ✅ Non-root user
RUN chmod 755 /app  # ✅ Proper permissions
```

---

## Slide 14: Vulnerable Dependencies - Example

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

## Slide 15: Authentication Failures - Example

**What is it?**
Broken authentication mechanisms allowing unauthorized access

**Vulnerable Code:**
```python
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    # No rate limiting, no account lockout
    user = db.query(f"SELECT * FROM users WHERE username='{username}'")
    if user and user['password'] == password:  # 🚨 Plain text!
        session['user_id'] = user['id']
        return jsonify({"success": True})
```
→ Brute-force possible, passwords in plain text! 🚨

**Secure Code:**
```python
from flask_limiter import Limiter
import bcrypt

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limiting
def login():
    username = request.json['username']
    password = request.json['password']

    user = db.query("SELECT * FROM users WHERE username=?", (username,))
    if user and bcrypt.checkpw(password.encode(), user['password_hash']):
        session.permanent = False  # Session timeout
        session['user_id'] = user['id']
        log_login_attempt(username, success=True)
        return jsonify({"success": True})

    log_login_attempt(username, success=False)
    return jsonify({"error": "Invalid credentials"}), 401
```
→ Rate limiting + hashed passwords + logging ✅

---

## Slide 16: Data Integrity Failures - Example

**What is it?**
Insecure deserialization leading to code execution

**Vulnerable Code:**
```python
import pickle
import yaml

# Pickle deserialization - RCE!
@app.route('/load-object', methods=['POST'])
def load_object():
    data = request.data
    obj = pickle.loads(data)  # 🚨 Attacker can execute code!
    return jsonify(obj)

# YAML deserialization
config = yaml.load(user_input)  # 🚨 Unsafe
```

**Attack:**
```python
# Attacker crafts malicious pickle
import pickle, os
class Exploit:
    def __reduce__(self):
        return (os.system, ('rm -rf /',))
payload = pickle.dumps(Exploit())
```

**Secure Code:**
```python
import json

@app.route('/load-object', methods=['POST'])
def load_object():
    data = request.data
    obj = json.loads(data)  # ✅ Safe serialization
    # Validate schema
    if not validate_schema(obj):
        abort(400)
    return jsonify(obj)

# Safe YAML loading
config = yaml.safe_load(user_input)  # ✅
```

---

## Slide 17: Logging & Monitoring Failures - Example

**What is it?**
Insufficient logging prevents detection of security incidents

**Vulnerable Code:**
```python
@app.route('/admin/delete-user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # No logging!
    db.execute(f"DELETE FROM users WHERE id = {user_id}")
    return jsonify({"success": True})

@app.route('/login', methods=['POST'])
def login():
    # Failed logins not logged
    if not authenticate(username, password):
        return jsonify({"error": "Invalid"}), 401
```
→ No audit trail, attacks go undetected! 🚨

**Secure Code:**
```python
import logging

logger = logging.getLogger(__name__)

@app.route('/admin/delete-user/<user_id>', methods=['DELETE'])
@require_role('admin')
def delete_user(user_id):
    logger.warning(f"User deletion attempt by {current_user.id} for user {user_id}")
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    logger.info(f"User {user_id} deleted by {current_user.id}")
    return jsonify({"success": True})

@app.route('/login', methods=['POST'])
def login():
    if not authenticate(username, password):
        logger.warning(f"Failed login attempt for user {username} from {request.remote_addr}")
        return jsonify({"error": "Invalid"}), 401
    logger.info(f"Successful login for user {username}")
```
→ Complete audit trail ✅

---

## Slide 18: Server-Side Request Forgery (SSRF) - Example

**What is it?**
Attacker forces server to make requests to unintended locations

**Vulnerable Code:**
```python
import requests

@app.route('/fetch-url', methods=['POST'])
def fetch_url():
    url = request.json['url']
    # No validation!
    response = requests.get(url)  # 🚨
    return response.text
```

**Attack:**
```
POST /fetch-url
{"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}
→ Access AWS metadata and steal credentials! 🚨
```

**Secure Code:**
```python
import requests
from urllib.parse import urlparse

ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']

@app.route('/fetch-url', methods=['POST'])
def fetch_url():
    url = request.json['url']

    # Validate URL
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        abort(400, "Invalid protocol")
    if parsed.hostname not in ALLOWED_DOMAINS:
        abort(400, "Domain not allowed")
    if parsed.hostname in ['localhost', '127.0.0.1', '169.254.169.254']:
        abort(400, "Internal IPs blocked")

    response = requests.get(url, timeout=5)
    return response.text
```
→ Whitelist validation + block internal IPs ✅

---

## Slide 19: Security Tools Overview

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

## Slide 20: Security Tools Overview (continued)

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

## Slide 21: The DevSecOps Workflow

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

## Slide 22: Your Practice Repository

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

## Slide 23: Repository Structure

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

## Slide 24: Exercise Workflow - Step by Step

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

## Slide 25: Exercise Workflow (continued)

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

## Slide 26: Exercise Workflow (continued)

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

## Slide 27: Exercise Workflow (continued)

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

## Slide 28: Example - Fixing SQL Injection

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

## Slide 29: Example - Fixing SQL Injection (continued)

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

## Slide 30: Tips for Success

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

## Slide 31: Common Mistakes to Avoid

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

## Slide 32: OpenShift Deployment

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

## Slide 33: Secrets Management

**Why It Matters?**
- Secrets should never be in source code
- Requires centralized and secure management
- Encryption at rest and in transit

**Recommended Approaches:**
- Environment Variables
- OpenShift Secrets
- Enterprise secrets management solutions (Vault, AWS Secrets Manager, Azure Key Vault)
- Kubernetes Secrets with encryption

**Benefits:**
- No hardcoded secrets
- Centralized secret management
- Audit trail for secret access
- Easy secret rotation

---

## Slide 34: Security Best Practices

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

## Slide 35: Security in Production

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

## Slide 36: Measuring Success

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

## Slide 37: Learning Resources

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

## Slide 38: Exercise Goals

By the end of this exercise, you will:

✅ Understand common security vulnerabilities
✅ Know how to use security scanning tools
✅ Be able to read and interpret security reports
✅ Fix vulnerabilities using secure coding practices
✅ Implement DevSecOps in CI/CD pipelines
✅ Deploy secure applications to OpenShift
✅ Use secure secrets management

**Remember:** Security is everyone's responsibility! 🔒

---

## Slide 39: Getting Help

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

## Slide 40: Let's Get Started!

**Pre-Exercise Checklist:**

□ GitHub account created
□ Git installed locally
□ Development environment set up:
  - Python 3.9+ OR
  - .NET 8.0 SDK OR
  - Node.js 18.x
□ Access to SonarQube instance
□ Access to Prisma Cloud console
□ OpenShift CLI installed (optional)
□ Repository forked/cloned

**Ready? Let's build secure applications! 🚀**

---

## Slide 41: Q&A

**Questions?**

---

## Slide 42: Additional Slides - Python Specific Vulnerabilities

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

## Slide 43: Additional Slides - .NET Specific Vulnerabilities

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

## Slide 44: Additional Slides - Node.js Specific Vulnerabilities

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

