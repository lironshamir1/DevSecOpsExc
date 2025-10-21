# Contributing to DevSecOps Practice Repository

This repository is designed for educational purposes to practice identifying and fixing security vulnerabilities. Here's how to use it effectively.

## Getting Started

### 1. Fork and Clone the Repository

```bash
git fork https://github.com/your-org/DevSecOpsExc
git clone https://github.com/your-username/DevSecOpsExc
cd DevSecOpsExc
```

### 2. Set Up Your Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install bandit safety pytest pytest-cov pylint flake8
```

### 3. Configure Your Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your own values
nano .env
```

### 4. Run Initial Scans

Before fixing anything, run the security scans to see all the issues:

```bash
# Run Bandit
bandit -r . -f json -o bandit-report.json
bandit -r . -f txt

# Check for vulnerable dependencies
safety check

# Run code quality checks
pylint *.py
flake8 .

# Run tests
pytest tests/ -v
```

## Practice Workflow

### Step 1: Choose a Vulnerability Category

Pick one category from the README to focus on:

1. Hardcoded Secrets
2. SQL Injection
3. Command Injection
4. Insecure Cryptography
5. Path Traversal
6. Insecure Deserialization
7. Vulnerable Dependencies
8. Missing Security Headers
9. Code Quality Issues
10. Information Disclosure

### Step 2: Create a Feature Branch

```bash
git checkout -b fix/sql-injection
```

### Step 3: Fix the Vulnerabilities

- Identify the vulnerable code
- Research the proper fix
- Implement the solution
- Test your fix

### Step 4: Verify Your Fix

```bash
# Run security scans again
bandit -r . -f txt

# Run tests
pytest tests/ -v

# Check code quality
pylint *.py
```

### Step 5: Commit and Push

```bash
git add .
git commit -m "Fix SQL injection vulnerabilities in database.py"
git push origin fix/sql-injection
```

### Step 6: Create a Pull Request

Create a PR to your main branch and check if the CI/CD pipeline passes.

## Validation Checklist

Before considering your fixes complete, ensure:

- [ ] All Bandit high-severity issues are resolved
- [ ] Safety reports no vulnerable dependencies
- [ ] All tests pass
- [ ] Code quality scores improved
- [ ] No secrets in code
- [ ] Documentation updated if needed
- [ ] CI/CD pipeline passes

## Challenge Levels

### Level 1: Beginner
Start with these easier fixes:
- Hardcoded secrets
- Vulnerable dependencies
- Information disclosure
- Missing .gitignore entries

### Level 2: Intermediate
Move to these moderate challenges:
- SQL injection
- Path traversal
- Code quality issues
- Security headers

### Level 3: Advanced
Tackle the harder vulnerabilities:
- Command injection
- Insecure cryptography
- Insecure deserialization
- SSTI (Server-Side Template Injection)

## Testing Your Fixes Locally

### Run the Vulnerable App (Before Fixes)

```bash
# Initialize database
python database.py

# Run the app
python app.py

# Test an endpoint
curl http://localhost:5000/
```

### Test Security Vulnerabilities

**SQL Injection Test:**
```bash
# This should work on vulnerable version
curl "http://localhost:5000/user/admin'%20OR%20'1'='1"
```

**Command Injection Test:**
```bash
# This should work on vulnerable version
curl "http://localhost:5000/search?q=test;cat%20/etc/passwd"
```

### Verify Fixes Work

After implementing fixes, ensure:
1. Legitimate requests still work
2. Exploit attempts are blocked
3. Proper error messages are returned
4. No sensitive information is leaked

## CI/CD Integration

### Setting Up SonarQube

1. Install SonarQube locally or use a cloud instance
2. Create a project in SonarQube
3. Get your project token
4. Add secrets to GitHub:
   - `SONAR_TOKEN`
   - `SONAR_HOST_URL`

### Setting Up Prisma Cloud

1. Get Prisma Cloud access credentials
2. Add secrets to GitHub:
   - `PRISMA_API_URL`
   - `PRISMA_ACCESS_KEY`
   - `PRISMA_SECRET_KEY`

### Running the Full Pipeline

```bash
# Push to your branch
git push origin your-branch-name

# GitHub Actions will automatically:
# 1. Run Bandit security scan
# 2. Run Safety dependency check
# 3. Run SonarQube analysis
# 4. Run tests with coverage
# 5. Run Prisma Cloud scan (if configured)
# 6. Check quality gates
```

## Common Mistakes to Avoid

### ❌ Don't Do This:
- Don't just delete vulnerable code without replacing it with secure alternatives
- Don't disable security checks to make the pipeline pass
- Don't commit .env files
- Don't remove security tools from requirements.txt
- Don't skip writing tests for your fixes

### ✅ Do This Instead:
- Replace vulnerable code with secure implementations
- Fix the root cause, not the symptom
- Add environment variables for secrets
- Keep security tools in requirements.txt
- Write tests that verify security fixes work

## Learning Resources

### Recommended Reading
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Flask Security Guide](https://flask.palletsprojects.com/en/latest/security/)
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices-cheat-sheet/)

### Tools Documentation
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Safety Documentation](https://pyup.io/safety/)
- [SonarQube Python Analysis](https://docs.sonarqube.org/latest/analysis/languages/python/)
- [Prisma Cloud Docs](https://docs.paloaltonetworks.com/prisma/prisma-cloud)

### Video Tutorials
- Search for "Python Security" on YouTube
- OWASP video series
- Python security conference talks

## Progress Tracking

Keep track of your progress:

```markdown
## My Progress

- [x] Hardcoded Secrets - Fixed in commit abc123
- [x] SQL Injection - Fixed in commit def456
- [ ] Command Injection - In progress
- [ ] Insecure Cryptography - Not started
- [ ] Path Traversal - Not started
- [ ] Insecure Deserialization - Not started
- [ ] Vulnerable Dependencies - Not started
- [ ] Missing Security Headers - Not started
- [ ] Code Quality Issues - Not started
- [ ] Information Disclosure - Not started
```

## Getting Help

If you're stuck:

1. Check the `SOLUTIONS.md` file for hints
2. Review the security tool output for clues
3. Research the specific vulnerability type
4. Look at the OWASP documentation
5. Check similar security issues on GitHub

## Completing the Exercise

Once you've fixed all vulnerabilities:

1. All security scans should pass
2. CI/CD pipeline should be green
3. Code quality scores should improve
4. Tests should all pass
5. No secrets in the repository

## Next Steps

After completing the Python repository:

1. Try the .NET version (coming soon)
2. Try the JavaScript version (coming soon)
3. Build your own secure application
4. Contribute to real open-source security projects

## Questions?

This is a learning repository. If you have questions or suggestions:

1. Open an issue
2. Share your learning experience
3. Suggest additional vulnerabilities to include
4. Contribute improvements to the documentation

---

**Remember:** This repository contains intentional vulnerabilities. NEVER use this code in production or any real application!

Happy learning! 🔐
