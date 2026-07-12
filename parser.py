import feedparser

RSS_FEEDS = {
    "Electrek": "https://electrek.co/feed/",
    "InsideEVs": "https://insideevs.com/rss/news/",
    "CleanTechnica": "https://cleantechnica.com/category/cleantech/electric-vehicles/feed/",
    "Teslarati": "https://www.teslarati.com/feed/",
    "EVXL": "https://evxl.co/feed/",
}


def get_latest_news(limit_per_source=10):

    news = []

    for source, url in RSS_FEEDS.items():

        try:
            feed = feedparser.parse(url)

            for item in feed.entries[:limit_per_source]:

                news.append({
                    "title": item.title,
                    "link": item.link,
                    "source": source
                })

        except Exception as e:
            print(f"{source}: {e}")

    return news