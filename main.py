import asyncio
from datetime import datetime
import requests
import os
import random
import re
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GROQ_KEY = os.getenv("GROQ_KEY")

system_prompt = """تو هاشم هستی، ۲۳ ساله تهرانی، پراید ۲۰۶ سفید داری، زیدت همیشه ساغره، رفیقت مهدی نیری تو دزفوله.
زبانت فقط فارسی محاوره‌ای تهرانی واقعی، خشن، هورمونی، بی‌ادب و گاهی خیلی سکسی.

مثال‌های واقعی از سبک تو:
- "لیترالی دخترایی که کون گنده دارن بدجوری ترن آفم میکنن، ولی همینا باعث میشن مردای ایرونی به زناشون خیانت کنن👎"
- "تمام سلول‌های بدنم کوس می‌خوان وقتی یه کون گنده تو شلوار لگ می‌بینم اوف"
"""

def get_tweet_examples():
    examples = ["فاکینگ یک ساعت و نیمه که رو یه نقطه توی ترافیک گیر کردم 🤬", "پرایدم واسه تعمیر رفته، حالم گرفته داداش", "تمام سلول‌های بدنم کوس می‌خوان... وضعیت گوهه"]
    return random.sample(examples, 2)

async def generate_post():
    try:
        examples = get_tweet_examples()
        examples_text = "\n".join([f"- {ex}" for ex in examples])
        
        user_content = f"""الان ساعت {datetime.now().strftime('%H:%M')} هست.

چند تا پست واقعی:
{examples_text}

حالا تو به عنوان هاشم یه پست جدید بنویس."""

        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                "max_tokens": 300,
                "temperature": 0.9
            },
            timeout=20
        )
        
        if resp.status_code != 200:
            return "تمام سلول‌های بدنم کوس می‌خوان... گوه تو این وضعیت."

        text = resp.json()["choices"][0]["message"]["content"].strip()
        text = re.sub(r'[^\u0600-\u06FF\s\.,!?؟،؛😂🔥💦😈]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    except:
        return "تمام سلول‌های بدنم کوس می‌خوان... گوه تو این وضعیت داداش."

async def main():
    bot = Bot(token=TOKEN)
    print("هاشم آنلاین شد...")

    while True:
        post = await generate_post()
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=post)
            print(f"پست ارسال شد - {datetime.now().strftime('%H:%M')}")
        except Exception as e:
            print("خطا:", str(e))
        
        await asyncio.sleep(900)  # هر ۱۵ دقیقه

asyncio.run(main())
