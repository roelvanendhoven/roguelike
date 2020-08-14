from tcod.console import Console
from tcod.event import EventDispatch, KeyDown, TextInput, K_RETURN, K_BACKSPACE

from anewrealm.components.ui.util import Drawable


class Input(Drawable, EventDispatch):

    def __init__(self, label: str = '', default: str = '', x: int = 0,
                 y: int = 0, width: int = 1, height: int = 1):
        super().__init__(x, y, width, height)
        self.label = label
        self.text = default
        self.on_enter_pressed = None

    def get_max_input_length(self):
        return self.width - len(self.label) - 3

    def draw(self, console: Console):
        console.print(self.x, self.y, self.label, fg=self.fg, bg=self.bg)
        console.print(self.x + len(self.label), self.y,
                      ' ' * (self.width - len(self.label) - 2),
                      fg=self.fg, bg=self.bg)
        console.print(self.x + len(self.label), self.y, self.text,
                      fg=self.fg, bg=self.bg)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym in (K_BACKSPACE, 8):
            self.text = self.text[0:-1]
        elif event.sym == K_RETURN:
            if self.on_enter_pressed:
                self.on_enter_pressed()

    def ev_textinput(self, event: TextInput) -> None:
        if self.get_max_input_length() > len(self.text):
            self.text += event.text
