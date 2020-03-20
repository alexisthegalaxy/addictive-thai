from typing import Tuple, List


Color = Tuple[int, int, int]


def get_explanatory_effects_from_tone(tones: str) -> Tuple[str, str, List[str], Color, Color]:
    if tones == "M":
        return (
            "Mid Tone",
            "Normal test",
            ["If the opponent answers incorrectly, they lose 1 HP."],
            (128, 128, 128),
            (0, 0, 0),
        )
    if tones == "L":
        return (
            "Low Tone",
            "Hard test",
            ["The opponent only has 10 seconds to answer this."],
            (50, 50, 50),
            (255, 255, 255),
        )
    if tones == "F":
        return (
            "Falling Tone",
            "Hard-Hitter",
            ["If the opponent answers incorrectly, they lose 3 HP."],
            (200, 100, 100),
            (0, 0, 0),
        )
    if tones == "R":
        return (
            "Rising Tone",
            "Vampiric test",
            ["If the opponent answers incorrectly, you steal 1 HP from them."],
            (100, 200, 100),
            (0, 0, 0),
        )
    if tones == "H":
        return (
            "High Tone",
            "Double-down",
            ["After you test your opponent, you can test them again."],
            (240, 240, 240),
            (0, 0, 0),
        )
    if tones == "MM":
        return (
            "Mid-Mid Tone",
            "Increase difficulty",
            ["The difficulty of your tests increases:", "your opponent will have lower accuracy for this test,", "and all your following tests."],
            (240, 240, 240),
            (0, 0, 0),
        )
    elif tones == "FL":
        return (
            "Mid-Mid Tone",
            "Increase difficulty",
            ["The time your opponent get to answer tests gets decreased"],
            (240, 240, 240),
            (0, 0, 0),
        )
    return f"{tones}", "Complex tones", ["Not done yet"], (240, 0, 240), (0, 0, 0)
