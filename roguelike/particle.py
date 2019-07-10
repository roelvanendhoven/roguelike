import tcod.console
import tcod
from typing import List
import random


class Emitter:

    def __init__(self, console, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.pconf = {
            'fade': 0.0000000001, 'col': (2, 4, 8)
        }

        self.console: tcod.console.Console = console
        self.particles: List[Particle] = []

    def create_particle(self):
        self.particles.append(
            Particle(self.x + random.randint(self.x, self.x + self.w), self.y, **self.pconf))

    def draw(self):
        self.console.print(1, 1, str(len(self.particles)))
        for p in self.particles:
            p.simulate()
            if p.life <= 0 or p._fadec >= 1:
                self.particles.remove(p)
            p.draw(self.console)


class Particle:

    def __init__(self, x, y, vx: float = 0, vy: float = 0, ax: float = 0, ay: float = 0, col: tuple = (50, 50, 50),
                 fade: float = 0, length:float = 1, height:float=1):
        self.x = x
        self.y = y

        self.length = 25

        self.col = col
        self.fade = fade
        self._fadec = 0

        self.ax = ax
        self.ay = ay

        self.vx = random.randint(-5, 5) / 100
        self.vy = random.randint(-4, -1) / 20

        self.life = 200

    def simulate(self):
        self.x += self.vx
        self.y += self.vy
        self._fadec += self.fade
        self.col = tcod.color_lerp(self.col, (0, 0, 0), self._fadec)
        self.vx += self.ax
        self.vy += self.ay
        self.life -= 1

    def draw(self, console: tcod.console.Console):
        console.print(int(self.x), int(self.y), ' ' * self.length, bg=self.col, bg_blend=tcod.BKGND_ADD)
        console.print(int(self.x), int(self.y - 1), ' ' * self.length, bg=self.col, bg_blend=tcod.BKGND_ADD)
        console.print(int(self.x), int(self.y - 2), ' ' * self.length, bg=self.col, bg_blend=tcod.BKGND_ADD)
        console.print(int(self.x), int(self.y - 3), ' ' * self.length, bg=self.col, bg_blend=tcod.BKGND_ADD)
