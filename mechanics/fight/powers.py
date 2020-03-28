import random
from math import log as ln
from typing import List, Any, Dict
from mechanics.fight.fighter import Fighter


def get_allowed_time(tones_effects: Dict[str, Any], attacker: Fighter, receiver: Fighter) -> float:
    time_multiplier = tones_effects.get("time_multiplier", 1)
    available_time = time_multiplier * receiver.time
    return available_time


def maybe_perform_attack(tones_effects: Dict[str, Any], attacker: Fighter, receiver: Fighter) -> bool:
    available_time = get_allowed_time(tones_effects, attacker, receiver)
    # The following formula returns 0.5 if available_time = 10, which is the default.
    probability_pass_test = min(max(0.5 * ln(available_time) / ln(10), 0.05), 0.95)
    if random.uniform(0, 1) > probability_pass_test:
        perform_attack(tones_effects, attacker, receiver)
        return True
    return False


def perform_attack(tones_effects: Dict[str, Any], attacker: Fighter, receiver: Fighter):
    damage_amount = 1  # eventually, will be different for each word, rarer words being hard-hitters
    damage_multiplier = tones_effects.get("damage_multiplier", 1)
    damage_dealt = damage_amount * damage_multiplier * attacker.attack / receiver.defense
    receiver.hp -= damage_dealt
    has_vampiric_effect = tones_effects.get("has_vampiric_effect", False)
    if has_vampiric_effect:
        attacker.hp += damage_dealt / 2
    is_dangerous = tones_effects.get("is_dangerous", False)
    if is_dangerous:
        attacker.hp -= damage_dealt


def apply_effects(tones_effects: Dict[str, Any], attacker: Fighter, receiver: Fighter, receiver_took_damage: bool) -> List[str]:
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
        amount_healed = attacker.heals(1)
        special_effects_text.append(f"{attacker.name.capitalize()}'s HP increased by {amount_healed}!")

    if receiver.active_healing > 0 and not receiver_took_damage:
        previous_hp = receiver.hp
        receiver.heals(receiver.active_healing)
        future_hp = receiver.hp
        special_effects_text.append(f"{receiver.name.capitalize()}'s HP went from {previous_hp} to {future_hp}!")

    if receiver.number_of_poisons > 0:
        damage = receiver.gets_damaged(receiver.number_of_poisons * attacker.poison_strength)
        special_effects_text.append(f"{receiver.name.capitalize()} takes {damage} poison damage!")

    adds_poisons = tones_effects.get("adds_poisons", 0)
    if adds_poisons and receiver_took_damage:
        receiver.number_of_poisons += adds_poisons
        special_effects_text.append(f"The test was poisoned and {receiver.name} will now")
        special_effects_text.append(f"take {receiver.number_of_poisons * attacker.poison_strength} damage each turn.")

    if "raise_defense_by" in tones_effects:
        raise_defense_by = tones_effects["raise_defense_by"]
        previous_defense = attacker.defense
        attacker.defense *= raise_defense_by
        future_defense = attacker.defense
        special_effects_text.append(f"The defense of {attacker.name} raised from {previous_defense} to {future_defense}!")

    if "increase_active_healing" in tones_effects:
        increase_active_healing_by = tones_effects["increase_active_healing"]
        previous_active_healing = attacker.active_healing
        attacker.active_healing += increase_active_healing_by
        future_active_healing = attacker.active_healing
        special_effects_text.append(f"The active healing of {attacker.name} raised from {previous_active_healing} to {future_active_healing}!")

    if "multiply_damage_by" in tones_effects:
        multiply_damage_by = tones_effects["multiply_damage_by"]
        previous_attack = attacker.attack
        attacker.attack *= multiply_damage_by
        future_attack = attacker.attack
        special_effects_text.append(f"The attack of {attacker.name} raised from {previous_attack} to {future_attack}!")

    if "increase_time_by_seconds" in tones_effects:
        increase_time_by_seconds = tones_effects["increase_time_by_seconds"]
        previous_time = attacker.time
        attacker.time += increase_time_by_seconds
        future_time = attacker.time
        special_effects_text.append(f"The time {attacker.name} has to answer tests")
        special_effects_text.append(f"raised from {previous_time} to {future_time}!")

    if "increase_time_by_ratio" in tones_effects:
        increase_time_by_ratio = tones_effects["increase_time_by_ratio"]
        previous_time = attacker.time
        attacker.time *= increase_time_by_ratio
        future_time = attacker.time
        special_effects_text.append(f"The time {attacker.name} has to answer tests")
        special_effects_text.append(f"raised from {previous_time} to {future_time}!")

    return special_effects_text
