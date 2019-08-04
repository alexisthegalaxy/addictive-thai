import random
import sqlite3

# from db import get_db_cursor, get_db_conn
conn = sqlite3.connect('thai.db')
c = conn.cursor()


def find_word_by_id(id):
    word_db = list(c.execute(f"SELECT * FROM words WHERE id = '{id}'"))[0]
    id = word_db[0]
    split_form = word_db[1]
    english = word_db[2]
    tone = word_db[3]
    pos = word_db[4]
    in_sentence = word_db[5]
    thai = word_db[6]
    return word_db


def get_word_by_id(word_id):
    from lexicon.items import Word
    word_db = list(c.execute(f"SELECT * FROM words WHERE id = '{word_id}'"))[0]
    id = word_db[0]
    split_form = word_db[1]
    english = word_db[2]
    tones = word_db[3]
    pos = word_db[4]
    # in_sentence = word_db[5]  # TODO
    thai = word_db[5]
    word = Word(
        id=id,
        split_form=split_form,
        thai=thai,
        english=english,
        tones=tones,
        pos=pos,
    )
    return word



def get_current_map(al):
    answers = list(c.execute("SELECT current_map FROM users WHERE is_playing = 1"))
    if answers:
        return al.mas.get_map_from_name(answers[0][0])


def get_current_xy(al):
    answers = list(c.execute("SELECT x, y FROM users WHERE is_playing = 1"))
    if answers:
        x = answers[0][0]
        y = answers[0][1]
        return x, y


def get_current_x_y_money_hp(al):
    answers = list(c.execute("SELECT x, y, money, hp FROM users WHERE is_playing = 1"))
    if answers:
        x = answers[0][0]
        y = answers[0][1]
        money = answers[0][2]
        hp = answers[0][3]
        return x, y, money, hp


def save_user_to_db(al, x, y, money, hp, current_map):
    c.execute(f"UPDATE users SET x = {x}, y = {y}, money = {money}, hp = {hp}, current_map='{current_map}' WHERE is_playing = 1")
    conn.commit()


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
