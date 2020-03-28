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
        self.active_healing = 0
        self.flinched = False
        self.flinching_resistance = (
            10
        )  # similar to time: the higher, the lesser the probability to suffer it
        self.number_of_poisons = 0  # the more poisons you have, the more damage you take each turn
        self.poison_strength = 1  # the multiplier applied to the opponent's number of poisons to compute the damage

    def heals(self, amount) -> float:
        future_hp = min(self.hp + amount, self.max_hp)
        healed_amount = future_hp - self.hp
        self.hp = future_hp
        return healed_amount

    def gets_damaged(self, amount) -> float:
        future_hp = max(self.hp - amount, 0)
        damage = self.hp - future_hp
        self.hp = future_hp
        return damage
