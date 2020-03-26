from __future__ import annotations

import time

from all import All
from lexicon.dex import Dex
import pygame

from models import get_words_with_a_teaching_order
from npc.import_npcs import import_npcs
from npc.npc_default_text import draw_npc_text
from ow.learner import Learner
from ow.overworld import Mas, CellTypes
from profile.profile import load
from sounds.thai.sound_processing import get_all_mp3_files
from ui.ui import Ui


def main_interact(al: All):
    ow_frozen = False
    if al.active_test:
        ow_frozen = True
        al.active_test.interact(al)
    elif al.active_battle:
        ow_frozen = True
        al.active_battle.interact(al)
    elif al.active_fight:
        ow_frozen = True
        al.active_fight.interact()
    if al.active_minimap:  # must happen before active_presentation
        ow_frozen = True
        al.active_minimap.interact()
    if al.active_learning:  # must happen before active_presentation
        ow_frozen = True
        al.active_learning.interact(al)
    if al.active_presentation:  # must happen before dex
        ow_frozen = True
        al.active_presentation.interact()
    if al.dex.active:
        ow_frozen = True
        al.dex.interact()
    if al.active_npc:
        ow_frozen = True
        if al.ui.space:
            al.learner.start_interacting(al)
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
    if al.ui.escape:
        al.ui.running = False


def main_draw(al: All):
    al.ui.screen.fill((0, 0, 0))
    al.mas.current_map.draw(al)
    for npc in al.mas.current_map.npcs:
        npc.draw(al)
    al.learner.draw(al)
    if al.active_npc and not al.active_npc.active_line_index == -1:
        draw_npc_text(al, al.active_npc)
    if al.active_test:
        al.active_test.draw()
        # the following is used to draw fighter's sprites even during other elements are active - for example, tests
        if al.active_battle:
            al.active_battle.draw_secondary()
        if al.active_fight:
            al.active_fight.draw_secondary()
    elif al.active_sale:
        al.active_sale.draw()
    elif al.active_battle:
        al.active_battle.draw()
    elif al.active_fight:
        al.active_fight.draw()
    if al.active_learning:
        al.active_learning.draw()
    if al.dex.active:
        al.dex.draw()
    if al.active_minimap:
        al.active_minimap.draw()
    if al.active_spell_identification:
        al.active_spell_identification.draw()
    if not al.active_fight:
        al.learner.draw_money_and_hp(al)
    pygame.display.flip()


def main():
    al = All(
        mas=Mas(),
        ui=Ui(),
        cell_types=CellTypes(),
    )
    al.learner = Learner(al, "Alexis")
    import_npcs(al)
    load(al)
    al.dex = Dex(al)
    # get_links_from_city_word("ดี", al)
    while al.ui.running:
        al.ui.listen_event(al)
        main_interact(al)
        if al.ui.lapsed_tick():
            al.ui.tick()
            al.tick_activity()
        # before_draw = time.time()
        main_draw(al)
        # print(f"fps = {1 / (time.time() - before_draw)}")
        # al.ui.clock.tick(50)


def print_thai_words_with_no_audio():
    print('all words with no audio...')
    number_of_files_to_convert = 0
    sound_files = get_all_mp3_files()
    for thai, english in get_words_with_a_teaching_order():
        if thai not in sound_files:
            print(f"{thai}           {english}")
            number_of_files_to_convert += 1
    if number_of_files_to_convert > 0:
        print(f"{number_of_files_to_convert} files to convert! 😅")


if __name__ == "__main__":
    # print_thai_words_with_no_audio()
    main()
