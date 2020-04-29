from abc import ABCMeta, abstractmethod
from typing import Union, Tuple

from tcod.console import Console

from components.ui.widgets.window import Window


def align_center(rectangle: Union[Console, Window],
                 dimensions: Tuple[int, int]) -> Tuple[int, int]:
    """Return horizontally and vertically centered coordinates within a window.

    This function takes a rectangle, being a Console or a Window, and aligns
    the parameter dimensions so that it's middle is centered within the
    rectangle. It then returns the top left coordinate for these dimensions.

    For example:

    |-------Window-------|
    |                    |
    |     X--------|     |
    |     |        |     |
    |     |        |     |
    |     |--------|     |
    |                    |
    |--------------------|

    Wherein the box in the center is denoted by parameter dimensions and the
    outer box being the window. The 'X' denotes the coordinate returned to
    align dimensions in the center of the window.

    :param rectangle: A class instance that is compliant with this function.
    So far only a Console instance or a Window instance. The class should
    implement getters for a height and width attribute.
    :param dimensions: A tuple containing the desired width and height for an
    element in the Window or Console
    :return: a tuple containing the top left coordinate to centralise a box
    of size 'dimensions' within 'window'.
    """
    w, h = dimensions
    new_x = (rectangle.width // 2) - w // 2
    new_y = (rectangle.height // 2) - h // 2
    return new_x, new_y


class Drawable(metaclass=ABCMeta):

    @abstractmethod
    def draw(self, console: Console):
        pass
