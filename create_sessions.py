import sqlite3

conn = sqlite3.connect("mosque.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    session_time TEXT,
    supervisor TEXT
)
""")

# بيانات تجريبية
conn.execute("""
INSERT INTO sessions (name, session_time, supervisor)
VALUES ('حلقة الفجر', '06:00', 'أحمد')
""")

conn.commit()
conn.close()

print("Sessions recreated + sample data added 🚀")