import asyncio

from parser import get_latest_news
from editor import get_best_news
from article import get_article_text
from ai import create_post
from publisher import publish
from logger import is_published, add_published


async def main():
    print("🔎 Шукаємо новини...")

    news = get_latest_news(20)

    if not news:
        print("❌ Новин не знайдено.")
        return

    print("🧠 AI оцінює новини...")

    ranking = get_best_news(news)

    selected_news = None
    selected_score = None
    selected_reason = None

    for item in ranking:
        candidate = news[item["number"] - 1]

        if not is_published(candidate["link"]):
            selected_news = candidate
            selected_score = item["score"]
            selected_reason = item["reason"]
            break

    if selected_news is None:
        print("✅ Усі важливі новини вже були опубліковані.")
        return

    print()
    print(f"⭐ AI Score: {selected_score}/100")
    print(f"💬 Причина: {selected_reason}")
    print()

    title = selected_news["title"]
    link = selected_news["link"]
    source = selected_news["source"]

    print(f"📰 Обрана новина:\n{title}")

    print("\n📖 Завантажуємо статтю...")

    article_text = get_article_text(link)

    if not article_text:
        print("❌ Не вдалося отримати текст статті.")
        return

    print("🤖 Створюємо пост...")

    post = create_post(title, article_text, source)

    print("\n==============================")
    print(post)
    print("==============================\n")

    print("📤 Публікуємо...")

    await publish(post)

    add_published(link)

    print("✅ Новину успішно опубліковано!")


if __name__ == "__main__":
    asyncio.run(main())