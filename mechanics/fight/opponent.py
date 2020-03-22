from mechanics.fight.fighter import Fighter


class Opponent(Fighter):
    def __init__(self, al, npc):
        super().__init__(al, hp=npc.hp)
