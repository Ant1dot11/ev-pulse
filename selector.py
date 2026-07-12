import json
from gemini_client import generate


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

    text = generate(prompt).strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    data = json.loads(text)

    return data