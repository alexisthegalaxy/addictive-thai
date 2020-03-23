import time
from lexicon.tests.tests import ThaiFromEnglish6

from mechanics.fight.fight_steps import FightStep
from npc.npc_default_text import draw_text


class DefensePhase(object):
    def __init__(self, al, fight):
        self.draw_text_since = time.time()
        self.al = al
        self.fight = fight
        self.took_test_text = None
        self.victory_text = f"You successfully passed the test of {self.fight.opponent.name}."
        self.defeat_text = f"You failed the test of {self.fight.opponent.name}!"
        self.end_defense_phase_text = f"Now, it's your turn to attack."

    def draw(self):
        if self.fight.current_step == FightStep.DEFENSE_PHASE_STARTING_MESSAGE.value:
            draw_text(
                self.al,
                text=f"Get ready, {self.fight.opponent.name} will test you!",
                draw_text_since=self.draw_text_since,
            )
        elif self.fight.current_step == FightStep.DEFENSE_PHASE_END_MESSAGE.value:
            draw_text(
                self.al, text=self.took_test_text, draw_text_since=self.draw_text_since
            )
        # elif self.fight.current_step == FightStep.DEFENSE_PHASE_TEST.value:

    def interact(self):
        if self.al.ui.space:
            self.al.ui.space = False
            if (
                self.fight.current_step
                == FightStep.DEFENSE_PHASE_STARTING_MESSAGE.value
            ):
                self.draw_text_since = time.time()
                self.fight.current_step = FightStep.DEFENSE_PHASE_TEST.value
                self.al.active_test  = ThaiFromEnglish6(
                    self.al,
                    correct=self.fight.words[0],
                    test_success_callback=self.pass_test,
                    test_failure_callback=self.fails_test(),
                )
            elif self.fight.current_step == FightStep.DEFENSE_PHASE_END_MESSAGE.value:
                self.draw_text_since = time.time()
                if (
                    self.took_test_text == self.victory_text
                    or self.took_test_text == self.defeat_text
                ):
                    self.took_test_text = self.end_defense_phase_text
                else:
                    self.end_defense_phase()

    def end_defense_phase(self):
        from mechanics.fight.attack_phase import AttackPhase
        # TODO do something if player is dead
        self.fight.current_step = (
            FightStep.ATTACK_PHASE_PICK_WEAPON.value
        )
        self.fight.active_phase = AttackPhase(self.al, self.fight, self.fight.player, self.fight.opponent)
        self.fight.active_phase.draw_text_since = time.time()
        self.fight.defense_phase = None

    def pass_test(self):
        self.draw_text_since = time.time()
        self.fight.current_step = FightStep.DEFENSE_PHASE_END_MESSAGE.value
        self.took_test_text = self.victory_text

    def fails_test(self):
        pass
