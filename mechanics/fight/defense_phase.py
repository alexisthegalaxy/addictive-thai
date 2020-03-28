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
        self.victory_text = (
            f"You passed the test of {self.fight.opponent.name}! Now, it's your turn!"
        )
        self.fails_test_text = f"You failed the test and got damaged! Time to fight back!!"

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
        elif self.fight.current_step == FightStep.DEFEAT_MESSAGE.value:
            if self.fight.player.hp == 0:
                draw_text(
                    self.al, text=f"{self.fight.opponent.name.capitalize()}: {self.fight.npc.victory_dialog[0]}", draw_text_since=self.draw_text_since
                )
            else:
                draw_text(
                    self.al, text=self.fight.npc.fails_test_text, draw_text_since=self.draw_text_since
                )

    def interact(self):
        if self.al.ui.space:
            self.al.ui.space = False
            if (
                self.fight.current_step
                == FightStep.DEFENSE_PHASE_STARTING_MESSAGE.value
            ):
                self.draw_text_since = time.time()
                self.fight.current_step = FightStep.DEFENSE_PHASE_TEST.value
                self.al.active_test = ThaiFromEnglish6(
                    self.al,
                    correct=self.fight.words[self.fight.round % len(self.fight.words)],
                    test_success_callback=self.pass_test,
                    test_failure_callback=self.fails_test,
                    will_hurt=False,
                    shows_timer=4,
                )
            elif self.fight.current_step == FightStep.DEFENSE_PHASE_END_MESSAGE.value:
                # if self.fight.player.hp == 0:
                #     self.fight.current_step = FightStep.DEFEAT_MESSAGE.value
                #     self.draw_text_since = time.time()
                # else:
                self.draw_text_since = time.time()
                self.end_defense_phase()
            elif self.fight.current_step == FightStep.DEFEAT_MESSAGE.value:
                self.fight.defeat()

    def end_defense_phase(self):
        from mechanics.fight.attack_phase import AttackPhase

        # TODO do something if player is dead
        self.fight.current_step = FightStep.ATTACK_PHASE_PICK_WEAPON.value
        self.fight.active_phase = AttackPhase(
            self.al, self.fight, self.fight.player, self.fight.opponent
        )
        self.fight.active_phase.draw_text_since = time.time()
        self.fight.defense_phase = None

    def pass_test(self):
        self.draw_text_since = time.time()
        self.fight.current_step = FightStep.DEFENSE_PHASE_END_MESSAGE.value
        self.took_test_text = self.victory_text

    def fails_test(self):
        self.draw_text_since = time.time()
        self.fight.current_step = FightStep.DEFENSE_PHASE_END_MESSAGE.value
        self.took_test_text = self.fails_test_text
        self.fight.player.hp -= 1
        self.al.active_test = None
        if self.fight.player.hp <= 0:
            self.fight.player.hp = 0
            self.fight.current_step = FightStep.DEFEAT_MESSAGE.value
            self.draw_text_since = time.time()
            print(self.al.learner.hp)
