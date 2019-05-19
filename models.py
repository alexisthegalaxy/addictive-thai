import random
import sqlite3

# open connection and get a cursor
conn = sqlite3.connect('thai.db')
c = conn.cursor()


def find_word_by_thai(thai):
    answers = list(c.execute(f"SELECT * FROM words WHERE thai = '{thai}'"))
    if answers:
        return answers[0]
    else:
        return None


def find_word_by_id(id):
    word_db = list(c.execute(f"SELECT * FROM words WHERE id = '{id}'"))[0]
    return word_db


def find_word_by_id_get_thai(id):
    thai = list(c.execute(f"SELECT thai FROM words WHERE id = '{id}'"))[0][0]
    return thai


def insert_word(thai, english, tones):
    if not find_word_by_thai(thai):
        c.execute(f"INSERT INTO words (thai, english, tones) VALUES ('{thai}', '{english}', '{tones}')")
        conn.commit()


def get_active_learner_id():
    answers = list(c.execute("SELECT id FROM users WHERE is_playing = 1"))
    if answers:
        return answers[0][0]


def get_known_words():
    learner_id = get_active_learner_id()
    answers = list(c.execute(f"SELECT id FROM user_word WHERE user_id = {learner_id} AND total_xp > 5"))
    if answers:
        return answers[0][0]


def get_random_known_word_id():
    user_id = get_active_learner_id()
    known_words = list(c.execute(f"""
        SELECT word_id
        FROM user_word
        WHERE total_xp > 0
          AND user_id = '{user_id}'
    """))
    return random.choice(known_words)[0]


def find_user_word(user_id, word_id):
    answers = list(
        c.execute(
            f"SELECT * FROM user_word WHERE user_id = '{user_id}' AND word_id = '{word_id}'"
        )
    )
    if answers:
        return answers[0]
    else:
        return None


def insert_user_word(
    user_id, word_id, total_xp, level, next_threshold, previous_threshold
):
    if not find_user_word(user_id, word_id):
        c.execute(
            f"INSERT INTO user_word (user_id, word_id, total_xp, level, next_threshold, previous_threshold) VALUES ('{user_id}', '{word_id}', '{total_xp}', '{level}', '{next_threshold}', '{previous_threshold}')"
        )
        conn.commit()


a = get_active_learner_id()
