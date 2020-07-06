from anewrealm.components.ui.widgets.menu_mixin import MenuItem
from tcod.console import Console
from tcod.event import EventDispatch, KeyDown, TextInput, K_RETURN, K_BACKSPACE


class Input(MenuItem, EventDispatch):

    def __init__(self, label: str = '', default: str = '', col=(255, 255, 255)):
        self.col = col
        self.x = 0
        self.y = 0
        super().__init__(self.x, self.y)
        self.width = 0
        self.label = label
        self.text = default
        self.on_enter_pressed = None

    def get_max_input_length(self):
        return self.width - len(self.label) - 3

    def draw(self, console: Console):
        console.print(self.x, self.y, self.label, fg=self.col)
        console.print(self.x + len(self.label) + 2, self.y,
                      ' ' * (self.width - len(self.label) - 3), bg=(20, 20, 20))
        console.print(self.x + len(self.label) + 2, self.y, self.text,
                      fg=self.col, bg=(20, 20, 20))

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym in (K_BACKSPACE, 8):
            self.text = self.text[0:-1]
        elif event.sym == K_RETURN:
            if self.on_enter_pressed:
                self.on_enter_pressed()

    def ev_textinput(self, event: TextInput) -> None:
        if self.get_max_input_length() > len(self.text):
            self.text += event.text
