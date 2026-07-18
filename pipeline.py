from parser import get_latest_news
from collector import remove_duplicates
from editor import get_best_news
from selector import choose_best_article
from article import get_article
from ai import create_post
from fact_checker import check_post
from config import USE_FACT_CHECKER

NEWS_LIMIT = 15
TOP_ARTICLES = 5


def build_best_post():

    print("🔎 Отримуємо новини...")
    print("➡️ Викликаємо parser...")

    news = get_latest_news(NEWS_LIMIT)
    print("✅ Parser завершив роботу")

    if not news:
        return None

    news = remove_duplicates(news)

    print(f"📰 Отримано {len(news)} новин")

    ranking = get_best_news(news)

    if not ranking:
        print("❌ AI не зміг оцінити новини.")
        return None

    candidates = []

    for i, item in enumerate(ranking[:TOP_ARTICLES], start=1):

        news_item = next(
            (
                n for n in news
                if n["title"] == item["title"]
            ),
            None
        )

        if news_item is None:
            continue

        print(f"📖 Завантажуємо: {news_item['title']}")

        article = get_article(news_item["link"])

        if not article["text"]:
            continue

        candidates.append(
            {
                "id": f"EVP{i:03}",
                "title": news_item["title"],
                "text": article["text"],
                "image": article["image"],
                "source": news_item["source"],
                "link": news_item["link"],
                "score": item["score"],
                "reason": item.get("reason", "")
            }
        )

    if not candidates:
        return None

    print("🧠 AI читає статті...")

    winner_ai = choose_best_article(candidates)

    if not winner_ai:
        return None

    winner = next(
        (
            article for article in candidates
            if article["id"] == winner_ai["id"]
        ),
        None
    )

    if winner is None:
        return None

    print(f"🏆 Остаточний вибір: {winner['title']}")

    print("\n🖼 Фото:")

    if winner["image"]:
        print(winner["image"])
    else:
        print("❌ Фото не знайдено")

    print()

    post = create_post(
        winner["title"],
        winner["text"],
        winner["source"]
    )

    if USE_FACT_CHECKER:
        if winner["score"] < 80:
            print("🧐 Перевіряємо факти...")
            post = check_post(post)
        else:
            print("✅ Перевірку фактів пропущено (AI Score високий)")

    return {
            "post": post,
            "article": winner["text"],
            "title": winner["title"],
            "title": winner["title"],
            "link": winner["link"],
            "source": winner["source"],
            "image": winner["image"],
            "score": winner["score"],
            "reason": winner_ai.get("reason", "")
        }


if __name__ == "__main__":

    result = build_best_post()

    if result:
        print("\n✅ Пост створено!\n")
        print(result["post"])
    else:
        print("\n❌ Не вдалося створити пост.")