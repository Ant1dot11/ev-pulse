from parser import get_latest_news
from collector import remove_duplicates
from editor import get_best_news
from article import get_article_text
from ai import create_post

NEWS_LIMIT = 10


def get_best_post():
    """
    Возвращает лучшую новость.
    Используется main.py
    """
    return get_post_by_rank(0)


def get_post_by_rank(index=0):
    """
    Возвращает новость по месту в AI-рейтинге.
    Используется Telegram-ботом.
    """

    # Получаем новости со всех источников
    news = get_latest_news(NEWS_LIMIT)

    # Удаляем похожие новости
    news = remove_duplicates(news)

    if not news:
        return None

    # AI ранжирует уже очищенный список
    ranking = get_best_news(news)

    if not ranking:
        return None

    if index >= len(ranking):
        return None

    best = ranking[index]

    selected = news[best["number"] - 1]

    title = selected["title"]
    link = selected["link"]
    source = selected["source"]

    print(f"🏆 AI Score: {best['score']}/100")

    article = get_article_text(link)

    if not article:
        return None

    post = create_post(
        title,
        article,
        source
    )

    return {
        "news": news,
        "ranking": ranking,
        "current": index,
        "post": post,
        "title": title,
        "link": link,
        "source": source,
        "score": best["score"],
        "reason": best["reason"],
    }