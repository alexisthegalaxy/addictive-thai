from mechanics.fight.fighter import Fighter
from models import get_least_known_known_words


class Player(Fighter):
    def __init__(self, al):
        super().__init__(al, name=al.learner.name, hp=al.learner.hp, max_hp=al.learner.max_hp)
        self.word_cards = get_least_known_known_words(number_of_words_to_get=4)
