from parser import get_latest_news
from editor import choose_best_news

news = get_latest_news(20)

results = choose_best_news(news)

results = sorted(results, key=lambda x: x["score"], reverse=True)

print("🏆 ТОП-5 новин:\n")

for item in results[:5]:
    news_item = news[item["number"] - 1]

    print(f"{item['score']}/100")
    print(news_item["title"])
    print(item["reason"])
    print("-" * 50)