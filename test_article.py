from parser import get_latest_news
from article import get_article_text

news = get_latest_news(1)

text = get_article_text(news[0]["link"])

print(text[:3000])