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

        self.console: tcod.console.Console = console
        self.particles: List[Particle] = []

    def create_particle(self):
        self.particles.append(
            Particle(self.x + random.randint(self.x, self.x + self.w), self.y, fade=0.0000000001, col=(2, 4, 8)))

    def draw(self):
        self.console.print(1, 1, str(len(self.particles)))
        for p in self.particles:
            p.simulate()
            p.draw(self.console)
            if p.life <= 0 or p.fadec >= 1:
                self.particles.remove(p)
            pass


class Particle:

    def __init__(self, x, y, col: tuple = (50, 50, 50), fade: float = 0):
        self.x = x
        self.y = y

        self.length = 25

        self.col = col
        self.fade = fade
        self.fadec = 0

        self.ax = 0
        self.ay = -0.001

        self.vx = random.randint(-5, 5) / 100
        self.vy = random.randint(-4, -1) / 20

        self.life = 200

    def simulate(self):
        self.x += self.vx
        self.y += self.vy
        self.fadec += self.fade
        self.col = tcod.color_lerp(self.col, (0, 0, 0), self.fadec)
        self.vx += self.ax
        self.vy += self.ay
        self.life -= 1

    def draw(self, console: tcod.console.Console):
        console.print(int(self.x), int(self.y), ' ' * self.length, bg=self.col, bg_blend=tcod.BKGND_ADD)
        console.print(int(self.x), int(self.y - 1), ' ' * self.length, bg=self.col, bg_blend=tcod.BKGND_ADD)
        console.print(int(self.x), int(self.y - 2), ' ' * self.length, bg=self.col, bg_blend=tcod.BKGND_ADD)
        console.print(int(self.x), int(self.y - 3), ' ' * self.length, bg=self.col, bg_blend=tcod.BKGND_ADD)
