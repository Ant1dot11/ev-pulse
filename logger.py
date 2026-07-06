import json
import os

FILE_NAME = "published.json"


def load_published():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_published(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def is_published(link):
    published = load_published()
    return link in published


def add_published(link):
    published = load_published()

    if link not in published:
        published.append(link)

    save_published(published)