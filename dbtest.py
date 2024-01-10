import sqlite3

conn = sqlite3.connect("th3.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS th3(
        song_name   TEXT,
        bpm         REAL
)""")

song_data = ('Song Title', 120.5)

# Insert data into the 'songs' table
c.execute("INSERT INTO th3 (song_name, bpm) VALUES (?, ?)", song_data)

c.execute("SELECT * FROM th3")
rows = c.fetchall()
for row in rows:
    print(row)


song_name_to_check = 'Song Title'
c.execute("SELECT * FROM th3 WHERE song_name = ?", (song_name_to_check,))

SAMErows = c.fetchall()
# Print the data
if len(SAMErows) > 1:
    print("yes, "+str(len(SAMErows)))

#c.execute("DELETE FROM th3")






conn.commit()

conn.close()
