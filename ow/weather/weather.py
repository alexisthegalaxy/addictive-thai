import math
from datetime import datetime
from typing import List

import pygame


class Shaking(object):
    def __init__(self, period, intensity):
        self.period = period  # in milliseconds
        self.intensity = intensity


class Weather(object):
    def __init__(
        self,
        h_shaking=None,
        v_shaking=None,
        cos_light_flashing=None,
        rain=False,
        lightning=False,
        wind=False,
    ):
        self.h_shaking = h_shaking
        self.v_shaking = v_shaking
        self.cos_light_flashing = cos_light_flashing
        self.rain = rain
        self.lightning = lightning
        self.wind = wind

    def get_offset_x(self):
        if self.h_shaking:
            t = datetime.now().microsecond
            p = self.h_shaking.period
            i = self.h_shaking.intensity
            return math.cos(t / p) * i
        return 0

    def get_offset_y(self):
        if self.h_shaking:
            t = datetime.now().microsecond
            p = self.v_shaking.period
            i = self.v_shaking.intensity
            return math.cos(t / p) * i
        return 0

    def draw_cos_light_flashing(self, al):
        ui = al.ui
        screen = ui.screen
        color = self.cos_light_flashing[2]
        s = pygame.Surface((ui.width, ui.height))  # the size of your rect
        t = datetime.now().second + datetime.now().microsecond / 1_000_000
        transparency = 64 + 92 * math.cos(t * 3)
        s.set_alpha(transparency)  # alpha level
        s.fill((color))  # this fills the entire surface
        screen.blit(s, (0, 0))

        # pygame.draw.rect(
        #     screen, , (0, 0, )
        # )

    def draw(self, al):
        if self.cos_light_flashing:
            self.draw_cos_light_flashing(al)

no_weather = Weather()

plane_crashing = Weather(
    h_shaking=Shaking(period=100000, intensity=5),  # (period, intensity)
    v_shaking=Shaking(period=5700, intensity=2),  # (period, intensity)
    cos_light_flashing=(2.7, 0.5, (255, 0, 0)),  # (period, transparency, color)
)

rain = Weather(
    rain=True
)

lightning_wind_storm = Weather(
    rain=True,
    lightning=True,
    wind=True,
)

lightning_storm = Weather(
    rain=True,
    lightning=True,
)

wind_storm = Weather(
    rain=True,
    wind=True,
)


def get_all_weathers() -> List[Weather]:
    return []
