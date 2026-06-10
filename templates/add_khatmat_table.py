import sqlite3

conn = sqlite3.connect("mosque.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS khatmat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    khatma_date TEXT,
    khatma_place TEXT,
    sheikh_name TEXT,
    notes TEXT
)
""")

conn.commit()
conn.close()

print("khatmat table created successfully")