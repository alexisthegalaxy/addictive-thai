import time
import pygame

from languages import render_multilingual_text
from models import should_we_show_thai
from npc.npc import Npc
from npc.question import Question


def _progressively_draw_line(
    line: str, number_of_characters_to_show, ui, screen, height, x, y
):
    x = x + 10
    y = y + int(height / 2.2) - 20
    line = line[:number_of_characters_to_show]
    render_multilingual_text(ui, text=line, x=x, y=y, size=32, color=(0, 0, 0))


def draw_text(al, draw_text_since: float = 0, text: str = "") -> bool:
    """
    Return whether the text is fully written or not (used for displaying Questions)
    """
    # 1 - Background:
    ui = al.ui
    x = 0
    y = ui.percent_height(0.9)
    width = ui.percent_width(1)
    height = ui.percent_height(0.1)

    screen = ui.screen
    pygame.draw.rect(screen, (150, 150, 150), (x, y, width, height))
    pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height], 1)

    # 2 - Draw text:
    now = time.time()
    number_of_characters_to_show = int((now - draw_text_since) * 75)
    if "//" in text:
        english, thai = text.split("//")
        we_should_show_thai = should_we_show_thai(thai)
        if we_should_show_thai:
            thai = thai.replace("_", "").replace("-", "")
            _progressively_draw_line(
                thai, number_of_characters_to_show, ui, screen, height, x, y
            )
            return number_of_characters_to_show >= len(thai)
        else:
            _progressively_draw_line(
                english, number_of_characters_to_show, ui, screen, height, x, y
            )
            return number_of_characters_to_show >= len(english)
    else:
        _progressively_draw_line(
            text, number_of_characters_to_show, ui, screen, height, x, y
        )
        return number_of_characters_to_show >= len(text)


def draw_npc_text(al, npc: Npc):
    if npc.active_line_index > -1 and type(npc.active_dialog[npc.active_line_index]) == Question:
        question = npc.active_dialog[npc.active_line_index]
        has_drawn_text = draw_text(al, npc.draw_text_since, question.precursor_text)
        if has_drawn_text:
            question.draw(al)
    else:
        draw_text(al, npc.draw_text_since, npc.active_dialog[npc.active_line_index])
