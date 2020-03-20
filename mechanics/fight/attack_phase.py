import time
from mechanics.fight.fight_steps import FightStep
from mechanics.fight.pick_weapon import PickWeapon
from npc.npc_default_text import draw_text


class AttackPhase(object):
    def __init__(self, al, fight, words, npc):
        self.draw_text_since = time.time()
        self.al = al
        self.fight = fight
        self.words = words
        self.npc = npc
        self.pick_weapon = PickWeapon(
            al=self.al,
            fight=self.fight,
            words=self.words,
            npc=self.npc,
            attack_phase=self,
        )

    def draw(self):
        if self.fight.current_step == FightStep.ATTACK_PHASE_STARTING_MESSAGE.value:
            draw_text(
                self.al,
                text=f"Prepare a test for {self.npc.name}!",
                draw_text_since=self.draw_text_since,
            )
        if self.fight.current_step == FightStep.ATTACK_PHASE_PICK_WEAPON.value:
            self.pick_weapon.draw()

    def interact(self):
        if self.fight.current_step == FightStep.ATTACK_PHASE_STARTING_MESSAGE.value:
            if self.al.ui.space:
                self.al.ui.space = False
                self.draw_text_since = time.time()
                self.fight.current_step = FightStep.ATTACK_PHASE_PICK_WEAPON.value
        if self.fight.current_step == FightStep.ATTACK_PHASE_PICK_WEAPON.value:
            self.pick_weapon.interact()
