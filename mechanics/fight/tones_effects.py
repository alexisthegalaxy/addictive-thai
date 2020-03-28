from typing import Tuple, List, Any, Dict


Color = Tuple[int, int, int]
Effect = List[Any]


def get_explanatory_effects_from_tone(tones: str) -> Dict[Any, Any]:
    # The test_description should break before reaching code line 98
    if tones == "M":
        return {
            "tone_name": "Mid Tone",
            "test_type": "Time-reducer test",
            "test_description": [
                "Tests (this one too) will have only 75% of the current time to",
                "be answered.",
            ],
            "bg_color": (128, 128, 128),
            "color": (0, 0, 0),
            "effects": {"reduce_time": 0.9},
        }
    if tones == "L":
        return {
            "tone_name": "Low tone",
            "test_type": "Fast test",
            "test_description": [
                "The opponent only has a third of the usual time to answer this",
                "test.",
            ],
            "bg_color": (50, 50, 50),
            "color": (255, 255, 255),
            "effects": {"time_multiplier": 1 / 3},
        }
    if tones == "F":
        return {
            "tone_name": "Falling tone",
            "test_type": "Damaging test",
            "test_description": [
                "If the opponent answers incorrectly,",
                "they lose three times more HP.",
            ],
            "bg_color": (200, 100, 100),
            "color": (0, 0, 0),
            "effects": {"damage_multiplier": 3},
        }
    if tones == "H":
        return {
            "tone_name": "High tone",
            "test_type": "Flincher",
            "test_description": [
                "Has a probability to make the target flinch, allowing for attacking",
                "again.",
            ],
            "bg_color": (240, 240, 240),
            "color": (0, 0, 0),
            "effects": {"may_induce_flinching": True},
        }
    if tones == "R":
        return {
            "tone_name": "Rising tone",
            "test_type": "Vampiric",
            "test_description": [
                "The attacker's HP is restored by half the damage taken by the",
                "target.",
            ],
            "bg_color": (100, 200, 100),
            "color": (0, 0, 0),
            "effects": {"has_vampiric_effect": True},
        }
    if tones == "LLH":
        return {
            "tone_name": "Low-low-high tone",
            "test_type": "Good news anyway",
            "test_description": [
                "Restores 1 HP if the target passes the test.",
            ],
            "bg_color": (50, 220, 50),
            "color": (0, 0, 0),
            "effects": {"has_happy_effect": True},
        }
    if tones == "FL":
        return {
            "tone_name": "Falling-low tone",
            "test_type": "Increase defense",
            "test_description": [
                "Reduce by a third the damage taken when failing a test.",
            ],
            "bg_color": (50, 220, 50),
            "color": (0, 0, 0),
            "effects": {"raise_defense_by": 1.5},
        }
    if tones == "RF":
        return {
            "tone_name": "Rising-falling tone",
            "test_type": "Increase attack",
            "test_description": [
                "Increase by 50% the damage dealt when the target fails the test.",
            ],
            "bg_color": (50, 220, 50),
            "color": (0, 0, 0),
            "effects": {"multiply_damage_by": 1.5},
        }
    if tones == "MR":
        return {
            "tone_name": "Mid-rising tone",
            "test_type": "Dangerous attack",
            "test_description": [
                "Deals twice the damage and has higher chance to hit,",
                "but the damage dealt to the target is also dealt to the attacker.",
            ],
            "bg_color": (50, 20, 222),
            "color": (0, 0, 0),
            "effects": {"damage_multiplier": 3, "is_dangerous": True, "time_multiplier": 1 / 3},
        }
    if tones == "MM":
        return {
            "tone_name": "Mid-mid tone",
            "test_type": "Poisoned test",
            "test_description": [
                "If the opponent answers incorrectly,",
                "they get a poison marker, dealing damage each turn.",
            ],
            "bg_color": (150, 0, 100),
            "color": (0, 0, 0),
            "effects": {"adds_poisons": 0.25},
        }
    if tones == "RH":
        return {
            "tone_name": "Rising-high tone",
            "test_type": "Increase active healing",
            "test_description": [
                "You get an additional 0.25 HP each time you get a test correct.",
            ],
            "bg_color": (50, 220, 50),
            "color": (0, 0, 0),
            "effects": {"increase_active_healing": 0.25},
        }
    if tones == "FM":
        return {
            "tone_name": "Falling-mid tone",
            "test_type": "Increase time",
            "test_description": [
                "You get 1 more second to answer your tests.",
            ],
            "bg_color": (50, 220, 50),
            "color": (0, 0, 0),
            "effects": {"increase_time_by_seconds": 1},
        }
    if tones == "LL":
        return {
            "tone_name": "Low-low tone",
            "test_type": "Increase time",
            "test_description": [
                "You get 25% more time to answer your tests.",
            ],
            "bg_color": (50, 220, 50),
            "color": (0, 0, 0),
            "effects": {"increase_time_by_ratio": 1.25},
        }
    return {
        "tone_name": tones,
        "test_type": "Normal test",
        "test_description": [
            "This test has no effect coded in yet - but will nonetheless",
            "damage the opponent.",
        ],
        "bg_color": (128, 128, 128),
        "color": (0, 0, 0),
        "effects": {},
    }
