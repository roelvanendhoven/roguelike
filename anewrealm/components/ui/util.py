from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Union, Tuple, List, Dict, TYPE_CHECKING

from tcod.console import Console
from tcod.event import EventDispatch

if TYPE_CHECKING:
    # To prevent circular imports, type checking imports should be done
    # inside a block like this. At runtime, TYPE_CHECKING won't evaluate to
    # true. This is an unfortunate hack because I wasn't aware of this
    # dramatic implementation.
    from components.ui.screen import Screen
    from components.ui.widgets.window import Window


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
                 width: int = 1, height: int = 1):
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

    def __init__(self, x: int = 0, y: int = 0,
                 width: int = 1, height: int = 1):
        super().__init__(x, y, width, height)
        self.event_listeners = dict()

    @abstractmethod
    def draw(self, console: Console):
        """Draw this object to a console

        :param console: a tcod.Console
        :return: None
        """
        pass

    @property
    def event_listeners(self):
        """Return the list of event_listeners of this Widgets

        :return:
        """
        return self._event_listeners

    @event_listeners.setter
    def event_listeners(self, event_listeners: Dict[str, List[Union[Screen,
                                                                    Window,
                                                                    Widget]]]):
        self._event_listeners = event_listeners
        pass


class LayoutManager(metaclass=ABCMeta):
    """Layout interface.

    Container objects can implement a layout manager to lay out
    their contained widgets.
    """

    def __init__(self):
        self.drawables = []
        self.change_listeners = []

    @property
    def drawables(self) -> List[Drawable]:
        return self._drawables

    @drawables.setter
    def drawables(self, drawables: List[Drawable]):
        self._drawables = drawables

    @abstractmethod
    def layout_container(self, parent: Container) -> None:
        """Lay out the containers components.

        This method should implement the way that this widget should lay out
        it's contained widgets.

        :return: None
        """
        return None

    @property
    def change_listeners(self) -> List[callable]:
        return self._change_listeners

    @change_listeners.setter
    def change_listeners(self, change_listeners: List[callable]):
        self._change_listeners = change_listeners

    def add_change_listener(self, listener: callable):
        self.change_listeners.append(listener)

    def remove_change_listener(self, listener: callable):
        self.change_listeners.remove(listener)

    def remove_change_listener_by_index(self, index: int):
        self.change_listeners.pop(index)

    def notify_dimensions_changed(self):
        for listener in self.change_listeners:
            listener()


class Container(Drawable, metaclass=ABCMeta):
    """Container class that holds multiple drawables.

    A container is a class that contains multiple event listeners or
    drawables.

    The container class can hold event listeners and drawables alike.
    Setting the content of the Container splits these into the
    event_handlers and drawables accessor methods. Classes that use
    containers can differentiate between drawables and event_handlers this
    way since not all drawables need to handle events and not all
    event_handlers have to be drawn.

    """

    def __init__(self, x: int = 0, y: int = 0, width: int = 1, height: int = 1,
                 contents: List[Union[Drawable, EventDispatch]] = None):
        super().__init__(x, y, width, height)
        self.parent = None
        self._layout_manager = None
        self.contents = contents
        # TODO: ability to set layout

    @property
    def event_handlers(self) -> List[EventDispatch]:
        if self._event_handlers:
            return self._event_handlers
        return list(
            filter(lambda x: isinstance(x, EventDispatch), self.contents))

    @property
    def drawables(self) -> List[Drawable]:
        if self._drawables:
            return self._drawables
        dr = list(filter(lambda x: isinstance(x, Widget), self.contents))
        return dr

    @property
    def contents(self) -> List[Union[Drawable, EventDispatch]]:
        return self._contents

    @contents.setter
    def contents(self, contents: List[Union[Drawable, EventDispatch]]) -> None:
        self._event_handlers = None
        self._drawables = None
        self._contents = contents

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: Container):
        self._parent = parent
        pass

    @property
    def layout(self) -> LayoutManager:
        return self._layout_manager

    @layout.setter
    def layout(self, layout_manager: LayoutManager):
        """Set a layout for the container

        :param layout_manager:
        :return:
        """
        self._layout_manager = layout_manager
        if self.layout:
            self.layout.drawables = self.drawables
            self.layout.add_change_listener(self.invalidate)
        self.invalidate()

    def invalidate(self, parent: Container = None):
        """invalidate the containers layout and signal upwards.

        Invalidate the containers layout, signifying that content has
        changed and now the container needs to relayout itself. Signals
        upwards to parent containers and invalidates them too.

        :return: None
        """
        if self.layout:
            print(type(parent))
            if self.parent and type(self.parent) == Container:
                self.layout.layout_container(parent)
                self.parent.invalidate()
            else:
                self.layout.layout_container(self)

    def draw(self, console: Console):
        for widget in self.drawables:
            widget.draw(console)


class MenuLayout(LayoutManager):
    """Layoutmanager for menus.

    MenuLayout is a layout manager used for vertical menu's. It aligns the
    elements spaced by a blank line.
    """

    def layout_container(self, parent: Container = None) -> None:
        """Lay out a container vertically with a gap of 1.

        Lay out all the elements within a container. Automatically stretches
        the container vertically if elements don't fit. This invalidates the
        layout of the parent container.

        :param parent: The parent container
        :return:
        """
        print(parent, 'Calling')
        if len(parent.drawables) * 2 > parent.height - 3:
            print('true')
            parent.height = (len(parent.drawables) * 2) + 3
            self.notify_dimensions_changed()
        for i, element in enumerate(parent.drawables, 1):
            element.x = 2
            element.y = (i * 2)
            element.width = parent.width - 3

class CenteredMenu(MenuLayout):

    def layout_container(self, parent: Container = None) -> None:
        # TODO: Hier verder gaan
        super().layout_container(parent)
        parent.x, parent.y = align_center(parent, (parent.width,
                                                               parent.height))
