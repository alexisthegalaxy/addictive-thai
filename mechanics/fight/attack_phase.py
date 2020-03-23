import time


from mechanics.fight.fight_steps import FightStep
from mechanics.fight.pick_weapon import PickWeapon
from mechanics.fight.powers import perform_attack, apply_effects
from npc.npc_default_text import draw_text


class AttackPhase(object):
    def __init__(self, al, fight, player, opponent):
        self.draw_text_since = time.time()
        self.al = al
        self.fight = fight
        self.player = player
        self.opponent = opponent
        self.pick_weapon = PickWeapon(al=self.al, fight=self.fight, attack_phase=self)
        self.chosen_weapon = None
        self.chosen_weapon_effects = None
        self.opponent_takes_damage = None
        self.special_effects_text = []
        self.special_effects_text_cursor = 0

    def draw(self):
        if self.fight.current_step == FightStep.ATTACK_PHASE_STARTING_MESSAGE.value:
            draw_text(
                self.al,
                text=f"Prepare a test for {self.opponent.name}!",
                draw_text_since=self.draw_text_since,
            )
        if self.fight.current_step == FightStep.ATTACK_PHASE_PICK_WEAPON.value:
            self.pick_weapon.draw()
        if self.fight.current_step == FightStep.ATTACK_PHASE_TEST.value:
            draw_text(
                self.al,
                text=f"You attack {self.opponent.name} with a test on {self.chosen_weapon.thai}...",
                draw_text_since=self.draw_text_since,
            )
        if self.fight.current_step == FightStep.CONGRATULATION_MESSAGE.value:
            draw_text(
                self.al,
                text=f"You defeated {self.opponent.name}!",
                draw_text_since=self.draw_text_since,
            )
        if self.fight.current_step == FightStep.ATTACK_PHASE_TEST_RESULT.value:
            if self.opponent_takes_damage:
                draw_text(
                    self.al,
                    text=f"{self.opponent.name.capitalize()} answered wrongly and took damage!",
                    draw_text_since=self.draw_text_since,
                )
            else:
                draw_text(
                    self.al,
                    text=f"{self.opponent.name.capitalize()} answered correctly and avoided the damage!",
                    draw_text_since=self.draw_text_since,
                )
        if self.fight.current_step == FightStep.ATTACK_PHASE_SPECIAL_EFFECT.value:
            draw_text(
                self.al,
                text=self.special_effects_text[self.special_effects_text_cursor],
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
                self.fight.current_step = FightStep.ATTACK_PHASE_TEST_RESULT.value
        if self.fight.current_step == FightStep.ATTACK_PHASE_TEST_RESULT.value:
            if self.al.ui.space:
                self.al.ui.space = False
                if self.special_effects_text:
                    self.draw_text_since = time.time()
                    self.fight.current_step = (
                        FightStep.ATTACK_PHASE_SPECIAL_EFFECT.value
                    )
                else:
                    self.end_attack_phase()
        if self.fight.current_step == FightStep.ATTACK_PHASE_SPECIAL_EFFECT.value:
            if self.al.ui.space:
                self.al.ui.space = False
                self.special_effects_text_cursor += 1
                if len(self.special_effects_text) > self.special_effects_text_cursor:
                    self.draw_text_since = time.time()
                else:
                    self.end_attack_phase()
        if self.fight.current_step == FightStep.CONGRATULATION_MESSAGE.value:
            if self.al.ui.space:
                self.al.ui.space = False
                self.fight.victory()

    def end_attack_phase(self):
        from mechanics.fight.defense_phase import DefensePhase

        if self.opponent.hp <= 0:
            self.fight.current_step = FightStep.CONGRATULATION_MESSAGE.value
            self.draw_text_since = time.time()
            self.fight.attack_phase = None
        else:
            self.fight.current_step = FightStep.DEFENSE_PHASE_STARTING_MESSAGE.value
            self.fight.active_phase = DefensePhase(self.al, self.fight)
            self.fight.active_phase.draw_text_since = time.time()
            self.fight.attack_phase = None
            self.fight.increase_round()

    def perform_attack_and_apply_effects(self):
        self.opponent_takes_damage = perform_attack(
            self.chosen_weapon_effects, attacker=self.player, receiver=self.opponent
        )
        self.special_effects_text = apply_effects(
            self.chosen_weapon_effects, attacker=self.player, receiver=self.opponent
        )
