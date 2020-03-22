import time
from mechanics.fight.fight_steps import FightStep
from mechanics.fight.pick_weapon import PickWeapon
from mechanics.fight.powers import perform_attack, apply_effects
from npc.npc_default_text import draw_text


class AttackPhase(object):
    def __init__(self, al, fight, words, npc, player, opponent):
        self.draw_text_since = time.time()
        self.al = al
        self.fight = fight
        self.words = words
        self.npc = npc
        self.player = player
        self.opponent = opponent
        self.pick_weapon = PickWeapon(
            al=self.al,
            fight=self.fight,
            attack_phase=self,
        )
        self.chosen_weapon = None
        self.chosen_weapon_effects = None

    def draw(self):
        if self.fight.current_step == FightStep.ATTACK_PHASE_STARTING_MESSAGE.value:
            draw_text(
                self.al,
                text=f"Prepare a test for {self.npc.name}!",
                draw_text_since=self.draw_text_since,
            )
        if self.fight.current_step == FightStep.ATTACK_PHASE_PICK_WEAPON.value:
            self.pick_weapon.draw()
        if self.fight.current_step == FightStep.ATTACK_PHASE_TEST.value:
            draw_text(
                self.al,
                text=f"You attack {self.npc.name} with a test on {self.chosen_weapon.thai}...",
                draw_text_since=self.draw_text_since,
            )

    def interact(self):
        if self.fight.current_step == FightStep.ATTACK_PHASE_STARTING_MESSAGE.value:
            if self.al.ui.space:
                self.al.ui.space = False
                self.draw_text_since = time.time()
                self.fight.current_step = FightStep.ATTACK_PHASE_PICK_WEAPON.value
        if self.fight.current_step == FightStep.ATTACK_PHASE_PICK_WEAPON.value:
            self.pick_weapon.interact()
        if self.fight.current_step == FightStep.ATTACK_PHASE_TEST.value:
            if self.al.ui.space:
                self.al.ui.space = False
                self.draw_text_since = time.time()
                self.perform_attack_and_apply_effects()

    def perform_attack_and_apply_effects(self):
        perform_attack(self.chosen_weapon_effects, attacker=self.player, receiver=self.opponent)
        apply_effects(self.chosen_weapon_effects, attacker=self.player, receiver=self.opponent)

