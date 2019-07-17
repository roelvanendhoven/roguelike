import tcod
from tcod.console import Console
from tcod.event import EventDispatch, KeyDown, TextInput
from queue import Queue, Empty


class QueueFactory:
    queue = Queue()

    @staticmethod
    def get_queue():
        return QueueFactory.queue


def get_ui_event():
    try:
        queue = QueueFactory.get_queue()
        event = queue.get(False)
        return event
    except Empty:
        pass


def calculate_middle(console, dimensions: tuple) -> tuple:
    w, h = dimensions
    new_w = (console.width // 2) - w // 2
    new_h = (console.height // 2) - h // 2
    return new_w, new_h


def create_menu(console, contents, title='', width=30, height=15):
    if len(contents) * 2 > height - 3:
        print('true')
        height = (len(contents) * 2) + 3
    x, y = calculate_middle(console, (width, height))
    menu = Menu(width, height, contents=contents, title=title)
    menu.x = x
    menu.y = y
    for i, element in enumerate(contents, 1):
        element.x = 2
        element.y = (i * 2)
        element.width = menu.width - 3
    menu.hidden = False
    return menu


class UIEvent:

    def __init__(self, type: str, value: dict = None):
        if value is None:
            self.value = dict()
        self.type = type
        self.value = value


class MenuItem:

    def __init__(self, x=0, y=0):
        self.y = x
        self.x = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


class Button(EventDispatch, MenuItem):

    def __init__(self, text='Ok', event: UIEvent = None, x=0, y=0, col=(255, 255, 255)):
        super().__init__(x, y)
        self.text = text
        self.col = col
        self.event = event

    def draw(self, console: Console):
        console.print(self.x, self.y, '< ' + self.text + ' >', fg=self.col)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == tcod.event.K_RETURN:
            QueueFactory.get_queue().put(self.event)
            pass


class Input(EventDispatch, MenuItem):

    def __init__(self, label: str = '', default: str = '', col=(255, 255, 255)):
        self.col = col
        self.x = 0
        self.y = 0
        self.width = 0
        self.label = label
        self.text = default

    def get_max_input_length(self):
        return self.width - len(self.label) - 3

    def draw(self, console: Console):
        console.print(self.x, self.y, self.label, fg=self.col)
        console.print(self.x + len(self.label) + 2, self.y, ' ' * (self.width - len(self.label) - 3), bg=(20, 20, 20))
        console.print(self.x + len(self.label) + 2, self.y, self.text, fg=self.col, bg=(20, 20, 20))

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym in (tcod.event.K_BACKSPACE, 8):
            self.text = self.text[0:-1]

    def ev_textinput(self, event: TextInput) -> None:
        if self.get_max_input_length() > len(self.text):
            self.text += event.text


class Menu(EventDispatch):

    def __init__(self, width, height, selected_index=0, contents=[], title=''):
        self.width = width
        self.height = height
        self.console = Console(width, height)
        self.selected_index = selected_index
        self.contents = contents
        self.title = title
        self.x = 0
        self.y = 0
        self.hidden = True
        self.input_values = {}

    def draw(self, console):
        if not self.hidden:
            self.console.draw_frame(0, 0, self.width, self.height, title=self.title, )
            for index, elem in enumerate(self.contents, 0):
                if index == self.selected_index:
                    elem.col = (245, 218, 66)
                else:
                    elem.col = (255, 255, 255)
                elem.draw(self.console)
            self.console.blit(console, self.x, self.y)

    def ev_textinput(self, event: TextInput) -> None:
        self.contents[self.selected_index].dispatch(event)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == tcod.event.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.contents)
        elif event.sym == tcod.event.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.contents)
        else:
            self.contents[self.selected_index].dispatch(event)
