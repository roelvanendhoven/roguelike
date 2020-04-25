from tcod.console import Console
from tcod.event import EventDispatch, KeyDown, K_DOWN, K_UP, TextInput

from components.ui.widgets.window import Window
from roguelike.components.ui.util import calculate_middle


class Menu(EventDispatch):

    def __init__(self, root_console, width: int, height: int, selected_index=0,
                 contents=[], title=''):
        self.root_console = root_console
        self.layer_console = self._create_layer_console(width, height)
        self.width = width
        self.height = height
        self.selected_index = selected_index
        self.contents = contents
        self.title = title
        self.x = 0
        self.y = 0
        self.hidden = True
        self.input_values = {}

    def pack(self):
        if len(self.contents) * 2 > self.height - 3:
            print('true')
            self.height = (len(self.contents) * 2) + 3
        x, y = calculate_middle(self.root_console, (self.width, self.height))
        self.x = x
        self.y = y
        self.layer_console = self._create_layer_console(self.width, self.height)
        for i, element in enumerate(self.contents, 1):
            element.x = 2
            element.y = (i * 2)
            element.width = self.width - 3
        return self

    @classmethod
    def create(cls, root_console, contents=(), width: int = 35,
               height: int = 10, title=''):
        menu = cls(root_console, width, height, contents=contents, title=title)
        menu.pack()
        menu.hidden = False
        return menu

    def draw(self):
        if not self.hidden:
            self.layer_console.draw_frame(0, 0, self.width, self.height,
                                          title=self.title, )
            for index, elem in enumerate(self.contents, 0):
                if index == self.selected_index:
                    elem.col = (245, 218, 66)
                else:
                    elem.col = (255, 255, 255)
                elem.draw(self.layer_console)
            self.layer_console.blit(self.root_console, self.x, self.y)

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
