import sqlite3

conn = sqlite3.connect("mosque.db")

columns = [
    ("age", "INTEGER"),
    ("national_id", "TEXT"),
    ("sheikh_group", "TEXT"),
    ("address", "TEXT"),
    ("parent_phone", "TEXT"),
    ("image", "TEXT")
]

for name, typ in columns:
    try:
        conn.execute(f"ALTER TABLE students ADD COLUMN {name} {typ}")
        print(f"Added: {name}")
    except Exception as e:
        print(f"Skipped: {name} (already exists)")

conn.commit()
conn.close()

print("Done 🚀")