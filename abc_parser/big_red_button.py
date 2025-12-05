import sqlite3

conn = sqlite3.connect("abc_tunes.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE abc_tunes")

conn.close()