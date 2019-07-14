import tcod
from tcod.console import Console
from tcod.event import EventDispatch, KeyDown


class Input(EventDispatch):

    def __init__(self, x: int, y: int, width: int = 0, label: str = None, default: str = None, col=(255, 255, 255)):
        self.col = col
        self.x = x
        self.y = y
        self.width = width
        self.label = label
        self.text = default

    def draw(self, console: Console, col=(255, 255, 255)):
        console.print(self.x, self.y, self.label, fg=col)
        console.print(self.x + len(self.label) + 2, self.y, ' ' * (self.width - len(self.label) - 2), bg=(20, 20, 20))
        console.print(self.x + len(self.label) + 2, self.y, self.text, bg=(20, 20, 20))

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym in (tcod.KEY_BACKSPACE, 8):
            self.text = self.text[0:-1]
        else:
            self.text += chr(event.sym)


class InputBox:

    def __init__(self, width, height, selected_index=0, contents=[], title=''):
        self.width = width
        self.height = height
        self.console = Console(width, height)
        self.selected_index = selected_index
        self.contents = contents
        self.title = title

    def draw(self, console, x, y):
        self.console.draw_frame(0, 0, self.width, self.height, title=self.title, )
        for elem in self.contents:
            elem.draw(self.console)

        self.console.blit(console, x, y)
