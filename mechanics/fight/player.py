from mechanics.fight.fighter import Fighter


class Player(Fighter):
    def __init__(self, al):
        super().__init__(al, hp=al.learner.hp)
