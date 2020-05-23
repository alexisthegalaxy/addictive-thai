from all import All


def ลม(al):
    from weather.weather import Weather, Overlay
    print('the wind is starting!')
    if al.weather is None:
        al.weather = Weather(
            al=al,
            # rain=True,
            wind=30,
            # overlay=Overlay(color=(30, 30, 30), transparency=92),
            # lightning=True,
        )
    else:
        al.weather.wind = 30


def หิน(al):
    from overworld import CellTypes

    x, y = al.learner.next_position()
    cell = al.mas.current_map.get_cell_at(x, y)
    cell.typ = CellTypes.boulder_2


def ผัก(al):
    from overworld import CellTypes

    def spread_field_around(al, x, y):
        cell = al.mas.current_map.get_cell_at(x, y)
        if cell.typ.letter in "草稂":
            cell.typ = CellTypes.field
            spread_field_around(al, x + 1, y)
            spread_field_around(al, x - 1, y)
            spread_field_around(al, x, y + 1)
            spread_field_around(al, x, y - 1)

    x, y = al.learner.x, al.learner.y
    spread_field_around(al, x, y)


def ฝน(al):
    print('rain is starting!!!')
    from weather.weather import Weather, Rain
    if al.weather is None:
        al.weather = Weather(
            al=al,
            rain=True,
        )
    else:
        al.weather.rain = Rain(al, al.weather.wind)


def spell_action(al: All, name: str):
    if name == "ลม":
        ลม(al)
    if name == "ฝน":
        ฝน(al)
    if name == "หิน":
        หิน(al)
    if name == "ผัก":
        ผัก(al)
