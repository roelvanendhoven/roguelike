import tcod
from tcod.console import Console
from tcod.event import EventDispatch, KeyDown, TextInput

from typing import List, Union


class Component:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def _draw(self, console: Console):
        pass


class Container(Component, EventDispatch):
    contents: List[Component] = []
    focused_component: Union[EventDispatch, Component] = None

    def _draw(self, console: Console) -> None:
        for component in self.contents:
            component._draw(console)

    def ev_keydown(self, event: KeyDown) -> None:
        if self.focused_component is not None:
            self.focused_component.dispatch(event)

    def ev_textinput(self, event: TextInput) -> None:
        if self.focused_component is not None:
            self.focused_component.dispatch(event)

    def add_widget(self, component: Component):
        self.contents.append(component)
        if self.focused_component is None:
            self.focused_component = component

    def remove_widget(self, component: Component):
        if component in self.contents:
            if component == self.focused_component:
                self.focused_component = None
            self.contents.remove(component)

class Dialog(Container):



class Screen(Container):

    def __init__(self, x, y, width, height, console: Console, title=''):
        super().__init__(x, y, width, height)
        self.console = console
        self.title = title

    def draw(self) -> None:
        tcod.console_flush()
        self.console.clear()
        super()._draw(self.console)
        self.console.draw_frame(self.x, self.y, self.width, self.height, clear=False, title=self.title)

    def show_dialog(self,entries):
        dialog = Dialog()




class Button(Component, EventDispatch):

    def __init__(self, x, y, text='Ok', col=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.col = col

    def draw(self, console: Console):
        console.print(self.x, self.y, '< ' + self.text + ' >', fg=self.col)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == tcod.event.K_KP_ENTER:
            pass





class Input(Component, EventDispatch):

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
        console.print(self.x + len(self.label) + 2, self.y, self.text, fg=col, bg=(20, 20, 20))

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym in (tcod.event.K_BACKSPACE, 8):
            self.text = self.text[0:-1]

    def ev_textinput(self, event: TextInput) -> None:
        self.text += event.text


class InputBox(EventDispatch):

    def __init__(self, width, height, selected_index=0, contents=[], title=''):
        self.width = width
        self.height = height
        self.console = Console(width, height)
        self.selected_index = selected_index
        self.contents = contents
        self.title = title

    def draw(self, console, x, y):
        self.console.draw_frame(0, 0, self.width, self.height, title=self.title, )
        for index, elem in enumerate(self.contents, 0):
            if index == self.selected_index:
                elem.draw(self.console, col=(245, 218, 66))
            else:
                elem.draw(self.console)

        self.console.blit(console, x, y)

    def ev_textinput(self, event: TextInput) -> None:
        self.contents[self.selected_index].dispatch(event)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == tcod.event.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.contents)
        elif event.sym == tcod.event.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.contents)
        else:
            self.contents[self.selected_index].dispatch(event)
