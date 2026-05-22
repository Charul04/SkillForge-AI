import sqlite3

conn = sqlite3.connect("skillforge.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    career TEXT,
    progress INTEGER,
    xp INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully!")