from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Union, Tuple, List, TYPE_CHECKING

from tcod.console import Console
from tcod.event import EventDispatch


def align_center(rectangle: Union[Console, Drawable],
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

    This functions is a helper for aligning menu boxes in the middle of the
    screen.

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
    """Drawable interface

    Abstraction never hurts. This is an abstract class that drawables should
    inherit denoting their drawability. Since a drawable is always drawn on a
    console, the drawable class denotes the x, y, width and height properties.
    """

    def __init__(self, x: int = 0, y: int = 0,
                 width: int = 0, height: int = 0):
        """Initialize properties.

        This satisfies the linter.
        """
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, console: Console) -> None:
        """Draw this object to a console

        :param console: a tcod.Console
        :return: None
        """
        pass

    @property
    def width(self) -> int:
        """Return the width of the Drawable.

        :return: The width of the Drawable as an int
        """
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        """Set the width of the Drawable.

        :param width: The width of the Drawable as an int
        :return: None
        """
        self._width = width

    @property
    def height(self) -> int:
        """Return the height of the Drawable.

        :return: The height of the Drawable as an int
        """
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        """Set the height of the Drawable.

        :param height: The height of the Drawable as an int
        :return: None
        """
        self._height = height

    @property
    def x(self) -> int:
        """Return the X position of the Drawable.

        :return: The X position of the Drawable relative to the widget it
        is drawn upon.
        """
        return self._x

    @x.setter
    def x(self, x: int):
        """Set the X coordinate of the Drawable.

        :param x: The X coordinate of the Drawable relative to the widget it
        is drawn upon.
        :return: None
        """
        self._x = x

    @property
    def y(self) -> int:
        """Return the Y position of the Drawable.

        :return: The Y position of the Drawable relative to the widget it
        is drawn upon.
        """
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        """Set the Y coordinate of the Drawable.

        :param y: The Y coordinate of the Drawable relative to the widget it
        is drawn upon.
        :return: None
        """
        self._y = y


class Widget(Drawable, metaclass=ABCMeta):

    @abstractmethod
    def draw(self, console: Console):
        """Draw this object to a console

        :param console: a tcod.Console
        :return: None
        """
        pass


class Container(Drawable, metaclass=ABCMeta):
    """Container class that holds multiple drawables.

    """
    def __init__(self, x: int, y: int, width: int, height: int,
                 contents: List[Union[Drawable, EventDispatch]]):
        super().__init__(x, y, width, height)
        self.contents = contents

    @property
    def event_handlers(self) -> List[EventDispatch]:

        # TODO make this lazy. now it filters every time. Only if contents
        #  are updated or something
        return list(
            filter(lambda x: isinstance(x, EventDispatch), self.contents))

    @property
    def drawables(self) -> List[Drawable]:

        # TODO make this lazy. now it filters every time
        dr = list(filter(lambda x: isinstance(x, Widget), self.contents))
        return dr

    @property
    def contents(self) -> List[Union[Drawable, EventDispatch]]:
        return self._contents

    @contents.setter
    def contents(self, contents: List[Union[Drawable, EventDispatch]]) -> None:
        self._contents = contents

    def pack(self, container: Drawable):
        if len(self.drawables) * 2 > self.height - 3:
            print('true')
            self.height = (len(self.drawables) * 2) + 3
        x, y = align_center(container, (self.width, self.height))
        self.x = x
        self.y = y
        for i, element in enumerate(self.drawables, 1):
            element.x = 2
            element.y = (i * 2)
            element.width = self.width - 3
        return self

    def draw(self, console: Console):
        for widget in self.drawables:
            widget.draw(console)
