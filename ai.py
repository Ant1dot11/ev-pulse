import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def create_post(title, article_text, source):
    prompt = f"""
Ти — головний редактор українського медіа EV Pulse.

Напиши професійний Telegram-пост українською мовою.

ПРАВИЛА:

• Не вигадуй фактів.
• Не перебільшуй.
• Не використовуй клікбейт.
• Використовуй ТІЛЬКИ інформацію зі статті.
• Якщо якоїсь інформації немає — не додавай її.

Структура:

⚡ Короткий український заголовок.

2–3 абзаци:
- що сталося;
- чому це важливо.

💡 Думка EV Pulse
(лише висновок на основі фактів статті).

🔗 Джерело: {source}

#EVPulse #Електромобілі

Заголовок статті:
{title}

Повний текст статті:
{article_text}
"""

    response = model.generate_content(prompt)

    return response.text