import sqlite3

conn = sqlite3.connect("abc_tunes.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE tunes")
print("Total tunes:", cursor.fetchone()[0])



conn.close()