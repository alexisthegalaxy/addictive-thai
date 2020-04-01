import math
from datetime import datetime
import random
import pygame


class Raindrop(object):
    def __init__(self, al, wind=10):
        self.image = al.ui.images[f"rain_drop_{random.randint(0, 3)}"]
        self.x = random.randint(0, al.ui.width)
        self.y = random.randint(0, al.ui.height)
        self.velocity_x = random.uniform(-.3 + wind - wind/3, .3 + wind)
        self.velocity_y = random.uniform(15, 80)

    def falls(self, al):
        self.x = self.x + self.velocity_x
        if self.x < 0:
            self.x = al.ui.width
        if self.x > al.ui.width:
            self.x = 0

        self.y = self.y + self.velocity_y
        if self.y > al.ui.height:
            self.y = 0

    def draw(self, al):
        al.ui.screen.blit(self.image, [self.x, self.y])


class Rain(object):
    def __init__(self, al):
        self.drops = [Raindrop(al) for _ in range(300)]

    def falls(self, al):
        for drop in self.drops:
            drop.falls(al)

    def draw(self, al):
        for drop in self.drops:
            drop.draw(al)



class Shaking(object):
    def __init__(self, period, intensity):
        self.period = period  # in milliseconds
        self.intensity = intensity


class Weather(object):
    def __init__(
        self,
        al,
        h_shaking=None,
        v_shaking=None,
        cos_light_flashing=None,
        rain=None,
        lightning=False,
        wind=False,
    ):
        self.h_shaking = h_shaking
        self.v_shaking = v_shaking
        self.cos_light_flashing = cos_light_flashing
        if rain:
            self.rain = Rain(al)
        else:
            self.rain = None
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
        s = pygame.Surface((ui.width, ui.height))
        t = datetime.now().second + datetime.now().microsecond / 1_000_000
        transparency = 64 + 92 * math.cos(t * 3)
        s.set_alpha(transparency)  # alpha level
        s.fill(color)  # this fills the entire surface
        screen.blit(s, (0, 0))

    def tick(self, al):
        if self.rain:
            self.rain.falls(al)

    def draw(self, al):
        if self.cos_light_flashing:
            self.draw_cos_light_flashing(al)
        if self.rain:
            self.rain.draw(al)

# no_weather = Weather()
#
# plane_crashing = Weather(
#     h_shaking=Shaking(period=100000, intensity=5),  # (period, intensity)
#     v_shaking=Shaking(period=5700, intensity=2),  # (period, intensity)
#     cos_light_flashing=(2.7, 0.5, (255, 0, 0)),  # (period, transparency, color)
# )
#
# lightning_wind_storm = Weather(
#     rain=True,
#     lightning=True,
#     wind=True,
# )
#
# lightning_storm = Weather(
#     rain=True,
#     lightning=True,
# )
#
# wind_storm = Weather(
#     rain=True,
#     wind=True,
# )
