from mechanics.fight.fighter import Fighter


class Player(Fighter):
    def __init__(self, al):
        super().__init__(al, name=al.learner.name, hp=al.learner.hp, max_hp=al.learner.max_hp)
