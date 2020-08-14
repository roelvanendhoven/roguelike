from tcod import CHAR_ARROW_N, CHAR_ARROW_S
from tcod.console import Console
from tcod.event import KeyDown, EventDispatch, K_DOWN, K_UP

from anewrealm.components.ui.util import Drawable


class Textbox(Drawable, EventDispatch):
    """Textbox displays a newline separated list of messages.

    Textbox is built to create scroll capability as soon as the list spills
    over the height of the widget.
    """

    messages = []

    def __init__(self, x: int = 0, y: int = 0, width: int = 1,
                 height: int = 1):
        super().__init__(x, y, width, height)
        self.scroll_offset = 0

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self.height - 3:
            self.scroll_offset = len(self.messages) - (
                    self.height - 3)

    def draw(self, console: Console):
        console.print_box(1, 1, self.width - 2,
                          self.height - 3,
                          ''.join(self.messages[self.scroll_offset:]),
                          fg=(255, 244, 122))
        if len(self.messages) > self.height - 3:
            console.print(self.width - 2, 1, chr(CHAR_ARROW_N))
            console.print(self.width - 2,
                          self.height - 3, chr(CHAR_ARROW_S))

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == K_DOWN:
            if self.scroll_offset < len(self.messages) - (
                    self.height - 3):
                self.scroll_offset += 1
        if event.sym == K_UP:
            if self.scroll_offset > 0:
                self.scroll_offset -= 1
