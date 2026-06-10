import sqlite3

conn = sqlite3.connect("mosque.db")

# ================= USERS =================
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# ================= STUDENTS =================
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
    image TEXT,
    juz_count INTEGER DEFAULT 0,
    umrah_count INTEGER DEFAULT 0,
    umrah_dates TEXT
)
""")

# ================= SESSIONS =================
conn.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    session_time TEXT,
    supervisor TEXT
)
""")

# ================= TEACHERS =================
conn.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    age INTEGER,
    address TEXT,
    specialization TEXT,
    join_date TEXT,
    students_count INTEGER,
    status TEXT
)
""")

# ================= HAFAZ =================
conn.execute("""
CREATE TABLE IF NOT EXISTS hafaz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    juz_count INTEGER,
    sheikh TEXT,
    khatma_date TEXT,
    khatma_place TEXT
)
""")

# ================= TESTS =================
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

# ================= UMRAH =================
conn.execute("""
CREATE TABLE IF NOT EXISTS umrah_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    umrah_name TEXT,
    umrah_year TEXT,
    umrah_date TEXT,
    host_company TEXT,
    hotel_name TEXT,
    makkah_nights INTEGER,
    madinah_nights INTEGER,
    other_city TEXT,
    total_nights INTEGER,
    assistant_name TEXT
)
""")

# ================= KHATMAT =================
conn.execute("""
CREATE TABLE IF NOT EXISTS khatmat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    khatma_date TEXT,
    khatma_place TEXT,
    sheikh_name TEXT,
    mosque_name TEXT,
    city TEXT,
    country TEXT,
    age INTEGER,
    grade TEXT,
    khatma_type TEXT,
    attendance_count INTEGER,
    certificate_image TEXT,
    student_image TEXT,
    video_file TEXT,
    pdf_file TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully 🚀")