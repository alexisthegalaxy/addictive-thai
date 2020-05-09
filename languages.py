

def get_font_from_locale(fonts, locale="en", size=32):
    if size != 32:
        raise NotImplementedError
    if locale == "th" or locale == "en":
        return fonts.sarabun32
    if locale == "lo":
        return fonts.lao32
    if locale == "sa":
        return fonts.sanskrit32
    if locale == "kh":
        return fonts.khmer32
    if locale == "my":
        return fonts.burmese32
    return fonts.sarabun32


def render_multilingual_text(ui, text, x, y, size=32, color=(0, 0, 0), blit=True):
    """
    Return the width of the rendered text
    """
    beginning_of_segment_x = x
    first_iteration = True
    if "{" in text:
        for segment in text.split("{"):
            if first_iteration:
                rendered_segment = ui.fonts.sarabun32.render(segment, True, color)
                ui.screen.blit(rendered_segment, (x, y))
                first_iteration = False
            else:
                locale = segment[:2]
                segment_text = segment[2:]
                font = get_font_from_locale(ui.fonts, locale, size)
                rendered_segment = font.render(segment_text, True, color)
                ui.screen.blit(rendered_segment, (beginning_of_segment_x, y))
            beginning_of_segment_x += rendered_segment.get_width()
    else:
        rendered_text = ui.fonts.sarabun32.render(text, True, (0, 0, 0))
        ui.screen.blit(rendered_text, (x, y))
