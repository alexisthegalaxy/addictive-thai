from all import All


def wind(al):
    from weather.weather import Weather, Overlay
    print('the wind is starting!')
    al.weather = Weather(
        al=al,
        rain=True,
        wind=30,
        overlay=Overlay(color=(30, 30, 30), transparency=92),
        lightning=True,
    )


def spell_action(al: All, name: str):
    if name == "ลม":
        wind(al)
