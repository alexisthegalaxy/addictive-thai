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
            "tone_name": "Low Tone",
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
            "tone_name": "Falling Tone",
            "test_type": "Damaging test",
            "test_description": [
                "If the opponent answers incorrectly,",
                "they lose three times more HP.",
            ],
            "bg_color": (200, 100, 100),
            "color": (0, 0, 0),
            "effects": {"damage_multiplier": 3},
        }
    if tones == "R":
        return {
            "tone_name": "Rising Tone",
            "test_type": "Vampiric test",
            "test_description": [
                "The attacker's HP is restored by half the damage taken by the",
                "target.",
            ],
            "bg_color": (100, 200, 100),
            "color": (0, 0, 0),
            "effects": {"has_vampiric_effect": True},
        }
    if tones == "H":
        return {
            "tone_name": "High Tone",
            "test_type": "Flincher test",
            "test_description": [
                "Has a probability to make the target flinch, allowing for attacking",
                "again.",
            ],
            "bg_color": (240, 240, 240),
            "color": (0, 0, 0),
            "effects": {"may_induce_flinching": True},
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
