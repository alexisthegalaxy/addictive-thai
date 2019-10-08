from typing import List, Optional
import json
from db import get_db_cursor, get_db_conn
from models import get_word_by_id, CONN, CURSOR, get_active_learner_id


class Growable(object):
    """
        Words, and any learnable item that can be learnt over time
        Growable have xp and a level
    """

    def __init__(self):
        self.thai = ""
        self.total_xp = 0
        self.level = 1
        self.next_threshold = 1
        self.previous_threshold = 0

    def increase_xp(self, al, value):
        # This only sets the xp for the in-memory object, and the DB manipulation is done by the inheriting class Word
        self.total_xp += value
        while self.total_xp >= self.next_threshold:
            self.level_up()

    def decrease_xp(self, al, value):
        # print('')
        # print('before the decreasing:')
        # print('total_xp = ', self.total_xp)

        final_xp = max(self.total_xp - value, 0)

        # reset
        self.total_xp = 0
        self.level = 1
        self.next_threshold = 1
        self.previous_threshold = 0

        self.increase_xp(al, final_xp)

        # print('after the decreasing')
        # print('total_xp = ', self.total_xp)
        # print('')

    def level_up(self):
        self.level += 1
        self.previous_threshold += self.level - 1
        self.next_threshold += self.level
        # print(f'{self.thai}levelled up to level {self.level}!')

    def reset(self, al, xp=0):
        if xp == 0:
            self.total_xp = 0
            self.level = 1
            self.next_threshold = 1
            self.previous_threshold = 0
            al.dex.determine_words_to_show()
        else:
            self.increase_xp(al, xp)

    def show_xp(self):
        print()
        print(f"level: {self.level}")
        print(f"total xp: {self.total_xp}")
        current_xp = self.total_xp - self.previous_threshold
        total_xp_in_level = self.next_threshold - self.previous_threshold
        print(f"current_xp: {current_xp}/{total_xp_in_level}")


class Word(Growable):
    def __init__(
        self,
        id: int,
        split_form: str = "no_split_form",
        thai: str ="no_thai",
        english="no_english",
        tones="LHMRF",
        pos="NOUN???",
        location="NOWHERE???",
        xp: Optional[str] = 0,
        x: int = -1,
        y: int = -1,
    ):
        super().__init__()
        self.id = id
        self.thai = thai
        self.split_form = split_form
        self.english = english
        self.tones = tones
        self.pos = pos
        self.location = location
        self.total_xp = xp
        self.x = x
        self.y = y

    def increase_xp(self, al, value):
        super().increase_xp(al, value)
        learner_id = get_active_learner_id()
        CURSOR.execute(
            f"UPDATE user_word "
            f"SET total_xp = {self.total_xp}, level = {self.level} "
            f"WHERE user_word.word_id = {self.id} "
            f"AND user_word.user_id = {learner_id}"
        )
        CONN.commit()

    def get_total_xp(self) -> int:
        # TODO Alexis: add a check in the case that there is no column at all
        total_xp = list(CURSOR.execute(
            f"SELECT uw.total_xp FROM user_word uw "
            f"JOIN words w on w.id = uw.word_id "
            f"JOIN users u on u.id = uw.user_id "
            f"WHERE w.id = '{self.id}'"
            f"AND u.is_playing"
        ))
        if not total_xp:
            user_id = get_active_learner_id()
            CURSOR.execute(
                f"INSERT INTO user_word (word_id, user_id, total_xp, level, next_threshold, previous_threshold) "
                f"VALUES ('{self.id}', '{user_id}', 0, 1, 1, 0)"
            )
            CONN.commit()
            return 0

        return total_xp[0][0]

    def get_syllables(self):
        return self.split_form.split("-")

    def get_sentences(self) -> List['Sentence']:
        # TODO Alexis
        sentences = []
        for sentence_db in list(get_db_cursor().execute(
            f"SELECT * FROM sentences s JOIN word_sentence ws on s.id = ws.sentence_id WHERE ws.word_id = '{self.id}'"
        )):
            thai = sentence_db[1]
            english = sentence_db[2]
            word_ids = json.loads(sentence_db[3])
            words = [
                get_word_by_id(word_id) for word_id in word_ids
            ]
            sentence = Sentence(thai=thai, english=english, words=words)
            sentences.append(sentence)
        return sentences


    @classmethod
    def get_known_words(self):
        words = []
        for word_db in list(get_db_cursor().execute(
            f"SELECT * FROM words w JOIN user_word uw on w.id = uw.word_id join users u on u.id = uw.user_id WHERE uw.total_xp > 5 AND u.is_playing = 1"
        )):
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
            words.append(word)
        return words

    @classmethod
    def get_all(cls):
        answers = list(get_db_cursor().execute(f"SELECT * FROM words"))
        words = []
        for answer in answers:
            id = answer[0]
            split_form = answer[1]
            english = answer[2]
            tones = answer[3]
            pos = answer[4]
            thai = answer[5]
            words.append(Word(
                id=id,
                split_form=split_form,
                thai=thai,
                english=english,
                tones=tones,
                pos=pos,
            ))
        return words

    @classmethod
    def get_by_split_form(cls, split_form):
        answers = list(get_db_cursor().execute(f"SELECT * FROM words WHERE split_form = '{split_form}'"))
        if answers and answers[0]:
            first_word = answers[0]
            id = first_word[0]
            split_form = first_word[1]
            english = first_word[2]
            tones = first_word[3]
            pos = first_word[4]
            thai = first_word[5]
            return Word(
                id=id,
                split_form=split_form,
                thai=thai,
                english=english,
                tones=tones,
                pos=pos,
            )
        else:
            print(f'can\'t find split_form for {split_form}')
            return None

    @classmethod
    def get_by_thai(cls, thai):
        answers = list(get_db_cursor().execute(f"SELECT * FROM words WHERE thai = '{thai}'"))
        if answers and answers[0]:
            first_word = answers[0]
            id = first_word[0]
            split_form = first_word[1]
            english = first_word[2]
            tones = first_word[3]
            pos = first_word[4]
            thai = first_word[5]
            return Word(
                id=id,
                split_form=split_form,
                thai=thai,
                english=english,
                tones=tones,
                pos=pos,
            )
        else:
            print(f'can\'t find word for {thai}')
            return None

    def __str__(self):
        return f"{self.thai} - {self.english}\n"


class Words(object):
    # def __init__(self):
    #     self.words: List[Word] = []
    #     self.words_per_map = {}  # a dictionary giving al the words for a given map

    def add_word(self, word: Word):
        self.words.append(word)
        if word.map:
            if word.map in self.words_per_map:
                self.words_per_map[word.map].append(word)
            else:
                self.words_per_map[word.map] = [word]

    def get_word(self, split_form: str):
        for word in self.words:
            if word.split_form == split_form:
                return word

    def time_to_xp_loss(self, number_of_seconds: int):
        """
        For now, there is one xp lost per day.
        Might be more complex in the future.
        """
        number_of_days = int(number_of_seconds / 86400)
        return number_of_days

    def get_known_words(self):
        return [word for word in self.words if word.total_xp > 0]

    def __str__(self):
        s = ""
        for word in self.words:
            s += str(word)
        return s

    def print(self):
        print(self)

    @classmethod
    def reset_words(cls, xp):
        CURSOR.execute(
            f"UPDATE user_word "
            f"SET total_xp = {xp}, level = 1, next_threshold = 1 "
            f"where EXISTS (SELECT 1 "
            f"    FROM users "
            f"    WHERE users.id = user_word.user_id "
            f"    AND users.is_playing = 1)"
        )
        CONN.commit()


class Sentence(object):
    def __init__(self, thai: str, english: str, words: List["Word"]):
        self.thai = thai.replace("-", "").replace("_", "")
        self.words = words
        self.english = english

    def __str__(self):
        return f"{self.thai} - {self.english}"

    @staticmethod
    def get_words_in_sentence(sentence_id):
        words_db = list(
            CURSOR.execute(
                f"SELECT * FROM words JOIN word_sentence ON words.id = word_sentence.word_id WHERE word_sentence.sentence_id = '{sentence_id}'"
            )
        )
        words = []
        for word_db in words_db:
            id = word_db[0]
            split_form = word_db[1]
            english = word_db[2]
            tones = word_db[3]
            pos = word_db[4]
            thai = word_db[5]
            words.append(
                Word(
                    id=id,
                    split_form=split_form,
                    thai=thai,
                    english=english,
                    tones=tones,
                    pos=pos,
                )
            )
        return words

    @classmethod
    def get(cls, sentence_id, al):
        sentence = list(
            al.cursor.execute(f"SELECT * FROM sentences WHERE id = '{sentence_id}'")
        )[0]
        thai = sentence[1]
        english = sentence[2]
        words = cls.get_words_in_sentence(sentence_id)
        return Sentence(thai=thai, english=english, words=words)

    @classmethod
    def get_random_known_sentence(cls):
        # TODO: for the moment, this only returns a random sentence!
        sentence = list(
            CURSOR.execute(f"SELECT * FROM sentences order by random() LIMIT 1")
        )[0]
        sentence_id = sentence[0]
        thai = sentence[1]
        english = sentence[2]
        words = cls.get_words_in_sentence(sentence_id)
        return Sentence(thai=thai, english=english, words=words)


class Sentences(object):
    def __init__(self):
        self.sentences = []

    def add_sentence(self, sentence: Sentence):
        self.sentences.append(sentence)

    def __str__(self):
        s = ""
        for sentence in self.sentences:
            s += str(sentence) + "\n"
        return s

    def print(self):
        print(self)


#
# class UserWord(object):
#     """
#     The word in relation to the user
#     """
#     def __init__(self, word):
#         self.word = word
#         self.xp = 0
#         self.lvl = 1
#
#
# class UserWords(object):
#     def __init__(self):
#         self.user_words = []
#
#     def add_word(self, user_word: UserWord):
#         self.user_words.append(user_word)
#
#     # def get_word(self, split_form: str):
#     #     for user_word in self.user_words:
#     #         if word.split_form == split_form:
#     #             return word
#
#     # def print(self):
#     #     for word in self.words:
#     #         word.print()
