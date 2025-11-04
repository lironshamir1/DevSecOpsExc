# מצגת הדרכה - DevSecOps
## זיהוי ותיקון פרצות אבטחה בפועל

---

## שקף 1: כותרת

**סדנת DevSecOps מעשית**
*שילוב אבטחה במחזור החיים של הפיתוח*

- זיהוי ותיקון פרצות אבטחה hands-on
- כלי אבטחה סטנדרטיים בתעשייה
- תרחישים מהעולם האמיתי

---

## שקף 2: סדר היום

1. **מה זה DevSecOps?**
2. **למה אבטחה חשובה**
3. **פרצות אבטחה נפוצות (OWASP Top 10)**
4. **סקירת כלי אבטחה**
5. **תהליך העבודה של DevSecOps**
6. **תרגול מעשי - סקירת הריפו**
7. **תהליך התרגיל**
8. **Best Practices וטיפים**

---

## שקף 3: מה זה DevSecOps?

**DevSecOps = Development + Security + Operations**

גישה מסורתית:
```
פיתוח → בדיקות → אבטחה → תפעול
```

גישת DevSecOps:
```
פיתוח + אבטחה + בדיקות + תפעול (משולב)
```

**עיקרון מרכזי:** "Shift Security Left"
- שילוב אבטחה מוקדם בתהליך הפיתוח
- אוטומציה של בדיקות אבטחה
- הפיכת אבטחה לאחריות של כולם

---

## שקף 4: למה DevSecOps?

**הבעיה:**
- 70% מהפריצות לאבטחה נובעות מפרצות באפליקציות
- עלות ממוצעת של פריצה: $4.45 מיליון (2023)
- בדיקות אבטחה מסורתיות מאוחרות מדי ואיטיות מדי

**הפתרון:**
- **סריקות אבטחה אוטומטיות** - גילוי בעיות מוקדם
- **ניטור רצוף** - זיהוי בעיות בזמן אמת
- **פידבק מהיר** - מפתחים מתקנים מיד
- **הפחתת סיכון** - פחות קוד פגיע בייצור

---

## שקף 5: קונספט Shift Left

```
מסורתי (Shift Right):
תכנון → קוד → בנייה → בדיקות → פריסה → [סריקת אבטחה] ❌ מאוחר מדי!

DevSecOps (Shift Left):
תכנון → [סקירת אבטחה] → קוד → [SAST] → בנייה → [SCA] →
בדיקות → [DAST] → פריסה → [ניטור] ✅ אבטחה בכל שלב!
```

**יתרונות:**
- גילוי פרצות מוקדם (זול יותר לתקן)
- הפחתת חוב אבטחה טכני
- זמן קצר יותר לשוק (ללא צווארי בקבוק של אבטחה)
- מצב אבטחה טוב יותר

---

## שקף 6: OWASP Top 10 - 2021

הסיכונים הקריטיים ביותר לאבטחת אפליקציות web:

1. **Broken Access Control** - משתמשים יכולים לפעול מעבר להרשאות
2. **Cryptographic Failures** - הצפנה חלשה או חסרה
3. **Injection** - התקפות SQL, Command, LDAP injection
4. **Insecure Design** - בקרות אבטחה חסרות
5. **Security Misconfiguration** - סיסמאות ברירת מחדל, פיצ'רים מיותרים
6. **Vulnerable Components** - ספריות מיושנות עם CVEs ידועים
7. **Authentication Failures** - מדיניות סיסמאות חלשה, בעיות session
8. **Data Integrity Failures** - deserialization לא מאובטח
9. **Logging & Monitoring Failures** - לוגים לא מספיקים
10. **Server-Side Request Forgery (SSRF)** - כפיית השרת לבצע בקשות

---

## שקף 7: SQL Injection - דוגמה

**מה זה?**
תוקף מזריק קוד SQL זדוני דרך קלט משתמש

**קוד פגיע:**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
```

**התקפה:**
```
username = "admin' OR '1'='1"
תוצאה: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```
→ מחזיר את כל המשתמשים! 🚨

**קוד מאובטח:**
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```
→ שאילתות עם פרמטרים מונעות injection ✅

---

## שקף 8: Command Injection - דוגמה

**מה זה?**
תוקף מריץ פקודות מערכת שרירותיות

**קוד פגיע:**
```python
os.system(f"ping {host}")
```

**התקפה:**
```
host = "google.com; rm -rf /"
תוצאה: ping google.com; rm -rf /
```
→ מוחק את כל הקבצים! 🚨

**קוד מאובטח:**
```python
subprocess.run(['ping', '-c', '4', validated_host], shell=False)
```
→ ללא פרשנות shell ✅

---

## שקף 9: Hardcoded Secrets - דוגמה

**מה זה?**
פרטי זיהוי רגישים שמורים בקוד המקור

**קוד פגיע:**
```python
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "password123"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG"
```
→ כל מי שיש לו גישה לקוד רואה את הסודות! 🚨

**קוד מאובטח:**
```python
import os
API_KEY = os.environ.get('API_KEY')
# או להשתמש במנגנון ניהול סודות חיצוני
```
→ ניהול סודות חיצוני ✅

---

## שקף 10: Broken Access Control - דוגמה

**מה זה?**
משתמשים יכולים לגשת למשאבים או לבצע פעולות שאינם מורשים לבצע

**קוד פגיע:**
```python
@app.route('/admin/user/<user_id>')
def get_user_details(user_id):
    # אין בדיקת הרשאות!
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    return jsonify(user)
```

**התקפה:**
```
משתמש עם תפקיד "guest" ניגש ל: /admin/user/1
→ מקבל פרטי משתמש admin! 🚨
```

**קוד מאובטח:**
```python
@app.route('/admin/user/<user_id>')
@require_role('admin')  # Decorator לבדיקת הרשאות
def get_user_details(user_id):
    if not current_user.is_admin:
        abort(403)
    user = db.query("SELECT * FROM users WHERE id = ?", (user_id,))
    return jsonify(user)
```
→ בדיקות הרשאות נאותות ✅

---

## שקף 11: Cryptographic Failures - דוגמה

**מה זה?**
שימוש באלגוריתמים קריפטוגרפיים חלשים או שבורים

**קוד פגיע:**
```python
import hashlib
from Crypto.Cipher import DES

# hashing חלש
password_hash = hashlib.md5(password.encode()).hexdigest()

# הצפנה חלשה
cipher = DES.new(b'8bytekey', DES.MODE_ECB)
encrypted = cipher.encrypt(data)
```
→ MD5 שבור, DES מיושן! 🚨

**קוד מאובטח:**
```python
import bcrypt
from cryptography.fernet import Fernet

# hashing חזק לסיסמאות
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# הצפנה חזקה (AES-256)
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(data.encode())
```
→ אלגוריתמים סטנדרטיים בתעשייה ✅

---

## שקף 12: Insecure Design - דוגמה

**מה זה?**
בקרות אבטחה חסרות או לא יעילות בעיצוב האפליקציה

**עיצוב פגיע:**
```python
# איפוס סיסמה ללא הגבלת קצב
@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.json['email']
    token = generate_token()  # קוד בן 6 ספרות
    send_email(email, token)
    return jsonify({"message": "Reset code sent"})
```
→ תוקף יכול לנסות brute-force על 6 ספרות! 🚨

**עיצוב מאובטח:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/reset-password', methods=['POST'])
@limiter.limit("3 per hour")  # הגבלת קצב
def reset_password():
    email = request.json['email']
    token = secrets.token_urlsafe(32)  # קריפטוגרפית מאובטח
    store_token_with_expiry(email, token, expires_in=15*60)  # 15 דקות
    send_email(email, token)
    return jsonify({"message": "Reset link sent"})
```
→ הגבלת קצב + טוקנים חזקים + תפוגה ✅

---

## שקף 13: Security Misconfiguration - דוגמה

**מה זה?**
הגדרות ברירת מחדל לא מאובטחות, הגדרות חלקיות, או מידע debug חשוף

**הגדרה פגיעה:**
```python
# אפליקציית Flask בייצור
app = Flask(__name__)
app.config['DEBUG'] = True  # 🚨 מצב debug בייצור!
app.config['SECRET_KEY'] = 'dev'  # 🚨 סוד חלש

# Dockerfile
FROM python:3.8
EXPOSE 5000
ENV FLASK_ENV=development  # 🚨
RUN chmod 777 /app  # 🚨 כתיבה לכולם
```

**הגדרה מאובטחת:**
```python
# אפליקציית Flask בייצור
app = Flask(__name__)
app.config['DEBUG'] = False  # ✅
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # ✅

# Dockerfile
FROM python:3.11-slim
EXPOSE 5000
ENV FLASK_ENV=production  # ✅
USER 1001  # ✅ משתמש לא-root
RUN chmod 755 /app  # ✅ הרשאות נכונות
```

---

## שקף 14: Vulnerable Dependencies - דוגמה

**מה זה?**
שימוש בספריות עם פרצות אבטחה ידועות

**דוגמה:**
```json
{
  "dependencies": {
    "lodash": "4.17.15",  // CVE-2019-10744 - Prototype Pollution
    "axios": "0.21.1",    // CVE-2021-3749 - SSRF
    "moment": "2.29.1"    // CVE-2022-31129 - ReDoS
  }
}
```

**השפעה:**
- הרצת קוד מרחוק (RCE)
- גניבת מידע
- Denial of Service

**פתרון:**
- לעדכן dependencies
- להשתמש בכלי סריקת אבטחה
- לנטר מאגרי CVE

---

## שקף 15: Authentication Failures - דוגמה

**מה זה?**
מנגנוני אימות שבורים המאפשרים גישה לא מורשית

**קוד פגיע:**
```python
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    # אין הגבלת קצב, אין נעילת חשבון
    user = db.query(f"SELECT * FROM users WHERE username='{username}'")
    if user and user['password'] == password:  # 🚨 טקסט פשוט!
        session['user_id'] = user['id']
        return jsonify({"success": True})
```
→ אפשר brute-force, סיסמאות בטקסט פשוט! 🚨

**קוד מאובטח:**
```python
from flask_limiter import Limiter
import bcrypt

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # הגבלת קצב
def login():
    username = request.json['username']
    password = request.json['password']

    user = db.query("SELECT * FROM users WHERE username=?", (username,))
    if user and bcrypt.checkpw(password.encode(), user['password_hash']):
        session.permanent = False  # timeout של session
        session['user_id'] = user['id']
        log_login_attempt(username, success=True)
        return jsonify({"success": True})

    log_login_attempt(username, success=False)
    return jsonify({"error": "Invalid credentials"}), 401
```
→ הגבלת קצב + סיסמאות מוצפנות + לוגים ✅

---

## שקף 16: Data Integrity Failures - דוגמה

**מה זה?**
deserialization לא מאובטח המוביל להרצת קוד

**קוד פגיע:**
```python
import pickle
import yaml

# Pickle deserialization - RCE!
@app.route('/load-object', methods=['POST'])
def load_object():
    data = request.data
    obj = pickle.loads(data)  # 🚨 תוקף יכול להריץ קוד!
    return jsonify(obj)

# YAML deserialization
config = yaml.load(user_input)  # 🚨 לא בטוח
```

**התקפה:**
```python
# תוקף יוצר pickle זדוני
import pickle, os
class Exploit:
    def __reduce__(self):
        return (os.system, ('rm -rf /',))
payload = pickle.dumps(Exploit())
```

**קוד מאובטח:**
```python
import json

@app.route('/load-object', methods=['POST'])
def load_object():
    data = request.data
    obj = json.loads(data)  # ✅ סריאליזציה בטוחה
    # אימות schema
    if not validate_schema(obj):
        abort(400)
    return jsonify(obj)

# טעינת YAML בטוחה
config = yaml.safe_load(user_input)  # ✅
```

---

## שקף 17: Logging & Monitoring Failures - דוגמה

**מה זה?**
לוגים לא מספיקים מונעים זיהוי של אירועי אבטחה

**קוד פגיע:**
```python
@app.route('/admin/delete-user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # אין לוגים!
    db.execute(f"DELETE FROM users WHERE id = {user_id}")
    return jsonify({"success": True})

@app.route('/login', methods=['POST'])
def login():
    # ניסיונות כושלים לא נרשמים בלוג
    if not authenticate(username, password):
        return jsonify({"error": "Invalid"}), 401
```
→ אין audit trail, התקפות לא מזוהות! 🚨

**קוד מאובטח:**
```python
import logging

logger = logging.getLogger(__name__)

@app.route('/admin/delete-user/<user_id>', methods=['DELETE'])
@require_role('admin')
def delete_user(user_id):
    logger.warning(f"ניסיון מחיקת משתמש על ידי {current_user.id} למשתמש {user_id}")
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    logger.info(f"משתמש {user_id} נמחק על ידי {current_user.id}")
    return jsonify({"success": True})

@app.route('/login', methods=['POST'])
def login():
    if not authenticate(username, password):
        logger.warning(f"ניסיון כניסה נכשל למשתמש {username} מ-{request.remote_addr}")
        return jsonify({"error": "Invalid"}), 401
    logger.info(f"כניסה מוצלחת למשתמש {username}")
```
→ audit trail מלא ✅

---

## שקף 18: Server-Side Request Forgery (SSRF) - דוגמה

**מה זה?**
תוקף מאלץ את השרת לבצע בקשות למיקומים לא מיועדים

**קוד פגיע:**
```python
import requests

@app.route('/fetch-url', methods=['POST'])
def fetch_url():
    url = request.json['url']
    # אין ולידציה!
    response = requests.get(url)  # 🚨
    return response.text
```

**התקפה:**
```
POST /fetch-url
{"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}
→ גישה ל-metadata של AWS וגניבת credentials! 🚨
```

**קוד מאובטח:**
```python
import requests
from urllib.parse import urlparse

ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']

@app.route('/fetch-url', methods=['POST'])
def fetch_url():
    url = request.json['url']

    # אימות URL
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        abort(400, "פרוטוקול לא תקין")
    if parsed.hostname not in ALLOWED_DOMAINS:
        abort(400, "דומיין לא מורשה")
    if parsed.hostname in ['localhost', '127.0.0.1', '169.254.169.254']:
        abort(400, "IPs פנימיים חסומים")

    response = requests.get(url, timeout=5)
    return response.text
```
→ אימות whitelist + חסימת IPs פנימיים ✅

---

## שקף 19: סקירת כלי אבטחה

### **1. SonarQube**
**Static Application Security Testing (SAST)**

מה זה עושה:
- מנתח קוד מקור בלי להריץ אותו
- מזהה בעיות איכות קוד
- מוצא פרצות אבטחה
- עוקב אחרי חוב טכני

מוצא:
- SQL Injection
- סודות מוטמעים בקוד
- הצפנה חלשה
- Code smells

---

## שקף 20: סקירת כלי אבטחה (המשך)

### **2. Prisma Cloud (Twistlock)**
**אבטחת Container ותשתית**

מה זה עושה:
- סורק Docker images לפרצות
- מנתח Infrastructure as Code (IaC)
- הגנה בזמן ריצה (runtime)
- בדיקות תאימות (compliance)

מוצא:
- Base images פגיעים
- Containers לא מוגדרים נכון
- פורטים חשופים
- שיטות Dockerfile לא מאובטחות

---

## שקף 21: תהליך העבודה DevSecOps

```
┌─────────────────────────────────────────────────┐
│  1. מפתח כותב קוד                               │
│     └─> Commit ל-Git                            │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│  2. Pipeline CI/CD מופעל                        │
│     ├─> בנייה של האפליקציה                     │
│     ├─> הרצת unit tests                         │
│     ├─> סריקת SonarQube (ניתוח קוד)            │
│     └─> סריקת Prisma Cloud (container)          │
└──────────────┬──────────────────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
┌─────▼──────┐   ┌──────▼──────┐
│ עבר ✅     │   │  נכשל ❌    │
│ פריסה      │   │  תיקון      │
└────────────┘   └──────┬──────┘
                        │
                 ┌──────▼───────────────────────┐
                 │ 3. מפתח בודק דוחות          │
                 │    └─> מתקן פרצות            │
                 └──────┬───────────────────────┘
                        │
                 ┌──────▼──────────┐
                 │ 4. Commit תיקון│
                 │    └─> חזרה ל-2 │
                 └─────────────────┘
```

---

## שקף 22: הריפו שלכם לתרגול

**שלוש גרסאות שפות:**
- **Python** - אפליקציית Flask
- **.NET/C#** - אפליקציית ASP.NET Core
- **Node.js** - אפליקציית Express.js

**כל אחת מכילה 10+ סוגי פרצות:**
- SQL Injection
- Command Injection
- סודות מוטמעים בקוד
- הצפנה חלשה
- Path Traversal
- Deserialization לא מאובטח
- פרצות XXE
- Dependencies פגיעים
- חשיפת מידע
- איכות קוד נמוכה

---

## שקף 23: מבנה הריפו

```
DevSecOpsExc/
├── python/           # אפליקציית Python/Flask פגיעה
│   ├── app.py
│   ├── database.py
│   ├── crypto_utils.py
│   ├── openshift/    # הגדרות OpenShift
│   └── .github/      # Pipeline CI/CD
├── dotnet/           # אפליקציית .NET/C# פגיעה
│   ├── Controllers/
│   ├── Services/
│   └── .github/      # Pipeline CI/CD
└── nodejs/           # אפליקציית Node.js פגיעה
    ├── routes/
    ├── server.js
    └── .github/      # Pipeline CI/CD
```

---

## שקף 24: תהליך התרגיל - צעד אחר צעד

**שלב 1: בחרו שפה**
```bash
cd python   # או dotnet או nodejs
```

**שלב 2: הריצו את האפליקציה מקומית**
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

## שקף 25: תהליך התרגיל (המשך)

**שלב 3: הפעילו את ה-CI/CD Pipeline**
```bash
git add .
git commit -m "Initial commit"
git push
```

**תוצאה:** ה-Pipeline **יכשל** 🚨

**שלב 4: בדקו דוחות אבטחה**
- כנסו ל-GitHub Actions
- צפו ב-pipeline שנכשל
- הורידו artifacts:
  - דוח SonarQube
  - דוח Prisma Cloud

---

## שקף 26: תהליך התרגיל (המשך)

**שלב 5: נתחו פרצות**

פתחו דוחות וזהו:
- **מה** הפרצה?
- **איפה** היא בקוד?
- **למה** היא מסוכנת?
- **איך** לתקן?

**שלב 6: תקנו בעיות**
- קראו `SOLUTIONS.md` להדרכה (אבל נסו קודם לבד!)
- עדכנו קוד עם יישומים מאובטחים
- בדקו תיקונים מקומית

---

## שקף 27: תהליך התרגיל (המשך)

**שלב 7: אמתו תיקונים**
```bash
git add .
git commit -m "Fix SQL injection in user.py"
git push
```

**שלב 8: חזרו עד שהכל עובר**
- Pipeline צריך להפוך לירוק ✅
- כל בדיקות האבטחה עוברות
- האפליקציה מאובטחת

---

## שקף 28: דוגמה - תיקון SQL Injection

**1. דוח SonarQube אומר:**
```
פרצת SQL Injection ב-database.py שורה 42
Severity: CRITICAL
```

**2. בדקו את הקוד:**
```python
# שורה 42 - database.py
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
```

**3. זהו את הבעיה:**
- שרשור מחרוזות עם קלט משתמש
- אין ולידציה של קלט
- הרצה ישירה של שאילתה

---

## שקף 29: דוגמה - תיקון SQL Injection (המשך)

**4. החילו את התיקון:**
```python
def get_user(username):
    # השתמשו בשאילתה עם פרמטרים
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
```

**5. אמתו:**
```bash
# הריצו בדיקות
pytest tests/

# Commit ו-push
git add database.py
git commit -m "Fix SQL injection in get_user()"
git push
```

**6. בדקו Pipeline:**
- סריקת SonarQube: עבר ✅
- סריקת Prisma Cloud: עבר ✅

---

## שקף 30: טיפים להצלחה

**1. קראו את הודעות השגיאה**
- כלי האבטחה נותנים הסברים מפורטים
- לעיתים קרובות כוללים המלצות לתיקון

**2. השתמשו ב-SOLUTIONS.md כמוצא אחרון**
- נסו לתקן בעיות לבד תחילה
- למדו על ידי עשייה, לא על ידי העתקה

**3. בדקו מקומית לפני push**
- הריצו את האפליקציה
- בדקו את ה-endpoint הפגיע
- וודאו שהתיקון עובד

**4. תקנו קטגוריה אחת בכל פעם**
- אל תנסו לתקן הכל בבת אחת
- התחילו עם בעיות קריטיות תחילה

---

## שקף 31: טעויות נפוצות להימנע מהן

❌ **אל תעשו:**
- למחוק קוד פגיע בלי להחליף אותו
- לכבות בדיקות אבטחה כדי להעביר pipeline
- להעתיק פתרונות בלי להבין
- להתעלם מבעיות severity בינוני/נמוך

✅ **כן תעשו:**
- להבין למה קוד פגיע
- ליישם תיקונים נכונים
- להוסיף ולידציה של קלט
- לעדכן dependencies
- להשתמש בהצפנה מאובטחת
- לעקוב אחרי עיקרון least privilege

---

## שקף 32: פריסה ל-OpenShift

**מה זה OpenShift?**
- פלטפורמת Kubernetes ארגונית של Red Hat
- תזמור containers
- פיצ'רי אבטחה מובנים

**הריפו שלכם כולל:**
- הגדרות deployment
- הגדרות service
- הגדרות route
- Build configs ל-S2I (Source-to-Image)

**פקודת פריסה:**
```bash
oc login https://openshift.example.com
oc new-project devsecops-practice
oc apply -f openshift/deployment-config.yml
```

---

## שקף 33: ניהול סודות (Secrets Management)

**למה חשוב?**
- סודות לא צריכים להיות בקוד המקור
- צריך ניהול מרכזי ובטוח
- הצפנה בזמן אחסון ובזמן העברה

**שיטות מומלצות:**
- משתני סביבה (Environment Variables)
- OpenShift Secrets
- פתרונות ניהול סודות ארגוניים (Vault, AWS Secrets Manager, Azure Key Vault)
- Kubernetes Secrets עם הצפנה

**יתרונות:**
- אין סודות מוטמעים בקוד
- ניהול סודות מרכזי
- Audit trail לגישה לסודות
- רוטציה קלה של סודות

---

## שקף 34: Best Practices אבטחה

**ולידציה של קלט**
- לאמת כל קלט משתמש
- להשתמש ב-whitelists, לא blacklists
- לסנן מידע לפני שימוש

**Authentication & Authorization**
- מדיניות סיסמאות חזקה
- אימות דו-שלבי
- עיקרון least privilege

**הצפנה**
- להשתמש באלגוריתמים סטנדרטיים
- לעולם לא לפתח קריפטו משלכם
- ניהול מפתחות נכון

**Dependencies**
- לעדכן ספריות
- לנטר מאגרי CVE
- להשתמש בכלי סריקת dependencies

---

## שקף 35: אבטחה בייצור

**Defense in Depth**
שכבות מרובות של אבטחה:

1. **רמת האפליקציה**
   - ולידציה של קלט
   - שיטות קידוד מאובטח

2. **רמת התשתית**
   - אבטחת container
   - מדיניות רשת

3. **רמת הפלטפורמה**
   - פיצ'רי אבטחה של OpenShift
   - Service mesh

4. **רמת הניטור**
   - לוגים ואודיט
   - זיהוי חדירות

---

## שקף 36: מדידת הצלחה

**מדדי מפתח:**

1. **זמן זיהוי פרצה**
   - יעד: < שעה אחרי commit

2. **זמן תיקון פרצה**
   - יעד: בעיות קריטיות < 24 שעות
   - יעד: בעיות High < 7 ימים

3. **שיעור False Positives**
   - יעד: < 10%

4. **שיעור הצלחת Pipeline**
   - יעד: > 80% בניסיון ראשון (אחרי הדרכה)

5. **חוב אבטחה**
   - יעד: אפס בעיות קריטיות/high בייצור

---

## שקף 37: משאבי למידה

**תיעוד:**
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
- SonarQube Docs: https://docs.sonarqube.org/
- Prisma Cloud Docs: https://docs.paloaltonetworks.com/prisma

**תרגול:**
- OWASP WebGoat: https://owasp.org/www-project-webgoat/
- HackTheBox: https://www.hackthebox.com/
- TryHackMe: https://tryhackme.com/

**קהילות:**
- קהילת OWASP
- DevSecOps Reddit
- Security Stack Exchange

---

## שקף 38: מטרות התרגיל

בסוף התרגיל תדעו:

✅ להבין פרצות אבטחה נפוצות
✅ להשתמש בכלי סריקת אבטחה
✅ לקרוא ולפרש דוחות אבטחה
✅ לתקן פרצות עם שיטות קידוד מאובטח
✅ ליישם DevSecOps ב-CI/CD pipelines
✅ לפרוס אפליקציות מאובטחות ל-OpenShift
✅ להשתמש בניהול סודות בטוח

**זכרו:** אבטחה היא אחריות של כולם! 🔒

---

## שקף 39: קבלת עזרה

**במהלך התרגיל:**

1. **בדקו SOLUTIONS.md** - תיקונים מפורטים לכל פרצה
2. **בדקו תיעוד הכלים** - מסמכי SonarQube ו-Prisma Cloud
3. **שאלו שאלות** - המדריכים כאן כדי לעזור
4. **שתפו פעולה** - דונו עם חברי הצוות
5. **חפשו באינטרנט** - OWASP, Stack Overflow

**בעיות בריפו:**
- GitHub Issues: דווחו על באגים או שאלו שאלות
- תיעוד: כל הקבצי README בכל תיקיית שפה

---

## שקף 40: בואו נתחיל!

**רשימת בדיקה לפני התרגיל:**

□ חשבון GitHub נוצר
□ Git מותקן מקומית
□ סביבת פיתוח מוכנה:
  - Python 3.9+ או
  - .NET 8.0 SDK או
  - Node.js 18.x
□ גישה למופע SonarQube
□ גישה לקונסול Prisma Cloud
□ OpenShift CLI מותקן (אופציונלי)
□ Repository עשה fork/clone

**מוכנים? בואו נבנה אפליקציות מאובטחות! 🚀**

---

## שקף 41: שאלות ותשובות

**שאלות?**

---

