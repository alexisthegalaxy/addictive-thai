from npc.npc import make_letter_beaten, Npc


def add_wild_letter(wild_letter: Npc):
    if wild_letter.letter.get_total_xp() > 1:
        make_letter_beaten(wild_letter)
    wild_letter.ma.add_npc(wild_letter)


def add_npc(npc: Npc, condition=True):
    if condition:
        npc.ma.add_npc(npc)


def no_callback(al, npc):
    print('no_callback')
    pass
