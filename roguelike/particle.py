import tcod.console
import tcod
from typing import List
import random


class Emitter:

    def __init__(self, console, pconf: dict, x: int, y: int, w: int, h: int, rate: int = 1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.rate = rate
        self.pconf = pconf

        self.console: tcod.console.Console = console
        self.particles: List[Particle] = []

    def create_particle(self):
        for i in range(self.rate):
            self.particles.append(
                Particle(self.x + random.randint(0, self.w - 1),
                         self.y + random.randint(0, self.h - 1), **self.pconf))

    def draw(self):
        for p in self.particles:
            p.simulate()
            if p.life <= 0 or p._fadec >= 1:
                self.particles.remove(p)
            p.draw(self.console)


class Particle:

    def __init__(self, x, y, vx: tuple = (1, 1), vy: tuple = (-1, -1), ax: float = 0, ay: float = 0,
                 col: tuple = (50, 50, 50),
                 fade: float = 0, length: int = 1, height: int = 1, life: int = 50):
        self.x = x
        self.y = y

        self.length = length
        self.height = height

        self.col = col
        self.fade = fade
        self._fadec = 0

        self.ax = ax
        self.ay = ay

        self.vx = random.randint(*vx) / 100
        self.vy = random.randint(*vy) / 20

        self.life = life

    def simulate(self):
        self.x += self.vx
        self.y += self.vy
        self._fadec += self.fade
        self.col = tcod.color_lerp(self.col, (0, 0, 0), self._fadec)
        self.vx += self.ax
        self.vy += self.ay
        self.life -= 1

    def draw(self, console: tcod.console.Console):
        for i in range(self.height):
            console.print(int(self.x), int(self.y - i), ' ' * self.length, bg=self.col, bg_blend=tcod.BKGND_ADD)
