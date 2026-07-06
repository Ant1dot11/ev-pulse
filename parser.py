import feedparser
from sources import RSS_SOURCES


def get_latest_news(limit=20):
    news_list = []

    for rss in RSS_SOURCES:
        feed = feedparser.parse(rss)

        for news in feed.entries[:10]:
            news_list.append({
                "title": news.title,
                "summary": getattr(news, "summary", ""),
                "link": news.link,
                "source": feed.feed.get("title", rss)
            })

    # удаляем дубликаты по ссылке
    unique_news = []
    links = set()

    for item in news_list:
        if item["link"] not in links:
            unique_news.append(item)
            links.add(item["link"])

    return unique_news[:limit]


if __name__ == "__main__":
    news = get_latest_news()

    print(f"Знайдено новин: {len(news)}\n")

    for item in news:
        print(f"[{item['source']}] {item['title']}")