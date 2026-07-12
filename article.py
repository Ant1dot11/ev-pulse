from newspaper import Article
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


def get_best_image(url):
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]

        tw = soup.find("meta", attrs={"name": "twitter:image"})
        if tw and tw.get("content"):
            return tw["content"]

        for script in soup.find_all(
            "script",
            type="application/ld+json"
        ):
            try:
                data = json.loads(script.string)

                if isinstance(data, dict):

                    image = data.get("image")

                    if isinstance(image, str):
                        return image

                    if isinstance(image, list) and image:
                        return image[0]

            except Exception:
                pass

        images = soup.find_all("img")

        for img in images:

            src = (
                img.get("src")
                or img.get("data-src")
                or img.get("data-lazy-src")
                or img.get("data-original")
            )

            if not src:
                continue

            src = src.strip()

            if src.startswith("//"):
                src = "https:" + src

            if src.startswith("/"):
                src = urljoin(url, src)

            bad = [
                "logo",
                "icon",
                "avatar",
                "emoji",
                "banner",
                "ads",
                "advert",
                "placeholder",
            ]

            if any(x in src.lower() for x in bad):
                continue

            return src

    except Exception as e:
        print(f"❌ Помилка пошуку фото: {e}")

    return ""


def get_article(url):

    try:

        article = Article(
            url,
            language="en"
        )

        article.download()
        article.parse()

        image = get_best_image(url)

        print("\n🖼 Фото:")
        print(image if image else "❌ Фото не знайдено")

        return {
            "text": article.text,
            "image": image
        }

    except Exception as e:

        print(f"❌ Помилка завантаження статті: {e}")

        return {
            "text": "",
            "image": ""
        }