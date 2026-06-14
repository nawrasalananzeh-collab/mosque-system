import sqlite3

conn = sqlite3.connect("mosque.db")

conn.execute("""
UPDATE users
SET password='123456'
WHERE username='admin'
""")

conn.commit()
conn.close()

print("DONE ✔️")
 