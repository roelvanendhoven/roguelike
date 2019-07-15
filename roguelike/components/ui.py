import tcod
from tcod.console import Console
from tcod.event import EventDispatch, KeyDown, TextInput

from typing import List, Union


def calculate_middle(console, dimensions: tuple) -> tuple:
    w, h = dimensions
    new_w = (console.width // 2) - w // 2
    new_h = (console.height // 2) - h // 2
    return new_w, new_h


def create_menu(console, contents, title=''):
    menu = Menu(30, 15, contents=contents, title=title)
    x, y = calculate_middle(console, (menu.width, menu.height))
    menu.x = x
    menu.y = y
    for i, element in enumerate(contents, 1):
        element.x = 2
        element.y = (i * 2)
        element.width = menu.width - 3
    menu.hidden = False
    return menu


class Component:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Button(EventDispatch):

    def __init__(self, text='Ok', col=(255, 255, 255)):
        self.text = text
        self.col = col
        self.x = 0
        self.y = 0

    def draw(self, console: Console):
        console.print(self.x, self.y, '< ' + self.text + ' >', fg=self.col)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == tcod.event.K_KP_ENTER:
            pass


class Input(EventDispatch):

    def __init__(self, label: str = None, default: str = None, col=(255, 255, 255)):
        self.col = col
        self.x = 0
        self.y = 0
        self.width = 0
        self.label = label
        self.text = default

    def get_max_input_length(self):
        return self.width - len(self.label) - 2

    def draw(self, console: Console, col=(255, 255, 255)):
        console.print(self.x, self.y, self.label, fg=col)
        console.print(self.x + len(self.label) + 2, self.y, ' ' * (self.width - len(self.label) - 2), bg=(20, 20, 20))
        console.print(self.x + len(self.label) + 2, self.y, self.text, fg=col, bg=(20, 20, 20))

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym in (tcod.event.K_BACKSPACE, 8):
            self.text = self.text[0:-1]

    def ev_textinput(self, event: TextInput) -> None:
        if self.get_max_input_length() < len(self.text):
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
