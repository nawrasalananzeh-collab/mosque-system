import sqlite3

conn = sqlite3.connect("mosque.db")

# الطلاب
conn.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    phone TEXT,
    national_id TEXT,
    sheikh_group TEXT,
    address TEXT,
    parent_phone TEXT,
    image TEXT
)
""")

# الاختبارات
conn.execute("""
CREATE TABLE IF NOT EXISTS tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    test_type TEXT,
    score TEXT,
    date TEXT,
    notes TEXT,
    pdf_file TEXT
)
""")

conn.commit()
conn.close()

print("DB Ready 🚀")