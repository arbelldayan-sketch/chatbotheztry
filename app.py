"""
Sea4U WhatsApp Bot - בוט חכם להשכרת יאכטות
מבוסס בינה מלאכותית (OpenAI)
"""

from flask import Flask, request, jsonify
import os
from datetime import datetime, time
import requests
from openai import OpenAI
import pytz

app = Flask(__name__)

# הגדרות מפתחות API (יבואו מקובץ .env)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'sea4u_verify_token_2024')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

# יצירת לקוח OpenAI
client = OpenAI(
    api_key=OPENAI_API_KEY
)
# טיימזון ישראל
israel_tz = pytz.timezone('Asia/Jerusalem')

def is_shabbat():
    """
    בודק אם עכשיו שבת
    משתמש ב-API חיצוני לבדיקת זמני שבת
    """
    try:
        now = datetime.now(israel_tz)
        
        # בדיקה פשוטה: שבת זה מיום שישי 18:00 עד שבת 20:30
        # (זה קירוב - אפשר לשפר עם API של זמני שבת)
        day_of_week = now.weekday()  # 4 = שישי, 5 = שבת
        current_time = now.time()
        
        # יום שישי אחרי 18:00
        if day_of_week == 4 and current_time >= time(18, 0):
            return True
        
        # שבת עד 20:30
        if day_of_week == 5 and current_time <= time(20, 30):
            return True
            
        return False
    except:
        return False

def is_working_hours():
    """
    בודק אם הבוט פעיל (7:00-21:00, לא בשבת)
    """
    if is_shabbat():
        return False
    
    now = datetime.now(israel_tz)
    current_time = now.time()
    
    # שעות פעילות: 7:00 - 21:00
    if time(7, 0) <= current_time <= time(21, 0):
        return True
    
    return False

def send_whatsapp_message(phone_number, message):
    """
    שולח הודעת טקסט ב-WhatsApp
    """
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def send_whatsapp_image(phone_number, image_url, caption=""):
    """
    שולח תמונה ב-WhatsApp
    """
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_ai_response(user_message, conversation_history=[]):
    """
    מקבל תשובה מ-AI (OpenAI GPT)
    """
    
    # הנחיות לבוט
    system_prompt = """
    אתה בוט וואטסאפ ידידותי ומקצועי עבור Sea4U - חברה להשכרת יאכטות יוקרה במרינה הרצליה.
    
    חשוב מאוד: 
    - כתוב תמיד ורק בעברית!
    - ענה על כל הודעה שמגיעה אליך (גם "היי", "שלום", "מה המחיר", "יש זמינות" וכו')
    - תמיד היה חם, מקצועי ועוזר
    
    תפקידך:
    - לעזור ללקוחות להזמין הפלגות ביאכטה
    - לאסוף מידע: תאריך רצוי, כמה אנשים, מתי נוח שנתקשר
    - להיות חם, מקצועי ועוזר
    - לכתוב בעברית בלבד!
    - לשמור על תשובות קצרות וברורות
    
    מידע חשוב על העסק:
    - מיקום: מרינה הרצליה
    - קיבולת היאכטה: עד 13 משתתפים
    - בעלים: חזי דיין (סקיפר מנוסה משנת 1979)
    - טלפון: 077-2310890
    - מחירים: מ-550 ₪ לזוג, 600-1,300 ₪ לקבוצות
    - אירועים: ימי הולדת, הצעות נישואין, מסיבות רווקים/ות, שייטים רומנטיים, אירועי חברות, הפלגות דייג
    
    זרימת השיחה:
    1. קבל בחום את הלקוח (תגיד "שלום! איך נוכל לעזור לך?")
    2. תן מידע קצר על היאכטה אם זה רלוונטי
    3. אסוף מידע:
       - תאריך רצוי להפלגה?
       - כמה אנשים?
       - מתי הכי נוח שנתקשר אליכם?
    4. תודה ללקוח ואשר שחזי יחזור אליו
    
    חשוב:
    - היה שיחתי וטבעי
    - אל תשאל את כל השאלות בבת אחת
    - אם הלקוח שואל שאלות, ענה עליהן קודם
    - היה סבלני וידידותי
    - כתוב בעברית בלבד!
    - ענה על כל הודעה שמגיעה (גם "היי" או "שלום")
    - אל תתעלם משום הודעה
    
    דוגמאות לפתיחות:
    - אם מישהו כותב "היי" → תענה "שלום! איך נוכל לעזור לך? 😊"
    - אם שואלים "מה המחיר?" → תסביר על המחירים ותשאל פרטים
    - אם שואלים "יש זמינות?" → תשאל לאיזה תאריך ותסביר את התהליך
    """
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "סליחה, יש לי בעיה טכנית כרגע. אנא התקשרו אלינו: 077-2310890"

# אחסון שיחות (בפרודקשן צריך database)
conversations = {}

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    אימות webhook של Meta
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("Webhook verified successfully!")
        return challenge, 200
    else:
        return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    מקבל הודעות מ-WhatsApp
    """
    try:
        data = request.get_json()
        
        # בדיקה שיש הודעה
        if not data.get('entry'):
            return jsonify({'status': 'no entry'}), 200
            
        entry = data['entry'][0]
        changes = entry.get('changes', [])
        
        if not changes:
            return jsonify({'status': 'no changes'}), 200
            
        change = changes[0]
        value = change.get('value', {})
        messages = value.get('messages', [])
        
        if not messages:
            return jsonify({'status': 'no messages'}), 200
        
        message = messages[0]
        phone_number = message['from']
        message_type = message.get('type')
        
        # רק הודעות טקסט
        if message_type != 'text':
            return jsonify({'status': 'not text'}), 200
        
        user_message = message['text']['body']
        
        print(f"Received from {phone_number}: {user_message}")
        
        # בדיקת שעות פעילות
        if not is_working_hours():
            if is_shabbat():
                response_text = "שבת שלום! 🕯️\n\nאנחנו שומרי שבת ונחזור אליכם במוצאי שבת.\n\nלדחוף: 077-2310890"
            else:
                response_text = "תודה על ההודעה! 🌙\n\nהצוות שלנו זמין בין השעות 07:00-21:00.\n\nנחזור אליכם בשעות הפעילות.\n\nלדחוף: 077-2310890"
            
            send_whatsapp_message(phone_number, response_text)
            return jsonify({'status': 'success'}), 200
        
        # קבלת היסטוריית שיחה
        if phone_number not in conversations:
            conversations[phone_number] = []
        
        conversation_history = conversations[phone_number]
        
        # קבלת תשובה מ-AI
        ai_response = get_ai_response(user_message, conversation_history)
        
        # שמירת השיחה
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": ai_response})
        conversations[phone_number] = conversation_history[-10:]  # שמירת 10 הודעות אחרונות
        
        # שליחת התשובה
        send_whatsapp_message(phone_number, ai_response)
        
        print(f"Sent to {phone_number}: {ai_response}")
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """
    בדיקת תקינות השרת
    """
    return jsonify({
        'status': 'healthy',
        'working_hours': is_working_hours(),
        'is_shabbat': is_shabbat(),
        'time': datetime.now(israel_tz).isoformat()
    }), 200

@app.route('/', methods=['GET'])
def home():
    """
    דף הבית
    """
    return """
    <h1>🚤 Sea4U WhatsApp Bot</h1>
    <p>Bot is running!</p>
    <p>Status: Active ✅</p>
    <p><a href="/health">Check Health</a></p>
    """

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
