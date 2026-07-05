import feedparser

url = "https://electrek.co/feed/"

feed = feedparser.parse(url)

print("Останні новини:\n")
print("Знайдено новин:", len(feed.entries))

for news in feed.entries[:5]:
    print("•", news.title)