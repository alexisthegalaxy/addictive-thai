from datetime import datetime
import random
import sqlite3

from typing import Optional

from bag.bag import Compartment
from bag.item import Item
from direction import Direction

CONN = sqlite3.connect("thai.db")
CURSOR = CONN.cursor()

#
# def find_word_by_id(id):
#     word_db = list(CURSOR.execute(f"SELECT * FROM words WHERE id = '{id}'"))[0]
#     # id = word_db[0]
#     # split_form = word_db[1]
#     # english = word_db[2]
#     # tone = word_db[3]
#     # pos = word_db[4]
#     # in_sentence = word_db[5]
#     # thai = word_db[6]
#     return word_db
#


def find_word_by_thai(thai_word: str) -> Optional[int]:
    """Return id of that db thai word"""
    try:
        word_id = list(CURSOR.execute(f"SELECT id FROM words WHERE thai = '{thai_word}'"))[0]
        return word_id[0]
    except IndexError:
        print(f'COULD NOT FIND WORD IN DB FOR {thai_word}')
        raise IndexError


def get_word_by_id(word_id):
    from lexicon.items import Word

    word_db = list(CURSOR.execute(f"SELECT * FROM words WHERE id = '{word_id}'"))[0]
    id = word_db[0]
    split_form = word_db[1]
    english = word_db[2]
    tones = word_db[3]
    pos = word_db[4]
    # in_sentence = word_db[5]  # TODO
    thai = word_db[5]
    word = Word(
        id=id, split_form=split_form, thai=thai, english=english, tones=tones, pos=pos
    )
    return word


def xp_from_word(word_id: int) -> int:
    total_xp = list(CURSOR.execute(
        f"SELECT user_word.total_xp FROM user_word "
        f"WHERE word_id = '{word_id}'"
    ))
    if not total_xp:
        return -1
    wi = total_xp[0][0]
    return wi


def find_word_by_thai_get_id(thai):
    print(thai)
    id = list(CURSOR.execute(f"SELECT id FROM words WHERE thai = '{thai}'"))[0][0]
    return id


def increase_xp(thai, value):
    """ increase xp by value """
    learner_id = get_active_learner_id()
    word_id = find_word_by_thai_get_id(thai)
    a = list(CURSOR.execute(
        f"SELECT user_word.total_xp FROM user_word "
        f"WHERE user_word.word_id = {word_id} "
        f"AND user_word.user_id = {learner_id};"
    ))
    if a:
        CURSOR.execute(
            f"UPDATE user_word "
            f"SET total_xp = total_xp + {value} "
            f"WHERE user_word.word_id = {word_id} "
            f"AND user_word.user_id = {learner_id};"
        )
    else:
        # we need to create the word
        CURSOR.execute(
            f"INSERT INTO user_word (word_id, user_id, total_xp, level, next_threshold, previous_threshold) "
            f"VALUES ('{word_id}', '{learner_id}', 1, 1, 1, 1);"
        )

    CONN.commit()


def increase_xp_letter_by_id(letter_id, xp_amount):
    learner_id = get_active_learner_id()
    a = list(CURSOR.execute(
        f"SELECT user_letter.total_xp FROM user_letter "
        f"WHERE user_letter.letter_id = {letter_id} "
        f"AND user_letter.user_id = {learner_id};"
    ))
    if a:
        CURSOR.execute(
            f"UPDATE user_word "
            f"SET total_xp = total_xp + {value} "
            f"WHERE user_word.word_id = {letter_id} "
            f"AND user_word.user_id = {learner_id};"
        )
    else:
        # we need to create the word
        CURSOR.execute(
            f"INSERT INTO user_letter (letter_id, user_id, total_xp, level, next_threshold, previous_threshold) "
            f"VALUES ('{letter_id}', '{learner_id}', 1, 1, 1, 1);"
        )

    CONN.commit()


def create_new_user(name):
    # Create a row in user and a row in user_details
    starting_map = 'house_learner_f2'
    starting_x = 5
    starting_y = 10
    starting_money = 0
    starting_hp = 5

    learner_id = CURSOR.execute(
        f"INSERT INTO users (name, is_playing, current_map, x, y, money, hp)"
        f"VALUES ('{name}', '1', '{starting_map}', '{starting_x}', '{starting_y}', '{starting_money}', '{starting_hp}')"
    ).lastrowid
    CONN.commit()

    last_healing_map = 'house_learner_f2'
    last_healing_x = 5
    last_healing_y = 10
    direction = Direction.DOWN.value
    max_hp = 5
    last_saved_timestamp = datetime.now().isoformat()
    CURSOR.execute(
        f"INSERT INTO user_details (user_id, last_healing_map, last_healing_x, last_healing_y, direction, max_hp, last_saved_timestamp)"
        f"VALUES ('{learner_id}', '{last_healing_map}', '{last_healing_x}', '{last_healing_y}', '{direction}', '{max_hp}', '{last_saved_timestamp}')"
    )
    CONN.commit()


def set_active_player(name):
    # 1 - Set all users to non-playing
    CURSOR.execute(
        f"UPDATE users "
        f"SET is_playing = 0 ")
    CONN.commit()

    # 1 - Check if there is a user in the DB under that name
    no_user_found = list(
        CURSOR.execute(f"SELECT is_playing FROM users WHERE name = '{name}'")
    ) == []

    if no_user_found:
        create_new_user(name)
    else:
        CURSOR.execute(
            f"UPDATE users "
            f"SET is_playing = 1 "
            f"WHERE name = '{name}'")
        CONN.commit()


def get_current_map(al):
    answers = list(CURSOR.execute("SELECT current_map FROM users WHERE is_playing = 1"))
    if answers:
        return al.mas.get_map_from_name(answers[0][0])


def get_current_xy(al):
    answers = list(CURSOR.execute("SELECT x, y FROM users WHERE is_playing = 1"))
    if answers:
        x = answers[0][0]
        y = answers[0][1]
        return x, y


def save_user_details_to_db(al):
    learner_id = get_active_learner_id()
    last_healing_place_x, last_healing_place_y, last_healing_place_map = al.learner.last_healing_place
    last_healing_place_map_filename = last_healing_place_map.filename
    direction = al.learner.direction.value
    max_hp = al.learner.max_hp
    last_saved_timestamp = datetime.now().isoformat()
    CURSOR.execute(
        f"UPDATE user_details "
        f"SET last_healing_map = '{last_healing_place_map_filename}',"
        f"  last_healing_x = {last_healing_place_x},"
        f"  last_healing_y = {last_healing_place_y},"
        f"  direction = {direction},"
        f"  max_hp = {max_hp},"
        f"  last_saved_timestamp = '{last_saved_timestamp}' "
        f"WHERE user_id={learner_id}"
    )
    CONN.commit()


def load_user_details(al):
    # TODO:
    #  Create a user_details table for users that don't have one yet.
    _, last_healing_map_name, last_healing_x, last_healing_y, direction, max_hp, last_saved_timestamp = list(CURSOR.execute(
        f"SELECT user_details.* FROM user_details "
        f"JOIN users ON users.id = user_details.user_id "
        f"WHERE users.is_playing = 1"
    ))[0]

    al.learner.direction = Direction(direction)
    al.learner.last_healing_place = (last_healing_x, last_healing_y, al.mas.get_map_from_name(last_healing_map_name))
    al.learner.max_hp = max_hp
    al.learner.last_saved_timestamp = datetime.fromisoformat(last_saved_timestamp)


def load_current_x_y_money_hp_ma(al):
    answers = list(
        CURSOR.execute("SELECT x, y, money, hp, current_map FROM users WHERE is_playing = 1")
    )
    if answers:
        al.learner.x = answers[0][0]
        al.learner.y = answers[0][1]
        al.learner.money = answers[0][2]
        al.learner.hp = answers[0][3]
        al.learner.ma = al.mas.get_map_from_name(answers[0][4])
        al.mas.current_map = al.learner.ma


def create_user_item(learner_id, item_id, quantity):
    CURSOR.execute(
        f"INSERT INTO user_items (user_id, item_id, quantity)"
        f"VALUES ('{learner_id}', '{item_id}', '{quantity}')"
    )
    CONN.commit()


def update_user_item(learner_id, item_id, quantity):
    CURSOR.execute(
        f"UPDATE user_items "
        f"SET quantity = {quantity} "
        f"WHERE user_id = '{learner_id}' AND item_id = '{item_id}'"
    )
    CONN.commit()


def item_exists(learner_id, item_id) -> bool:
    results = list(CURSOR.execute(
        f"SELECT item_id "
        f"FROM user_items "
        f"WHERE user_id = '{learner_id}' AND item_id = '{item_id}'"
    ))
    return results and results[0]


def save_bag(al: 'All'):
    learner_id = get_active_learner_id()
    for item in al.bag.get_all_items():
        item_exist = item_exists(learner_id, item.name_id)
        if item_exist:
            update_user_item(learner_id, item.name_id, item.amount)
        else:
            create_user_item(learner_id, item.name_id, item.amount)


def load_bag(al: 'All'):
    learner_id = get_active_learner_id()
    results = list(CURSOR.execute(
        f"SELECT item.id, item.name, item.description, item.price, item.compartment, user_item.quantity "
        f"FROM items item "
        f"JOIN user_items user_item "
        f"ON item.id = user_item.item_id "
        f"WHERE user_item.user_id = {learner_id}"
    ))
    items = [Item(
        name_id=item[0],
        name=item[1],
        description=item[2],
        price=item[3],
        compartment=Compartment(item[4]),
        amount=item[5],
    ) for item in results]
    for item in items:
        if item.compartment == Compartment.BATTLE:
            al.bag.battle.append(item)
        if item.compartment == Compartment.OUT_OF_BATTLE:
            al.bag.out_of_battle.append(item)
        if item.compartment == Compartment.BONUS:
            al.bag.bonus.append(item)
        if item.compartment == Compartment.QUEST:
            al.bag.quest.append(item)


def get_item_from_name(item_name: str) -> Optional[Item]:
    results = list(CURSOR.execute(
        f"SELECT item.name, item.id, item.description, item.price, item.compartment "
        f"FROM items item "
        f"WHERE item.id = '{item_name}'"
    ))
    name, item_id, description, price, compartment = results[0]
    item = Item(
        name_id=item_id,
        name=name,
        description=description,
        price=price,
        compartment=Compartment(compartment),
    )
    return item


def save_user_to_db(al, x, y, money, hp, current_map):
    CURSOR.execute(
        f"UPDATE users SET x = {x}, y = {y}, money = {money}, hp = {hp}, current_map='{current_map}' WHERE is_playing = 1"
    )
    CONN.commit()


def find_word_by_id_get_thai(id):
    thai = list(CURSOR.execute(f"SELECT thai FROM words WHERE id = '{id}'"))[0][0]
    return thai


def insert_word(thai, english, tones):
    if not find_word_by_thai(thai):
        CURSOR.execute(
            f"INSERT INTO words (thai, english, tones) VALUES ('{thai}', '{english}', '{tones}')"
        )
        CONN.commit()


def get_active_learner_id():
    answers = list(CURSOR.execute("SELECT id FROM users WHERE is_playing = 1"))
    if answers:
        return answers[0][0]


def get_known_words():
    learner_id = get_active_learner_id()
    answers = list(
        CURSOR.execute(
            f"SELECT id FROM user_word WHERE user_id = {learner_id} AND total_xp > 5"
        )
    )
    if answers:
        return answers[0][0]


def get_words_with_a_teaching_order():
    return list(
        CURSOR.execute(
            f"SELECT thai, english FROM main.words WHERE teaching_order > 0 "
        )
    )


def get_random_known_word_id():
    user_id = get_active_learner_id()
    known_words = list(
        CURSOR.execute(
            f"""
        SELECT word_id
        FROM user_word
        WHERE total_xp > 0
          AND user_id = '{user_id}'
    """
        )
    )
    return random.choice(known_words)[0]


def get_event_status(event_key: str) -> int:
    user_id = get_active_learner_id()
    event_status = list(
        CURSOR.execute(
            f"""
            SELECT status
            FROM events_user
            WHERE event_key = '{event_key}'
              AND user_id = '{user_id}'
            """
        )
    )
    if event_status and event_status[0]:
        return event_status[0][0]
    else:
        CURSOR.execute(
            f"""
            INSERT  
            INTO events_user (user_id, event_key, status)
            VALUES ('{user_id}', '{event_key}', 0)
            """
        )
        CONN.commit()
        return 0


def increment_event(event_key: str):
    user_id = get_active_learner_id()
    get_event_status(event_key)
    CURSOR.execute(
        f"UPDATE events_user "
        f"SET status = events_user.status + 1 "
        f"WHERE events_user.user_id = {user_id} "
        f"AND events_user.event_key = '{event_key}';"
    )
    CONN.commit()


def set_event(event_key: str, value: int):
    user_id = get_active_learner_id()
    CURSOR.execute(
        f"UPDATE events_user "
        f"SET status = '{value}' "
        f"WHERE events_user.user_id = {user_id} "
        f"AND events_user.event_key = '{event_key}';"
    )
    CONN.commit()


def get_random_word_id() -> "Word":
    from lexicon.items import Word

    random_word_db = random.choice(
        list(
            CURSOR.execute(
                f"""
        SELECT id, split_form, english, tones, pos, thai
        FROM words
    """
            )
        )
    )
    return Word(
        id=random_word_db[0],
        split_form=random_word_db[1],
        english=random_word_db[2],
        tones=random_word_db[3],
        pos=random_word_db[4],
        thai=random_word_db[5],
    )


def find_user_word(user_id, word_id):
    answers = list(
        CURSOR.execute(
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
        CURSOR.execute(
            f"INSERT INTO user_word (user_id, word_id, total_xp, level, next_threshold, previous_threshold) VALUES ('{user_id}', '{word_id}', '{total_xp}', '{level}', '{next_threshold}', '{previous_threshold}')"
        )
        CONN.commit()
