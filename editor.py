from gemini_client import generate_json

def choose_best_news(news_list):
    prompt = """
Ти — головний редактор EV Pulse.

Перед тобою список заголовків новин.

Оціни КОЖНУ новину.

Поверни ЛИШЕ JSON-масив.

Формат:

[
    {
        "title": "Назва новини",
        "score": 98,
        "reason": "Коротке пояснення"
    }
]

Критерії:

• важливість;
• актуальність;
• вплив на ринок EV;
• цікавість українській аудиторії.

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
- автономному водінню

Не віддавай високі оцінки:

- eVTOL
- літакам
- дронам
- дрібним оновленням
- малозначущим судовим справам

Новини:
"""

    for item in news_list:
        prompt += f"\n- {item['title']}"

    return generate_json(prompt)


def get_best_news(news_list):
    results = choose_best_news(news_list)

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results