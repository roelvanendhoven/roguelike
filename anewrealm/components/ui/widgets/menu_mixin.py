from __future__ import annotations

from typing import List, TYPE_CHECKING, Union

from tcod.event import EventDispatch, KeyDown, K_DOWN, K_UP, TextInput

from anewrealm.components.ui.util import Container, Drawable
from constants import DEFAULT_UI_FOREGROUND, SELECTED_UI_FOREGROUND

if TYPE_CHECKING:
    # To prevent circular imports, type checking imports should be done
    # inside a block like this. At runtime, TYPE_CHECKING won't evaluate to
    # true. This is an unfortunate hack because I wasn't aware of this.
    pass


class MenuMixin(Container, EventDispatch):

    _selected_index = 0

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        self.drawables[self.selected_index].col = DEFAULT_UI_FOREGROUND
        self._selected_index = value
        self.drawables[self.selected_index].col = SELECTED_UI_FOREGROUND

    def ev_textinput(self, event: TextInput) -> None:
        self.event_handlers[self.selected_index].dispatch(event)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(
                self.contents)
        elif event.sym == K_UP:
            self.selected_index = (self.selected_index - 1) % len(
                self.contents)
        else:
            self.event_handlers[self.selected_index].dispatch(event)


class MenuItem:

    def __init__(self, x=0, y=0):
        self.y = x
        self.x = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
