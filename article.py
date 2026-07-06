from newspaper import Article


def get_article_text(url):
    try:
        article = Article(url, language="en")

        article.download()
        article.parse()

        return article.text

    except Exception as e:
        print(f"❌ Помилка завантаження статті: {e}")
        return ""