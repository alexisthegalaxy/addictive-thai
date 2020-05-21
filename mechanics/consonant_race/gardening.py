from npc.spell import get_spells_of_player


class Gardening(object):
    def __init__(self, al, ma, x, y):
        self.al = al
        self.ma = ma
        self.x = x
        self.y = y
        a = get_spells_of_player()
        print(a)

