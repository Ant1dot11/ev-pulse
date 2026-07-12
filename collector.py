from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


def remove_duplicates(news_list, threshold=0.80):
    """
    Удаляет похожие новости.
    """

    unique_news = []

    for news in news_list:

        duplicate = False

        for saved in unique_news:

            score = similarity(
                news["title"],
                saved["title"]
            )

            if score >= threshold:
                duplicate = True
                break

        if not duplicate:
            unique_news.append(news)

    return unique_news