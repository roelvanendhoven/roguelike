import tcod
from tcod.console import Console
from tcod.event import EventDispatch, KeyDown, TextInput


def calculate_middle(console, dimensions: tuple) -> tuple:
    w, h = dimensions
    new_w = (console.width // 2) - w // 2
    new_h = (console.height // 2) - h // 2
    return new_w, new_h


class MenuItem:

    def __init__(self, x=0, y=0):
        self.y = x
        self.x = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


class Button(EventDispatch, MenuItem):

    def __init__(self, text='Ok', on_press: callable = None, x=0, y=0, col=(255, 255, 255)):
        super().__init__(x, y)
        self.text = text
        self.col = col
        self.on_press = on_press

    def draw(self, console: Console):
        console.print(self.x, self.y, '' + self.text + '', fg=self.col)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == tcod.event.K_RETURN:
            if self.on_press:
                self.on_press(self)
            pass


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
        console.print(self.x + len(self.label) + 2, self.y, ' ' * (self.width - len(self.label) - 3), bg=(20, 20, 20))
        console.print(self.x + len(self.label) + 2, self.y, self.text, fg=self.col, bg=(20, 20, 20))

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym in (tcod.event.K_BACKSPACE, 8):
            self.text = self.text[0:-1]
        elif event.sym == tcod.event.K_RETURN:
            if self.on_enter_pressed:
                self.on_enter_pressed()

    def ev_textinput(self, event: TextInput) -> None:
        if self.get_max_input_length() > len(self.text):
            self.text += event.text


class Textbox(EventDispatch):
    """Textbox displays a newline separated list of messages.

    Textbox is built to create scroll capability as soon as the list spills over the height of the widget.
    """

    messages = []

    def __init__(self, root_console: Console):
        self._console = root_console
        self.scroll_offset = 0

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self._console.height - 3:
            self.scroll_offset = len(self.messages) - (self._console.height - 3)

    def draw(self, root_console):
        self._console.draw_frame(0, 0, self._console.width, self._console.height)
        self._console.print_box(1, 1, self._console.width - 2, self._console.height - 3,
                                ''.join(self.messages[self.scroll_offset:]),
                                fg=(255, 244, 122))
        if len(self.messages) > self._console.height - 3:
            self._console.print(self._console.width - 2, 1, chr(tcod.CHAR_ARROW_N))
            self._console.print(self._console.width - 2, self._console.height - 3, chr(tcod.CHAR_ARROW_S))
        x, y = calculate_middle(root_console, (self._console.width, self._console.height))
        self._console.blit(root_console, x, y)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == tcod.event.K_DOWN:
            if self.scroll_offset < len(self.messages) - (self._console.height - 3):
                self.scroll_offset += 1
        if event.sym == tcod.event.K_UP:
            if self.scroll_offset > 0:
                self.scroll_offset -= 1


class Menu(EventDispatch):

    def __init__(self, root_console, width: int, height: int, selected_index=0, contents=[], title=''):
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

    @staticmethod
    def _create_layer_console(width, height):
        return Console(width, height)

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
    def create(cls, root_console, contents=[], width: int = 35, height: int = 10, title=''):
        menu = cls(root_console, width, height, contents=contents, title=title)
        menu.pack()
        menu.hidden = False
        return menu

    def draw(self):
        if not self.hidden:
            self.layer_console.draw_frame(0, 0, self.width, self.height, title=self.title, )
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
        if event.sym == tcod.event.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.contents)
        elif event.sym == tcod.event.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.contents)
        else:
            self.contents[self.selected_index].dispatch(event)
