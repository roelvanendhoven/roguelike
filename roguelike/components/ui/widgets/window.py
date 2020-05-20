"""Window Module for drawing windows containing widgets.

The window module provides a Window class that has it's own sub Console (see
tcod.console.Console). It is used for drawing widgets within a container so
that the contained widgets can be agnostic of the sub console that it is
drawn on.

"""
from typing import List

from tcod.console import Console
from roguelike.components.ui.util import Drawable


class Window(Drawable):
    """Window class to draw widgets into a contained window.

    The window class serves as a container class for widgets. It uses it's
    own tcod Console as a layer upon which it draws it's contents. After
    drawing the contents on the sub window layer the entire console is
    blitted onto the root console.

    """

    def __init__(self, width: int, height: int,
                 x: int = 0, y: int = 0) -> None:
        """Initialize the Window.

        Initialize a window object provided a root console upon which it
        draws it's contents.

        :param width: The width of this window.
        :param height: The height of the window.
        :param x: The X position relative to the root console.
        :param y: The Y position relative to the root console.
        """
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.contents = []

    @property
    def contents(self) -> List[Drawable]:
        """Return the Windows's content.

        Return a list of the widgets contained in this window. These should
        not necessarily be widget but anything drawable.

        :return: The list of Drawables contained by this Window.
        """
        return self._contents

    @contents.setter
    def contents(self, contents: List[Drawable]) -> None:
        """Set the contents of this Window.

        Set the list of contents of this Window. This should be a list of
        Drawables.

        :param contents: A list of Drawables to be contained in the Window
        :return:
        """
        self._contents = contents

    @property
    def _layer_console(self) -> Console:
        """Return the layer console upon which the content is drawn.

        :return: The Console upon which this windows draws it's content.
        """
        return self._layer_console

    @_layer_console.setter
    def _layer_console(self, layer_console: Console) -> None:
        """Set the layer console of this Window.

        :param layer_console: A tcod Console which is used to draw the
        component list upon
        :return:
        """
        self._layer_console = layer_console

    def _create_layer_console(self, height, width) -> None:
        """Create the layer console of this window.

        The layer console is a sub console upon which the content of this
        window is drawn. In the draw cycle, every widget contained by this
        window is drawn to this layer console.

        :param height:
        :param width:
        :return:
        """
        self._layer_console = Console(height, width)

    def draw(self, console: Console) -> None:
        """Draw the contents of this Window and blit them to root console.

        Loop over the contents list containing the widgets within this
        window. Then, call the draw method on each one of them given the
        layer console this window is drawn on.

        :return: None
        """
        for widget in self.contents:
            widget.draw(self._layer_console)
        self._layer_console.blit(console, self.x, self.y)


class BorderedWindow(Window):
    """Bordered Window class draws a border along it's edges.

    Window subclass that draws a border around it's edges before the
    drawing of the contents. Optionally, a title can be given to the window
    which is draw for the frame of this window.
    """

    def __init__(self, root_console: Console, width: int, height: int,
                 x: int = 0, y: int = 0, title: str = '') -> None:
        """Initialize the Window.

        Initialize a window object provided a root console upon which it
        draws it's contents.

        :param root_console: The console on which this window is drawn.
        :param width: The width of this window.
        :param height: The height of the window.
        :param x: The X position relative to the root console. Defaults to 0
        or most left.
        :param y: The Y position relative to the root console. Defaults to 0
        for most upper.
        :param title: The title of the window to draw
        """
        super().__init__(root_console, width, height, x, y)
        self.title = title

    def draw(self, console: Console) -> None:
        """Draw the contents of this Window and blit them to root console.

        Loop over the contents list containing the widgets within this
        window. Then, call the draw method on each one of them given the
        layer console this window is drawn on. After that, create a border
        along the edges of this window.

        :return: None
        """
        self._layer_console.draw_frame(0, 0, self.width, self.height)
        super(self).draw(console)
