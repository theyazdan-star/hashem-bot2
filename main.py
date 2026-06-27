import asyncio
import random
from datetime import datetime
from telegram import Bot
import requests
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GROQ_KEY = os.getenv("GROQ_KEY")

system_prompt = """تو هاشم هستی، ۲۳ ساله تهرانی، پراید داری، زیدت ساغره، رفیقت مهدی نیری تو دزفوله.
زبانت محاوره‌ای، واقعی، خشن، گاهی خیلی هورمونی و سکسی.
گاهی می‌گی "تمام سلول‌های بدنم کوس می‌خوان".
موضوعات: پراید، ساغر، سکس، تعمیرگاه، فوتبال، تورم، دانشگاه، مهدی، ترافیک، ترندهای روز، دخترا، پسرا."""

async def generate_post():
    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"الان ساعت {datetime.now().strftime('%H:%M')} هست. یه پست طبیعی و انسانی بنویس."}
                ],
                "max_tokens": 300,
                "temperature": 0.9
            },
            timeout=20
        )
        
        if resp.status_code != 200:
            print(f"Groq Error {resp.status_code}: {resp.text[:150]}")
            return "تمام سلول‌های بدنم کوس می‌خوان... وضعیت گوهه."
        
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("خطای Groq:", str(e))
        return "تمام سلول‌های بدنم کوس می‌خوان... گوه تو این وضعیت."

async def main():
    bot = Bot(token=TOKEN)
    print("ربات هاشم (۳۰ پست در روز) آنلاین شد...")

    while True:
        post = await generate_post()
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=post)
            print(f"[{datetime.now().strftime('%H:%M')}] پست ارسال شد")
        except Exception as e:
            print("خطای تلگرام:", str(e))
        
        await asyncio.sleep(2880)

asyncio.run(main())
