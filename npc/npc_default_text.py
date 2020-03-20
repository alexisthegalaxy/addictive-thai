import time
import pygame
from models import should_we_show_thai
from npc.npc import Npc


def _progressively_draw_line(
    line: str, number_of_characters_to_show, ui, screen, height, x, y
):
    line = line[:number_of_characters_to_show]
    rendered_text = ui.fonts.garuda32.render(line, True, (0, 0, 0))
    screen.blit(rendered_text, (x + 10, y + int(height / 2.2) - 20))


def draw_text(al, draw_text_since: float = 0, text: str = ""):
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
        else:
            _progressively_draw_line(
                english, number_of_characters_to_show, ui, screen, height, x, y
            )
    else:
        _progressively_draw_line(
            text, number_of_characters_to_show, ui, screen, height, x, y
        )


def draw_npc_text(al, npc: Npc):
    draw_text(al, npc.draw_text_since, npc.active_dialog[npc.active_line_index])
