import sqlite3

DB_NAME = "evpulse.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS published_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE,
            title TEXT,
            source TEXT,
            score INTEGER,
            published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def is_published(link):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM published_news WHERE link = ?",
        (link,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def add_published(link, title="", source="", score=0):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO published_news
        (link, title, source, score)
        VALUES (?, ?, ?, ?)
    """, (link, title, source, score))

    conn.commit()
    conn.close()


def get_statistics():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM published_news"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return {
        "published": total
    }