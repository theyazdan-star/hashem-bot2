import asyncio
import random
from datetime import datetime
from telegram import Bot
import requests
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CLAUDE_KEY = os.getenv("CLAUDE_KEY")

system_prompt = """تو هاشم هستی، ۲۳ ساله تهرانی، پراید داری، زیدت ساغره، رفیقت مهدی نیری تو دزفوله.
زبانت محاوره‌ای، واقعی، خشن، گاهی خیلی هورمونی و سکسی.
گاهی می‌گی "تمام سلول‌های بدنم کوس می‌خوان".
موضوعات: پراید، ساغر، سکس، تعمیرگاه، فوتبال، تورم، دانشگاه، مهدی، ترافیک، ترندهای روز، دخترا، پسرا.
۳۰ پست در روز، تنوع بالا، کوتاه تا متوسط."""

async def generate_post():
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": CLAUDE_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={
                "model": "claude-3-5-sonnet-20240620",
                "max_tokens": 250,
                "system": system_prompt,
                "messages": [{"role": "user", "content": f"الان ساعت {datetime.now().strftime('%H:%M')} هست. یه پست طبیعی و انسانی بنویس."}]
            }
        )
        return resp.json()["content"][0]["text"].strip()
    except:
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
            print("خطا:", e)
        
        # هر ۴۸ دقیقه (۳۰ پست در روز)
        await asyncio.sleep(2880)

asyncio.run(main())
