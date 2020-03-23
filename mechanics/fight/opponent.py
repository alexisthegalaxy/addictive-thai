from mechanics.fight.fighter import Fighter


class Opponent(Fighter):
    def __init__(self, al, npc):
        super().__init__(al, name=npc.name, hp=npc.hp, max_hp=npc.hp)
