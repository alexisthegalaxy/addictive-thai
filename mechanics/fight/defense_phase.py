import time
from lexicon.tests.tests import ThaiFromEnglish6

from mechanics.fight.fight_steps import FightStep
from mechanics.fight.powers import perform_attack, apply_effects, get_allowed_time
from mechanics.fight.tones_effects import get_explanatory_effects_from_tone
from npc.npc_default_text import draw_text


class DefensePhase(object):
    def __init__(self, al, fight):
        self.draw_text_since = time.time()
        self.al = al
        self.fight = fight
        self.took_test_text = None
        self.word, self.word_effects, self.allowed_time = self.select_word()
        self.victory_text = (
            f"You passed the test of {self.fight.opponent.name}! Now, it's your turn!"
        )
        self.fails_test_text = f"You failed the test and got damaged! Time to fight back!!"
        self.player_takes_damage = None
        self.special_effects_text = []
        self.special_effects_text_cursor = 0

    def select_word(self):
        word = self.fight.words[self.fight.round % len(self.fight.words)]
        word_effects = get_explanatory_effects_from_tone(word.tones)["effects"]
        allowed_time = get_allowed_time(
            tones_effects=word_effects,
            attacker=self.fight.opponent,
            receiver=self.fight.player,
        )
        return word, word_effects, allowed_time


    def draw(self):
        if self.fight.current_step == FightStep.DEFENSE_PHASE_STARTING_MESSAGE.value:
            draw_text(
                self.al,
                text=f"Get ready, {self.fight.opponent.name} will test you!",
                draw_text_since=self.draw_text_since,
            )
        elif self.fight.current_step == FightStep.DEFENSE_PHASE_TEST_RESULT.value:
            draw_text(
                self.al, text=self.took_test_text, draw_text_since=self.draw_text_since
            )
        elif self.fight.current_step == FightStep.DEFENSE_PHASE_SPECIAL_EFFECT.value:
            draw_text(
                self.al,
                text=self.special_effects_text[self.special_effects_text_cursor],
                draw_text_since=self.draw_text_since,
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
                    correct=self.word,
                    test_success_callback=self.pass_test,
                    test_failure_callback=self.fails_test,
                    will_hurt=False,
                    allowed_time=self.allowed_time,
                )
            elif self.fight.current_step == FightStep.DEFENSE_PHASE_TEST_RESULT.value:
                if self.special_effects_text:
                    self.draw_text_since = time.time()
                    self.fight.current_step = (
                        FightStep.DEFENSE_PHASE_SPECIAL_EFFECT.value
                    )
                else:
                    self.end_defense_phase()
                # if self.fight.player.hp == 0:
                #     self.fight.current_step = FightStep.DEFEAT_MESSAGE.value
                #     self.draw_text_since = time.time()
                # else:
            elif self.fight.current_step == FightStep.DEFENSE_PHASE_SPECIAL_EFFECT.value:
                self.special_effects_text_cursor += 1
                if len(self.special_effects_text) > self.special_effects_text_cursor:
                    self.draw_text_since = time.time()
                else:
                    self.end_defense_phase()
            elif self.fight.current_step == FightStep.DEFEAT_MESSAGE.value:
                self.fight.defeat()

    def end_defense_phase(self):
        from mechanics.fight.attack_phase import AttackPhase

        if self.fight.player.flinched:
            self.restart_defense_phase()
        else:
            self.draw_text_since = time.time()
            # TODO do something if player is dead
            self.fight.current_step = FightStep.ATTACK_PHASE_PICK_WEAPON.value
            self.fight.active_phase = AttackPhase(
                self.al, self.fight, self.fight.player, self.fight.opponent
            )
            self.fight.active_phase.draw_text_since = time.time()
            self.fight.defense_phase = None

    def restart_defense_phase(self):
        self.fight.current_step = FightStep.DEFENSE_PHASE_STARTING_MESSAGE.value
        self.word, self.word_effects, self.allowed_time = self.select_word()
        self.al.ui.space = False
        self.draw_text_since = time.time()
        self.fight.increase_round()

    def pass_test(self):
        self.player_takes_damage = False
        self.apply_effects()
        self.draw_text_since = time.time()
        self.fight.current_step = FightStep.DEFENSE_PHASE_TEST_RESULT.value
        self.took_test_text = self.victory_text

    def fails_test(self):
        self.player_takes_damage = True
        self.draw_text_since = time.time()
        self.fight.current_step = FightStep.DEFENSE_PHASE_TEST_RESULT.value
        self.took_test_text = self.fails_test_text
        self.apply_effects()

        perform_attack(tones_effects=self.word_effects, attacker=self.fight.opponent, receiver=self.fight.player)
        # self.fight.player.hp -= 1
        self.al.active_test = None
        if self.fight.player.hp <= 0:
            self.fight.player.hp = 0
            self.fight.current_step = FightStep.DEFEAT_MESSAGE.value
            self.draw_text_since = time.time()
            print(self.al.learner.hp)

    def apply_effects(self):
        self.special_effects_text = apply_effects(
            tones_effects=self.word_effects,
            attacker=self.fight.opponent,
            receiver=self.fight.player,
            receiver_took_damage=self.player_takes_damage,
        )