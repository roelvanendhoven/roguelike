from abc import ABCMeta, abstractmethod
from tcod.console import Console


def calculate_middle(console, dimensions: tuple) -> tuple:
    w, h = dimensions
    new_w = (console.width // 2) - w // 2
    new_h = (console.height // 2) - h // 2
    return new_w, new_h


class Drawable(metaclass=ABCMeta):

    @abstractmethod
    def draw(self, console: Console):
        pass
