import sqlite3

conn = sqlite3.connect("mosque.db")
cur = conn.execute("SELECT username, password FROM users")

print(cur.fetchall())

conn.close()