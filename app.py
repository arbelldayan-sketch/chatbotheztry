import os
from flask import Flask, request
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

# Environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
WHATSAPP_TOKEN = os.environ.get('WHATSAPP_TOKEN')
PHONE_NUMBER_ID = os.environ.get('PHONE_NUMBER_ID')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'sea4u_verify_token_2024')

# DON'T initialize OpenAI at startup - do it inside function!
openai_client = None

def get_openai_client():
    """Lazy load OpenAI client"""
    global openai_client
    if openai_client is None:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    return openai_client

# Store conversation history
conversations = {}

def is_shabbat():
    """Check if it's Shabbat"""
    israel_tz = pytz.timezone('Asia/Jerusalem')
    now = datetime.now(israel_tz)
    
    if now.weekday() == 4 and now.hour >= 18:
        return True
    
    if now.weekday() == 5 and (now.hour < 20 or (now.hour == 20 and now.minute < 30)):
        return True
    
    return False

def is_working_hours():
    """Check working hours 7-21"""
    israel_tz = pytz.timezone('Asia/Jerusalem')
    now = datetime.now(israel_tz)
    return 7 <= now.hour < 21

def send_whatsapp_message(to_number, message):
    """Send WhatsApp message"""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_ai_response(user_message, user_number):
    """Get AI response"""
    
    # Get OpenAI client
    client = get_openai_client()
    
    if user_number not in conversations:
        conversations[user_number] = []
    
    conversations[user_number].append({
        "role": "user",
        "content": user_message
    })
    
    if len(conversations[user_number]) > 10:
        conversations[user_number] = conversations[user_number][-10:]
    
    system_prompt = """אתה עוזר AI ידידותי של Sea4U - שירות השכרת יאכטות בהרצליה.

חשוב: ענה רק בעברית! תמיד בעברית!

פרטי העסק:
- שם: Sea4U
- מיקום: מרינה הרצליה
- טלפון: 077-2310890
- קיבולת: עד 13 אנשים
- מחירים: 550-1,300 ש"ח
- אירועים: ימי הולדת, הצעות נישואין, מסיבות רווקים, שייט רומנטי, אירועי חברה, דיג

המטרה שלך:
1. לענות בעברית בלבד
2. לאסוף: תאריך, מספר אנשים, שעה נוחה לשיחה
3. להפנות לטלפון

סגנון: קצר וידידותי (2-3 משפטים), תמיד ענה!

זכור: תמיד ענה בעברית!"""
    
    messages = [
        {"role": "system", "content": system_prompt}
    ] + conversations[user_number]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        ai_message = response.choices[0].message.content
        
        conversations[user_number].append({
            "role": "assistant",
            "content": ai_message
        })
        
        return ai_message
        
    except Exception as e:
        print(f"OpenAI Error: {str(e)}")
        return "מצטער, יש בעיה טכנית. תחייג ל-077-2310890 בבקשה 🙏"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Forbidden', 403
    
    elif request.method == 'POST':
        data = request.get_json()
        
        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            
            if 'messages' in value:
                message = value['messages'][0]
                from_number = message['from']
                message_body = message['text']['body']
                
                print(f"Received: {message_body} from {from_number}")
                
                if is_shabbat():
                    response_text = "שבת שלום! 🕯️ אנחנו לא זמינים בשבת. נחזור במוצאי שבת!"
                    send_whatsapp_message(from_number, response_text)
                    return 'OK', 200
                
                if not is_working_hours():
                    response_text = "תודה! 🌙 אנחנו זמינים 7:00-21:00. נחזור אליך מחר!"
                    send_whatsapp_message(from_number, response_text)
                    return 'OK', 200
                
                ai_response = get_ai_response(message_body, from_number)
                send_whatsapp_message(from_number, ai_response)
        
        except Exception as e:
            print(f"Error: {str(e)}")
        
        return 'OK', 200

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'healthy', 'service': 'Sea4U WhatsApp Bot'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
