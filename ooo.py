from lexicon.items import Word

import sqlite3

conn = sqlite3.connect('thai.db')
c = conn.cursor()
answers = list(c.execute(f"SELECT * FROM words WHERE thai = '{'ข้าว'}'"))
print(answers)








