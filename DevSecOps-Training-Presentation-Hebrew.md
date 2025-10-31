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
# או להשתמש ב-HashiCorp Vault
from vault_integration import VaultClient
vault = VaultClient()
API_KEY = vault.get_secret('app/api_key')
```
→ ניהול סודות חיצוני ✅

---

## שקף 10: Vulnerable Dependencies - דוגמה

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

## שקף 11: סקירת כלי אבטחה

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

## שקף 12: סקירת כלי אבטחה (המשך)

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

## שקף 13: תהליך העבודה DevSecOps

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

## שקף 14: הריפו שלכם לתרגול

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

## שקף 15: מבנה הריפו

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

## שקף 16: תהליך התרגיל - צעד אחר צעד

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

## שקף 17: תהליך התרגיל (המשך)

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

## שקף 18: תהליך התרגיל (המשך)

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

## שקף 19: תהליך התרגיל (המשך)

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

## שקף 20: דוגמה - תיקון SQL Injection

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

## שקף 21: דוגמה - תיקון SQL Injection (המשך)

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

## שקף 22: טיפים להצלחה

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

## שקף 23: טעויות נפוצות להימנע מהן

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

## שקף 24: פריסה ל-OpenShift

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

## שקף 25: אינטגרציה עם HashiCorp Vault

**מה זה Vault?**
- פלטפורמה לניהול סודות
- יצירת סודות דינמיים
- הצפנה כשירות

**הריפו שלכם כולל:**
- אינטגרציה של Vault client
- אימות Kubernetes
- Credentials דינמיים למסד נתונים
- דוגמאות לרוטציה של סודות

**יתרונות:**
- אין סודות מוטמעים בקוד
- ניהול סודות מרכזי
- Audit trail לגישה לסודות
- רוטציה אוטומטית של סודות

---

## שקף 26: Best Practices אבטחה

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

## שקף 27: אבטחה בייצור

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

## שקף 28: מדידת הצלחה

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

## שקף 29: משאבי למידה

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

## שקף 30: מטרות התרגיל

בסוף התרגיל תדעו:

✅ להבין פרצות אבטחה נפוצות
✅ להשתמש בכלי סריקת אבטחה
✅ לקרוא ולפרש דוחות אבטחה
✅ לתקן פרצות עם שיטות קידוד מאובטח
✅ ליישם DevSecOps ב-CI/CD pipelines
✅ לפרוס אפליקציות מאובטחות ל-OpenShift
✅ להשתמש ב-Vault לניהול סודות

**זכרו:** אבטחה היא אחריות של כולם! 🔒

---

## שקף 31: קבלת עזרה

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

## שקף 32: בואו נתחיל!

**רשימת בדיקה לפני התרגיל:**

□ חשבון GitHub נוצר
□ Git מותקן מקומית
□ סביבת פיתוח מוכנה:
  - Python 3.9+ או
  - .NET 6.0 SDK או
  - Node.js 14.x
□ גישה למופע SonarQube
□ גישה לקונסול Prisma Cloud
□ OpenShift CLI מותקן (אופציונלי)
□ Repository עשה fork/clone

**מוכנים? בואו נבנה אפליקציות מאובטחות! 🚀**

---

## שקף 33: שאלות ותשובות

**שאלות?**

---

