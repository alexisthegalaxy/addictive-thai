import math
from datetime import datetime
import random
import pygame
import time


class LightningStrike(object):
    def __init__(self, al):
        self.image = al.ui.images[f"lightning_strike_{random.randint(0, 1)}"]
        self.started_at = time.time()
        self.width = 3 * 80
        self.x = random.randint(0, al.ui.width - self.width)
        self.y = 0

    def draw(self, al):
        # The first second, we show the screen being blank, and the lightning image
        if time.time() - self.started_at < 0.1:
            ui = al.ui
            screen = ui.screen
            transparency = 128
            color = (255, 255, 255)
            s = pygame.Surface((ui.width, ui.height))
            s.set_alpha(transparency)
            s.fill(color)
            screen.blit(s, (0, 0))

            al.ui.screen.blit(self.image, [self.x, self.y])
        # The second second, dark, and going back to normal
        elif time.time() - self.started_at < 1.1:
            ui = al.ui
            screen = ui.screen
            transparency = self.post_lightning_darkness(time.time() - self.started_at)
            color = (0, 0, 0)
            s = pygame.Surface((ui.width, ui.height))
            s.set_alpha(transparency)
            s.fill(color)
            screen.blit(s, (0, 0))

    def maybe_restart(self, al):
        if random.randint(0, 90) == 0:
            self.started_at = time.time()
            self.x = random.randint(0, al.ui.width - self.width)
            self.image = al.ui.images[f"lightning_strike_{random.randint(0, 2)}"]

    @staticmethod
    def post_lightning_darkness(t):
        a = -128
        b = 116
        return a * t + b



class Raindrop(object):
    def __init__(self, al, wind):
        self.image = al.ui.images[f"rain_drop_{random.randint(0, 3)}"]
        self.image.set_alpha(128)
        self.x = random.randint(0, al.ui.width)
        self.y = random.randint(0, al.ui.height)
        self.velocity_x = random.uniform(-.3 + wind - wind/3, .3 + wind)
        self.velocity_y = random.uniform(15, 80)

    def falls(self, al, wind_amplifier):
        self.x = self.x + self.velocity_x + wind_amplifier
        if self.x < 0:
            self.x = al.ui.width
        if self.x > al.ui.width:
            self.x = 0 + random.randint(0, 30)

        self.y = self.y + self.velocity_y
        if self.y > al.ui.height:
            self.y = 0 + random.randint(0, 30)

    def draw(self, al):
        al.ui.screen.blit(self.image, [self.x, self.y])


class Rain(object):
    def __init__(self, al, wind):
        self.drops = [Raindrop(al, wind=wind) for _ in range(300)]

    def falls(self, al, wind_amplifier):
        for drop in self.drops:
            drop.falls(al, wind_amplifier)

    def draw(self, al):
        for drop in self.drops:
            drop.draw(al)



class Shaking(object):
    def __init__(self, period, intensity):
        self.period = period  # in milliseconds
        self.intensity = intensity


class Overlay(object):
    def __init__(self, color, transparency):
        self.color = color
        self.transparency = transparency


class Weather(object):
    def __init__(
        self,
        al,
        h_shaking=None,
        v_shaking=None,
        cos_light_flashing=None,
        overlay=None,
        rain=None,
        lightning=None,
        wind=4,
        quake=None,
    ):
        self.h_shaking = h_shaking
        self.v_shaking = v_shaking
        self.cos_light_flashing = cos_light_flashing
        if rain:
            self.rain = Rain(al, wind)
        else:
            self.rain = None

        self.lightning = LightningStrike(al)
        self.lightning_started_at = None
        self.lightning_shape = None

        self.wind = wind
        self.overlay = overlay
        self.quake = quake

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
        s.set_alpha(transparency)
        s.fill(color)
        screen.blit(s, (0, 0))

    def tick(self, al):
        if self.rain:
            t = datetime.now().second + datetime.now().microsecond / 1_000_000
            wind_amplifier = 3 + 15 * math.cos(t / 2)
            self.rain.falls(al, wind_amplifier=wind_amplifier)
        if self.lightning:
            self.lightning.maybe_restart(al)

    def draw(self, al):
        if self.cos_light_flashing:
            self.draw_cos_light_flashing(al)
        if self.rain and not al.mas.current_map.inside:
            self.rain.draw(al)
        if self.overlay:
            ui = al.ui
            screen = ui.screen
            s = pygame.Surface((ui.width, ui.height))
            s.set_alpha(self.overlay.transparency)
            s.fill(self.overlay.color)
            screen.blit(s, (0, 0))
        if self.lightning and not al.mas.current_map.inside:
            self.lightning.draw(al)
