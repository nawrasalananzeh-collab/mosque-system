import sqlite3

conn = sqlite3.connect("mosque.db")

conn.execute("""
INSERT INTO users (username, password)
VALUES (?, ?)
""", ("admin", "1234"))

conn.commit()
conn.close()

print("Admin created ✔ username: admin / password: 1234")