from abc import ABCMeta, abstractmethod
from typing import Union, Tuple, List

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

    Abstraction never hurts. This is an interface that drawables should
    inherit denoting their drawability.
    """

    @abstractmethod
    def draw(self, console: Console) -> None:
        """Draw this object to a console

        :param console: a tcod.Console
        :return: None
        """
        pass


class Widget(metaclass=ABCMeta, Drawable):

    @property
    def console(self) -> Console:
        """Return the root console which this window blits it's contents upon.

        :return: The root console upon which the window draws.
        """
        return self.console

    @console.setter
    def console(self, console: Console) -> None:
        """Set the root console upon which is drawn.

        :param console: A tcod Console object upon which this Window
        content is blitted after drawing it's content.
        :return: None
        """
        self.console = console
        pass

    @property
    def width(self) -> int:
        """Return the width of the window.

        :return: The width of the Window as an int
        """
        return self.width

    @width.setter
    def width(self, width: int) -> None:
        """Set the width of the window.

        :param width: The width of the window as an int
        :return: None
        :raises: ValueError if the window is too wide when compared to it's x
        offset
        """
        if self.x + width > self.console.width:
            raise ValueError(f'Window to wide to fit screen')
        self.width = width

    @property
    def height(self) -> int:
        """Return the height of the window.

        :return: The height of the Window as an int
        """
        return self.height

    @height.setter
    def height(self, height: int) -> None:
        """Set the height of the window.

        :param height: The height of the window as an int
        :return: None
        :raises: ValueError if the window is too high when compared to it's y
        offset
        """
        if self.y + height > self.console.height:
            raise ValueError(f'Window to high to fit screen')
        self.height = height

    @property
    def x(self) -> int:
        """Return the X position of the window.

        :return: The X position of the window relative to the root console.
        """
        return self.x

    @x.setter
    def x(self, x: int):
        """Set the X coordinate of the window.

        :param x: The X coordinate of the window relative to the root console.
        :return: None
        """
        if x < 0 or x > self.console.width:
            raise ValueError(f'X value out of parent dimensions: {x}')
        self.x = x

    @property
    def y(self) -> int:
        """Return the Y position of the window.

        :return: The Y position of the window relative to the root console.
        """
        return self.y

    @y.setter
    def y(self, y: int) -> None:
        """Set the Y coordinate of the window.

        :param y: The Y coordinate of the window relative to the root console.
        :return: None
        """
        if y < 0 or y > self.console.height:
            raise ValueError(f'X value out of parent dimensions: {y}')
        self.y = y

    @abstractmethod
    def draw(self, console: Console):
        """Draw this object to a console

        :param console: a tcod.Console
        :return: None
        """
        pass


class Container(metaclass=ABCMeta, Widget):

    @property
    def contents(self) -> List[Drawable]:
        return []

    @contents.setter
    def contents(self, contents: List[Drawable]) -> None:
        pass

    def pack(self):
        if len(self.contents) * 2 > self.height - 3:
            print('true')
            self.height = (len(self.contents) * 2) + 3
        x, y = align_center(self.console, (self.width, self.height))
        self.x = x
        self.y = y
        for i, element in enumerate(self.contents, 1):
            element.x = 2
            element.y = (i * 2)
            element.width = self.width - 3
        return self

    def draw(self, console: Console):
        for widget in self.contents:
            widget.draw(console)
