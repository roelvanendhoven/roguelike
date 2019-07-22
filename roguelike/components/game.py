'''Game module containing game logic

This module should contain logic related to gameplay.
For now this module contains a rudimentary loop switching turns between players.

'''

from typing import List
import tcod.console

class Map:
    tiles = [
        []
    ]


class Action():
    value = None
    type = None


class Entity(object):

    def __init__(self, x, y, char, col):
        self.x = x
        self.y = y

        self.char = char
        self.col = col

    def draw(self, console: tcod.console.Console):
        console.print(self.x,self.y,self.char,fg=self.col)


class Player:

    def __init__(self, name, col):
        self.name = name
        self.col = col
        self.entity = Entity(5, 5, '@', col)


class GameState:
    turncount: int = 0
    players: List[Player] = []
    current_player: Player = None

    def start(self):
        if len(self.players) > 0:
            self.current_player = self.players[0]

    def take_turn(self, action: Action):
        if action.type == 'MOVE':
            self.current_player.entity.x = action.value[0]
            self.current_player.entity.y = action.value[1]
        self.turncount += 1
        self.current_player = self.players[self.turncount % len(self.players)]

    def draw_state(self, console):
        for player in self.players:
            player.entity.draw(console)
        pass
