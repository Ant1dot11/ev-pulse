import feedparser

RSS_URL = "https://electrek.co/feed/"


def get_latest_news(limit=5):
    feed = feedparser.parse(RSS_URL)

    news_list = []

    for news in feed.entries[:limit]:
        news_list.append({
            "title": news.title,
            "link": news.link
        })

    return news_list


if __name__ == "__main__":
    news = get_latest_news()

    print("Останні новини:\n")

    for item in news:
        print(f"• {item['title']}")