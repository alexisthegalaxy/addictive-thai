import random
from math import log as ln

# from mechanics.fight.fighter import Fighter
#
#
# def deals_damage(al, fight, attacker: Fighter, receiver: Fighter, amount: float) -> float:
#     """
#     attacker and receiver can be Player or Opponent
#     """
#     damage_dealt = amount * attacker.attack / receiver.defense
#     receiver.hp -= damage_dealt
#     return damage_dealt
#
#
# def heals(al, fight, fighter: Fighter, amount):
#     health_healed = amount * fighter.healing_power
#     fighter.hp += health_healed
#
#
# def deals_vampiric_damage(al, fight, attacker, receiver, amount):
#     damage_dealt = deals_damage(al, fight, attacker, receiver, amount)
#     health_healed = damage_dealt / 2
#     attacker.hp += health_healed
from typing import List


def perform_attack(tones_effects, attacker, receiver) -> bool:
    damage_amount = 1  # eventually, will be different for each word, rarer words being hard-hitters

    damage_multiplier = tones_effects.get("damage_multiplier", 1)

    damage_dealt = damage_amount * damage_multiplier * attacker.attack / receiver.defense
    time_multiplier = tones_effects.get("time_multiplier", 1)
    available_time = time_multiplier * receiver.time
    # The following formula returns 0.5 if available_time = 10, which is the default.
    probability_pass_test = min(max(0.5 * ln(available_time) / ln(10), 0.05), 0.95)
    if random.uniform(0, 1) > probability_pass_test:
        # then, test fails
        receiver.hp -= damage_dealt
        has_vampiric_effect = tones_effects.get("has_vampiric_effect", False)
        if has_vampiric_effect:
            attacker.hp += damage_dealt / 2
        return True
    return False


def apply_effects(tones_effects, attacker, receiver, receiver_took_damage) -> List[str]:
    special_effects_text = []
    # special_effects_text.append(f"There was no special effect.")
    if "reduce_time" in tones_effects:
        receiver.time *= tones_effects["reduce_time"]
        special_effects_text.append(f"{receiver.name.capitalize()}'s time to answer all tests was reduced by 25%!")

    may_induce_flinching = tones_effects.get("may_induce_flinching", False)
    if may_induce_flinching:
        probability_flinches = min(max(0.5 * ln(receiver.flinching_resistance) / ln(10), 0.05), 0.95)
        receiver.flinched = random.uniform(0, 1) > probability_flinches
        if receiver.flinched:
            special_effects_text.append(f"{receiver.name.capitalize()} flinched and can't attack for one turn!")

    has_happy_effect = tones_effects.get("has_happy_effect", False)
    if has_happy_effect and not receiver_took_damage:
        attacker.hp += 1.0
        special_effects_text.append(f"You got a HP back!")

    if "raise_defense_by" in tones_effects:
        raise_defense_by = tones_effects["raise_defense_by"]
        previous_defense = attacker.defense
        attacker.defense *= raise_defense_by
        future_defense = attacker.defense
        special_effects_text.append(f"Your defense raised from {previous_defense} to {future_defense}!")

    if "multiply_damage_by" in tones_effects:
        multiply_damage_by = tones_effects["multiply_damage_by"]
        previous_attack = attacker.attack
        attacker.attack *= multiply_damage_by
        future_attack = attacker.attack
        special_effects_text.append(f"Your attack raised from {previous_attack} to {future_attack}!")

    return special_effects_text
