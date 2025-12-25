# ⚡ מדריך התחלה מהירה - 5 דקות

## צעדים פשוטים:

### 1️⃣ OpenAI (2 דקות)
1. לך ל-https://platform.openai.com/api-keys
2. לחץ **+ Create new secret key**
3. שם: "Sea4U Bot"
4. העתק את המפתח (מתחיל ב-`sk-proj-`)

### 2️⃣ Meta WhatsApp (5 דקות)
1. לך ל-https://developers.facebook.com
2. צור App → בחר **Business**
3. הוסף **WhatsApp** product
4. העתק:
   - **Phone Number ID** (מספר ארוך)
   - **Access Token** (מתחיל ב-`EAA`)
5. הוסף את מספר הטלפון של חזי: 077-2310890

### 3️⃣ Railway (3 דקות)
1. לך ל-https://railway.app
2. התחבר עם GitHub
3. **+ New Project** → **Deploy from GitHub**
4. העלה את כל הקבצים
5. הוסף **Variables:**
   ```
   OPENAI_API_KEY = המפתח מצעד 1
   WHATSAPP_TOKEN = ה-token מצעד 2
   PHONE_NUMBER_ID = ה-ID מצעד 2
   VERIFY_TOKEN = sea4u_verify_token_2024
   ```
6. לחץ **Deploy**
7. העתק את ה-**Domain URL**

### 4️⃣ חיבור Webhook (2 דקות)
1. חזור ל-Meta Developers
2. **WhatsApp** → **Configuration**
3. **Webhook** → **Edit:**
   - Callback URL: `https://YOUR-DOMAIN.up.railway.app/webhook`
   - Verify Token: `sea4u_verify_token_2024`
4. **Verify and Save**
5. סמן ✅ **messages** ב-Webhook fields

### 5️⃣ בדיקה!
1. שלח הודעה למספר הבוט
2. כתוב: "Hello"
3. אמור לקבל תשובה! 🎉

---

**יש בעיה? קרא את [SETUP_GUIDE.md](SETUP_GUIDE.md) למדריך המלא!**
