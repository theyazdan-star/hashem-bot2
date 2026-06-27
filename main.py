import asyncio
from datetime import datetime
import requests
import os
import random
import re

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GROQ_KEY = os.getenv("GROQ_KEY")

system_prompt = """تو هاشم هستی، ۲۳ ساله تهرانی، پراید ۲۰۶ سفید داری، زیدت همیشه ساغره، رفیقت مهدی نیری تو دزفوله.
زبانت فقط فارسی محاوره‌ای تهرانی واقعی، خشن، هورمونی، بی‌ادب و گاهی خیلی سکسی.

موضوعات مورد علاقه‌ت:
- پراید و تعمیرگاه
- ساغر و حال کردن
- دخترا، کون گنده، سکس، خیانت
- تورم، ترافیک، دانشگاه، فوتبال، مهدی

سبک نظر دادنت در مورد دخترا:
- خیلی مستقیم و هورمونی باش
- گاهی ترن‌آف کنی ولی اعتراف کنی که وسوسه‌کننده‌ست
- نظرات جنجالی و واقعی جوونای ایرانی بده

مثال‌های واقعی از سبک تو:
- "لیترالی دخترایی که کون گنده دارن بدجوری ترن آفم میکنن، ولی همینا باعث میشن مردای ایرونی به زناشون خیانت کنن👎"
- "کون گنده دیدم دیگه چشمامو نمی‌تونم ازش بردارم، ولی ازدواج باهاش؟ نه بابا، فقط برای حال کردن"
- "داداش اگه زنم کون گنده داشته باشه خیانت نمی‌کنم، ولی اکثر دخترای بیرون کونشون انفجاریه، چیکار کنم؟"
- "تمام سلول‌های بدنم کوس می‌خوان وقتی یه کون گنده تو شلوار لگ می‌بینم اوف"
- "پرایدم واسه تعمیر رفته، حالم گرفته داداش"
"""

def get_tweet_examples():
    examples = [
        "فاکینگ یک ساعت و نیمه که رو یه نقطه توی ترافیک گیر کردم 🤬",
        "اگه میتونی ۶ لیتر الکل بزنی نام نویسی کن بیارمت جمع 😎",
        "پرایدم واسه تعمیر رفته، حالم گرفته داداش",
        "ارزونترین ماشین ۴۰۰ تومن، اجاره ۱۰ تومن، حقوق ۱۵ تومن... داریم می‌میریم",
        "تمام سلول‌های بدنم کوس می‌خوان... وضعیت گوهه",
        "باشگاه رفتم فقط موز برداشتم موندم اونجا 😂",
        "استاد دانشگاه سخت نگیره ناراحت می‌شم ولی این یکی درست درس هم نمی‌ده"
    ]
    return random.sample(examples, 3)

async def generate_post():
    try:
        examples = get_tweet_examples()
        examples_text = "\n".join([f"- {ex}" for ex in examples])
        
        user_content = f"""الان ساعت {datetime.now().strftime('%H:%M')} هست.

چند تا پست واقعی جوونای تهرانی:
{examples_text}

حالا تو به عنوان هاشم یه پست جدید و طبیعی بنویس. خیلی شبیه همون سبک باش. گاهی هم در مورد دخترا و کون گنده و خیانت نظر بده."""

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
                    {"role": "user", "content": user_content}
                ],
                "max_tokens": 320,
                "temperature": 0.93,
                "top_p": 0.95
            },
            timeout=25
        )
        
        if resp.status_code != 200:
            return random.choice([
                "اوف داداش وضعیت گوهه امشب...",
                "تمام سلول‌های بدنم کوس می‌خوان... خسته‌م",
                "پرایدم بازم خراب شد، گوه خوردم",
                "تورم داره ما رو می‌کشه داداش",
                "لیترالی دخترایی که کون گنده دارن بدجوری ترن آفم میکنن 👎"
            ])

        text = resp.json()["choices"][0]["message"]["content"].strip()
        
        # پاک‌سازی
        text = re.sub(r'[^\u0600-\u06FF\uFB8A\u067E\u0686\u06AF\s\.,!?؟،؛😂🔥💦😈😏]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    except Exception as e:
        print("خطا در تولید پست:", str(e))
        return "تمام سلول‌های بدنم کوس می‌خوان... گوه تو این وضعیت داداش."

async def main():
    bot = Bot(token=TOKEN)
    print("هاشم آنلاین شد...")

    while True:
        post = await generate_post()
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=post)
            print(f"[{datetime.now().strftime('%H:%M')}] پست ارسال شد")
        except Exception as e:
            print("خطای ارسال به تلگرام:", str(e))
        
        # هر ۱۵ دقیقه
        await asyncio.sleep(900)

asyncio.run(main())
