import json
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def choose_best_news(news_list):
    prompt = """
Ти — головний редактор українського медіа EV Pulse.

Перед тобою список новин.

Оціни КОЖНУ новину за шкалою від 0 до 100.

Критерії:

• Наскільки новина важлива для власників електромобілів.
• Наскільки вона цікава українській аудиторії.
• Наскільки вона актуальна.
• Наскільки вона впливає на ринок електромобілів.

Не віддавай високі оцінки:

- eVTOL
- літакам
- дронам
- незначним оновленням застосунків
- малозначущим судовим справам

Віддавай перевагу:

- Tesla
- BYD
- CATL
- Rivian
- Hyundai
- Kia
- Volkswagen
- Mercedes
- BMW
- Volvo
- батареям
- зарядним станціям
- новим моделям
- автономному керуванню
- програмному забезпеченню автомобілів

Поверни ЛИШЕ JSON-масив.

Приклад:

[
    {
        "number": 1,
        "score": 95,
        "reason": "Дуже важлива новина."
    },
    {
        "number": 2,
        "score": 83,
        "reason": "Цікава, але менш важлива."
    }
]

Новини:
"""

    for i, item in enumerate(news_list, start=1):
        prompt += f"\n{i}. {item['title']}"

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    data = json.loads(text)

    return data


def get_best_news(news_list):
    results = choose_best_news(news_list)

    results.sort(key=lambda x: x["score"], reverse=True)

    return results