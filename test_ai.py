from parser import get_latest_news
from ai import create_post

news = get_latest_news(1)

post = create_post(news[0]["title"])

print(post)