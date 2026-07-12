import sqlite3

conn = sqlite3.connect("evpulse.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM published_news")

conn.commit()
conn.close()

print("✅ База очищена")