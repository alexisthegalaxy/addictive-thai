from all import All
from lexicon.dex import Dex
from lexicon.init import init_vocab
import pygame

from npc.import_npcs import import_npcs
from ow.learner import Learner
from ow.overworld import Mas, CellTypes
from profile.profile import Profiles
from ui.ui import Ui


def main_interact(al: All):
    ow_frozen = False
    if al.active_test:
        ow_frozen = True
        al.active_test.interact(al)
    elif al.active_battle:
        ow_frozen = True
        al.active_battle.interact(al)
    if al.dex.active:
        ow_frozen = True
        al.dex.interact()
    if al.active_npc:
        ow_frozen = True
        if al.ui.space:
            al.learner.start_interacting(al)
    if al.active_learning:
        ow_frozen = True
        al.active_learning.interact(al)
    if al.active_sale:
        ow_frozen = True
        al.active_sale.interact(al)
    if any([npc.must_walk_to for npc in al.mas.current_map.npcs]):
        ow_frozen = True
    if not ow_frozen:
        if al.ui.space:
            al.learner.start_interacting(al)
        if al.learner.can_move():
            al.learner.move(al)


def main_draw(al: All):
    al.ui.screen.fill((0, 0, 0))
    al.mas.current_map.draw(al)
    for npc in al.mas.current_map.npcs:
        npc.draw(al)
    al.learner.draw(al)
    for npc in al.mas.current_map.npcs:
        if not npc.active_line_index == -1:
            npc.draw_text(al)
    if al.active_test:
        al.active_test.draw()
    elif al.active_sale:
        al.active_sale.draw()
    elif al.active_battle:
        al.active_battle.draw()
        al.active_battle.opponent_play()
    if al.active_learning:
        al.active_learning.draw()
    if al.dex.active:
        al.dex.draw()
    al.learner.draw_money_and_hp(al)
    pygame.display.flip()


def main():
    syllables, words, sentences = init_vocab()
    cell_types = CellTypes()
    mas = Mas(words, cell_types)
    mas.form_links()
    profiles = Profiles()
    profiles.set_as_profile("Alexis")
    al = All(
        mas=mas,
        words=words,
        sentences=sentences,
        syllables=syllables,
        ui=Ui(),
        cell_types=cell_types,
        profiles=profiles,
    )

    al.add_sentences_to_words()
    al.learner = Learner(al, 1, 1, (150, 0, 150))
    import_npcs(al)

    profiles.current_profile.load(al)
    al.dex = Dex(al)
    while al.ui.running:
        al.ui.listen_event(al)
        main_interact(al)
        if al.ui.lapsed_tick():
            al.ui.tick()
            al.tick_activity()
        main_draw(al)
        al.ui.clock.tick(50)


if __name__ == "__main__":
    main()
