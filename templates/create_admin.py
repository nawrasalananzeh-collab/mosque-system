import sqlite3

conn = sqlite3.connect("mosque.db")

conn.execute("""
INSERT INTO users (
    username,
    password,
    full_name,
    role
)
VALUES (
    'admin',
    '123456',
    'مدير النظام',
    'admin'
)
""")

conn.commit()
conn.close()

print("Admin Created")