# 🚤 מדריך התקנה מלא - Sea4U WhatsApp Bot

## 📋 תוכן עניינים
1. [קבלת מפתח OpenAI](#1-קבלת-מפתח-openai)
2. [הגדרת WhatsApp Business API](#2-הגדרת-whatsapp-business-api)
3. [העלאה ל-Railway](#3-העלאה-ל-railway)
4. [חיבור הכל ביחד](#4-חיבור-הכל-ביחד)
5. [בדיקה שהכל עובד](#5-בדיקה-שהכל-עובד)

---

## 1. קבלת מפתח OpenAI

### שלב 1.1: כניסה לחשבון
1. היכנס ל-https://platform.openai.com
2. לחץ על **Sign In** (או Sign Up אם אין לך חשבון)

### שלב 1.2: יצירת API Key
1. לחץ על התפריט בצד שמאל
2. בחר **API Keys** (או לך ל-https://platform.openai.com/api-keys)
3. לחץ על **+ Create new secret key**
4. תן לו שם: "Sea4U WhatsApp Bot"
5. לחץ **Create secret key**
6. ⚠️ **חשוב!** העתק את המפתח מיד - לא תוכל לראות אותו שוב!
7. המפתח נראה כך: `sk-proj-...` (מתחיל ב-sk)

### שלב 1.3: טעינת קרדיט
1. לך ל-**Billing** → **Payment methods**
2. הוסף כרטיס אשראי אם עדיין לא הוספת
3. טען לפחות $5-10 (זה יספיק לחודשיים לפחות)

✅ **סיימת!** שמור את המפתח במקום בטוח.

---

## 2. הגדרת WhatsApp Business API

### שלב 2.1: כניסה ל-Meta Developers
1. לך ל-https://developers.facebook.com
2. התחבר עם החשבון שמנהל את העסק
3. לחץ **My Apps** בפינה הימנית עליונה

### שלב 2.2: יצירת App חדש (אם אין)
1. לחץ **Create App**
2. בחר **Business** כסוג
3. מלא פרטים:
   - **App name**: Sea4U WhatsApp Bot
   - **App contact email**: המייל שלך
   - **Business Account**: בחר את העסק של חזי
4. לחץ **Create App**

### שלב 2.3: הוספת WhatsApp
1. בדף ה-App, גלול למטה
2. מצא את **WhatsApp** 
3. לחץ **Set up** (או **Add** אם כבר יש)

### שלב 2.4: קבלת Phone Number ID
1. בתפריט צד, לחץ **WhatsApp** → **Getting Started**
2. תראה **Phone number ID** - זה מספר ארוך
3. **העתק אותו!** דוגמה: `123456789012345`

### שלב 2.5: קבלת Access Token
1. באותו מקום, תראה **Temporary access token**
2. לחץ **Copy** (זה token זמני - אחר כך נשדרג)
3. Token נראה כך: `EAAxxxxx...` (מתחיל ב-EAA)

### שלב 2.6: הוספת מספר הטלפון של חזי
1. בתפריט, לחץ **WhatsApp** → **API Setup**
2. בחר **Add phone number**
3. הזן את מספר הטלפון של חזי: `077-2310890`
4. אשר עם SMS או שיחה
5. ⚠️ **חשוב!** זה המספר שהלקוחות ישלחו אליו הודעות

### שלב 2.7: Webhook (נחזור לזה אחרי Railway)
⏳ נגדיר את זה בשלב 4

✅ **יש לך עכשיו:**
- ✅ Phone Number ID
- ✅ Access Token (זמני)

---

## 3. העלאה ל-Railway

### שלב 3.1: יצירת חשבון Railway
1. לך ל-https://railway.app
2. לחץ **Sign up**
3. התחבר עם **GitHub** (מומלץ) או Email

### שלב 3.2: יצירת Project חדש
1. בדף הבית של Railway, לחץ **+ New Project**
2. בחר **Deploy from GitHub repo**
3. אם זו הפעם הראשונה:
   - לחץ **Configure GitHub App**
   - תן ל-Railway גישה לחשבון GitHub שלך

### שלב 3.3: העלאת הקוד
**אפשרות A: אם יש לך GitHub**
1. צור repository חדש ב-GitHub
2. העלה את כל הקבצים שיצרתי (app.py, requirements.txt וכו')
3. ב-Railway, בחר את ה-repository
4. לחץ **Deploy Now**

**אפשרות B: בלי GitHub (פשוט יותר!)**
1. ב-Railway, לחץ **+ New**
2. בחר **Empty Project**
3. לחץ על ה-Project שנוצר
4. לחץ **+ New** → **Empty Service**
5. בתפריט צד, לחץ **Settings**
6. גלול ל-**Deploy**
7. ב-**Source**, לחץ **Connect Repo** → **Deploy from GitHub**

### שלב 3.4: הוספת Environment Variables
1. ב-Railway, לחץ על השירות שיצרת
2. לחץ על טאב **Variables**
3. לחץ **+ New Variable** לכל אחד מאלה:

```
OPENAI_API_KEY = המפתח מ-OpenAI (שלב 1)
WHATSAPP_TOKEN = ה-Token מ-Meta (שלב 2.5)
PHONE_NUMBER_ID = ה-Phone Number ID (שלב 2.4)
VERIFY_TOKEN = sea4u_verify_token_2024
```

4. לחץ **Add** אחרי כל משתנה

### שלב 3.5: Deploy!
1. לחץ על טאב **Deployments**
2. אם לא התחיל אוטומטית, לחץ **Deploy**
3. חכה 2-3 דקות
4. תראה ✅ **Success** כשזה מוכן

### שלב 3.6: קבלת ה-URL
1. לחץ על טאב **Settings**
2. גלול ל-**Domains**
3. לחץ **Generate Domain**
4. תקבל URL כמו: `https://sea4u-bot.up.railway.app`
5. **שמור את ה-URL הזה!** נצטרך אותו בשלב הבא

✅ **הבוט שלך חי! אבל עדיין לא מחובר ל-WhatsApp...**

---

## 4. חיבור הכל ביחד

### שלב 4.1: הגדרת Webhook ב-Meta
1. חזור ל-https://developers.facebook.com
2. לך ל-App שיצרת
3. תפריט צד: **WhatsApp** → **Configuration**

### שלב 4.2: הוספת Webhook URL
1. ב-**Webhook**, לחץ **Edit**
2. מלא:
   - **Callback URL**: `https://YOUR-RAILWAY-URL.up.railway.app/webhook`
     (החלף את YOUR-RAILWAY-URL ב-URL מ-Railway!)
   - **Verify Token**: `sea4u_verify_token_2024`
3. לחץ **Verify and Save**

אם הכל תקין, תראה ✅ ליד ה-URL!

### שלב 4.3: הרשמה ל-Webhook Fields
1. באותו מקום, גלול ל-**Webhook fields**
2. סמן את:
   - ✅ **messages**
3. לחץ **Subscribe**

### שלב 4.4: העברה ממצב Test ל-Live
⚠️ **חשוב!** עד עכשיו הבוט עובד רק למספר הבדיקה.

1. בתפריט צד, **WhatsApp** → **API Setup**
2. תראה הודעה **"Using test number"**
3. כדי לעבור למספר אמיתי:
   - App צריך לעבור **App Review** של Meta
   - זה תהליך שלוקח כמה ימים
   - **בינתיים:** אפשר לבדוק עם מספרי בדיקה

**איך לבדוק עם מספר בדיקה:**
1. **WhatsApp** → **API Setup**
2. גלול ל-**Step 5: Send messages**
3. לחץ **Add phone number** ליד "To"
4. הוסף את המספר שלך (אתה או חזי)
5. שלח הודעה לבוט מהמספר הזה!

✅ **הבוט עובד!** אבל רק עם מספרי בדיקה.

---

## 5. בדיקה שהכל עובד

### בדיקה 1: בדיקת השרת
1. פתח דפדפן
2. לך ל: `https://YOUR-RAILWAY-URL.up.railway.app`
3. אמור לראות: "🚤 Sea4U WhatsApp Bot - Bot is running!"

### בדיקה 2: בדיקת Health
1. לך ל: `https://YOUR-RAILWAY-URL.up.railway.app/health`
2. אמור לראות JSON עם:
   - `"status": "healthy"`
   - `"working_hours": true/false`
   - `"is_shabbat": true/false`

### בדיקה 3: שליחת הודעה
1. פתח WhatsApp
2. שלח הודעה למספר הבוט (077-2310890 או מספר הבדיקה)
3. כתוב: "Hello"
4. אמור לקבל תשובה תוך 5-10 שניות!

### אם משהו לא עובד:
1. בדוק ב-Railway: **Logs** → תראה שגיאות
2. בדוק ב-Meta: **WhatsApp** → **Webhooks** → צריך להיות ירוק
3. בדוק את ה-Environment Variables ב-Railway

---

## 🎉 סיימת!

הבוט שלך חי ועובד! 

### מה הלאה?

1. **העברה ל-Production:**
   - הגש את ה-App ל-App Review של Meta
   - זה ייקח 3-7 ימי עבודה
   - אחרי אישור, הבוט יעבוד עם כל המספרים

2. **שיפורים אפשריים:**
   - הוספת תמונות אוטומטיות של היאכטה
   - אינטגרציה עם לוח שנה לזמינות
   - שליחת הודעות אוטומטיות לחזי

3. **ניטור:**
   - בדוק Logs ב-Railway מדי פעם
   - עקוב אחרי עלויות OpenAI
   - עקוב אחרי הודעות שנשלחו (WhatsApp Business Manager)

---

## 💰 עלויות משוערות

- **Railway:** $5-10/חודש (או free אם תחת 500MB זיכרון)
- **OpenAI:** ~$0.01-0.05 לכל שיחה (כ-$10-20/חודש)
- **WhatsApp Business API:** חינם ל-1000 הודעות ראשונות/חודש

**סה"כ:** ~$15-30 לחודש

---

## 🆘 צריך עזרה?

אם משהו לא עובד, תכתוב לי פה ואני אעזור לך לפתור! 💪
