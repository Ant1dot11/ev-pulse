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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pending_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT,
            title TEXT,
            source TEXT,
            score INTEGER,
            image TEXT,
            article TEXT,
            post TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    cursor.execute("SELECT COUNT(*) FROM published_news")
    total = cursor.fetchone()[0]

    conn.close()

    return {"published": total}


# ---- pending_posts (мост между cron-процессом и процессом бота) ----

def create_pending_post(link, title, source, score, image, article, post):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pending_posts (link, title, source, score, image, article, post)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (link, title, source, score, image, article, post))

    pending_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return pending_id


def get_pending_post(pending_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT link, title, source, score, image, article, post FROM pending_posts WHERE id = ?",
        (pending_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "link": row[0],
        "title": row[1],
        "source": row[2],
        "score": row[3],
        "image": row[4],
        "article": row[5],
        "post": row[6],
    }


def update_pending_post_text(pending_id, post):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE pending_posts SET post = ? WHERE id = ?",
        (post, pending_id)
    )

    conn.commit()
    conn.close()


def delete_pending_post(pending_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM pending_posts WHERE id = ?",
        (pending_id,)
    )

    conn.commit()
    conn.close()