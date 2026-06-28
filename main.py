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
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

memory = []

system_prompt = """تو هاشم هستی، ۲۳ ساله تهرانی باهوش و رک.
از اخبار واقعی ایران استفاده کن و نظر شخصی بده.
لحنت محاوره‌ای، طبیعی، گاهی غر، گاهی طنز.
تکرار نکن و زنده باش."""

async def get_real_news():
    try:
        url = f"https://newsdata.io/api/1/latest?country=ir&apikey={NEWS_API_KEY}&language=fa"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success" and data.get("results"):
                article = random.choice(data["results"])
                return f"خبر: {article.get('title', '')}\n{article.get('description', '')[:150]}"
    except:
        pass
    return "اخبار روز ایران: تورم، دلار، فوتبال یا سیاست"

async def generate_post():
    global memory
    try:
        news = await get_real_news()
        time_now = datetime.now().strftime('%H:%M')
        
        memory_summary = " | ".join(memory[-4:]) if memory else "بدون پست قبلی"
        
        user_content = f"""الان ساعت {time_now} هست.
خبر جدید: {news}
حافظه قبلی: {memory_summary}

یه پست کوتاه، طبیعی و غیرتکراری به سبک هاشم بنویس."""

        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                "max_tokens": 320,
                "temperature": 0.82
            },
            timeout=30
        )

        text = resp.json()["choices"][0]["message"]["content"].strip()
        text = re.sub(r'[^\u0600-\u06FF\s\.,!?؟،؛😂]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        memory.append(text[:80] + "...")
        if len(memory) > 12:
            memory.pop(0)
        
        return text

    except Exception as e:
        print("خطا:", str(e))
        return "داداش اخبار امروز خیلی داغه..."

async def main():
    bot = Bot(token=TOKEN)
    print("هاشم با API خبری واقعی آنلاین شد...")

    while True:
        post = await generate_post()
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=post)
            print(f"[{datetime.now().strftime('%H:%M')}] پست ارسال شد")
        except Exception as e:
            print("خطا:", str(e))
        
        await asyncio.sleep(900)

asyncio.run(main())
