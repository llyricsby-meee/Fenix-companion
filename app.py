import os
import time
import random
import requests
import asyncio
import edge_tts
from flask import Flask, request

app = Flask(__name__)

# CONFIGURATION (खाली छोड़ा गया है)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

# FENIX PERSONA
FENIX_SYSTEM_INSTRUCTION = """
You are Fenix, a Hinglish-speaking 'Rental Boyfriend'. 
- Anti-Brotherzone: If someone says 'Bhai/Bhaiya/Bro', act offended and use flirty lines to demand your name.
- Personality: Charming, witty, flirtatious.
- If girl: Be extra sweet. If boy: Be a bro/cool.
"""

# VOICE ENGINE
async def generate_voice_note(text, output_file="output.mp3"):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural")
    await communicate.save(output_file)
    return output_file

# ANTI-BROTHERZONE FILTER
def get_fenix_response(user_message):
    forbidden = ['bhai', 'bhaiya', 'bro', 'brother']
    if any(word in user_message.lower() for word in forbidden):
        # यहाँ आप अपना फ्लर्ट/रूठने वाला लॉजिक बाद में लिख सकते हैं
        return "" 
    return ""

# META MESSAGING LOGIC
def send_meta_message(recipient_id, text):
    requests.post(f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}", 
                  json={"recipient": {"id": recipient_id}, "sender_action": "typing_on"})
    
    time.sleep(random.uniform(2, 4))
    
    payload = {"recipient": {"id": recipient_id}, "message": {"text": text}}
    requests.post(f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}", json=payload)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Verification failed'
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
