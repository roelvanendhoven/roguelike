from tcod.console import Console
from tcod.event import EventDispatch, KeyDown, K_DOWN, K_UP, TextInput

from components.ui.widgets.window import Window
from roguelike.components.ui.util import align_center, Widget, Container


class Menu(EventDispatch, Container):

    def __init__(self, window: Window, width: int, height: int,
                 selected_index=0,
                 contents=[], title=''):
        self.window = window
        self.width = width
        self.height = height
        self.selected_index = selected_index
        self.contents = contents
        self.title = title
        self.x = 0
        self.y = 0
        self.hidden = True
        self.input_values = {}

    @classmethod
    def create(cls, root_console, contents=(), width: int = 35,
               height: int = 10, title=''):
        menu = cls(root_console, width, height, contents=contents, title=title)
        menu.pack()
        menu.hidden = False
        return menu

    def draw(self):
        if not self.hidden:
            self.console.draw_frame(0, 0, self.width, self.height,
                                    title=self.title, )
            for index, elem in enumerate(self.contents, 0):
                if index == self.selected_index:
                    elem.col = (245, 218, 66)
                else:
                    elem.col = (255, 255, 255)
                elem.draw(self.console)
            self.console.blit(self.console, self.x, self.y)

    def ev_textinput(self, event: TextInput) -> None:
        self.contents[self.selected_index].dispatch(event)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.contents)
        elif event.sym == K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.contents)
        else:
            self.contents[self.selected_index].dispatch(event)


class MenuItem:

    def __init__(self, x=0, y=0):
        self.y = x
        self.x = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
