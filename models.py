import sqlite3

# open connection and get a cursor
conn = sqlite3.connect('thai.db')
c = conn.cursor()


def find_word(thai):
    answers = list(c.execute(f"SELECT * FROM words WHERE thai = '{thai}'"))
    if answers:
        return answers[0]
    else:
        return None


def insert_word(thai, english, tones):
    if not find_word(thai):
        c.execute(f"INSERT INTO words (thai, english, tones) VALUES ('{thai}', '{english}', '{tones}')")
        conn.commit()
