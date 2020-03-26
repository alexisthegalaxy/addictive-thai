class Fighter(object):
    def __init__(self, al, name, hp, max_hp):
        self.al = al
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.time = 10  # seconds available to answer the test
        self.defense = 1  # a multiplier applied to the damage received
        self.attack = 1  # a multiplier applied to the damage dealt
        self.healing_power = 1  # a multiplier applied to the healing
        self.critical_ratio = 1.1  #
        self.speed = (
            1
        )  # will attack every 1 turn. if speed = 2, will only attack once every two turns
        self.active_healing = 0  # TODO
        self.flinched = False
        self.flinching_resistance = (
            10
        )  # similar to time: the higher, the lesser the probability to suffer it
