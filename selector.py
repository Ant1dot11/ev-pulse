from gemini_client import generate_json

def choose_best_article(articles):
    """
    Выбирает лучшую статью среди кандидатов.
    Возвращает:
    {
        "id": "...",
        "reason": "..."
    }
    """

    prompt = """
Ти — головний редактор EV Pulse.

Перед тобою кілька повних статей.

Обери лише ОДНУ — найкращу.

Критерії:

• найбільша важливість;
• максимальний вплив на ринок EV;
• цікавість українській аудиторії;
• актуальність.

Поверни ЛИШЕ JSON.

Приклад:

{
    "id": "EVP001",
    "reason": "Найважливіша новина дня."
}

Статті:
"""

    for article in articles:

        prompt += f"""

======================================

ID:
{article["id"]}

Заголовок:
{article["title"]}

Текст:
{article["text"][:2500]}
"""

    return generate_json(prompt)