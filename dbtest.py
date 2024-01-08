import sqlite3

conn = sqlite3.connect("th3.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS th3(
        song_name   TEXT,
        bpm         REAL
)""")
