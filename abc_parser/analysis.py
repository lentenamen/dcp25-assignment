import sqlite3

conn = sqlite3.connect("abc_tunes.db")
cursor = conn.cursor()

# Example 1: See how many tunes you have
cursor.execute("SELECT COUNT(*) FROM tunes")
print("Total tunes:", cursor.fetchone()[0])



conn.close()
