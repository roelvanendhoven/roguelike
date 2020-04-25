from tcod.console import Console
from tcod.event import KeyDown, EventDispatch, K_DOWN, K_UP
from tcod import CHAR_ARROW_N, CHAR_ARROW_S


class Textbox(EventDispatch):
    """Textbox displays a newline separated list of messages.

    Textbox is built to create scroll capability as soon as the list spills
    over the height of the widget.
    """

    messages = []

    def __init__(self, root_console: Console):
        self._console = root_console
        self.scroll_offset = 0

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self._console.height - 3:
            self.scroll_offset = len(self.messages) - (self._console.height - 3)

    def draw(self, root_console: Console):
        self._console.draw_frame(0, 0, self._console.width,
                                 self._console.height)
        self._console.print_box(1, 1, self._console.width - 2,
                                self._console.height - 3,
                                ''.join(self.messages[self.scroll_offset:]),
                                fg=(255, 244, 122))
        if len(self.messages) > self._console.height - 3:
            self._console.print(self._console.width - 2, 1, chr(CHAR_ARROW_N))
            self._console.print(self._console.width - 2,
                                self._console.height - 3, chr(CHAR_ARROW_S))

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == event.K_DOWN:
            if self.scroll_offset < len(self.messages) - (
                    self._console.height - 3):
                self.scroll_offset += 1
        if event.sym == event.K_UP:
            if self.scroll_offset > 0:
                self.scroll_offset -= 1
