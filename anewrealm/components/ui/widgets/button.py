from tcod.event import EventDispatch, KeyDown, K_RETURN
from tcod.console import Console
from anewrealm.components.ui.widgets.menu import MenuItem


class Button(EventDispatch, MenuItem):

    def __init__(self, text='Ok', on_press: callable = None, x=0, y=0,
                 col=(255, 255, 255)):
        super().__init__(x, y)
        self.text = text
        self.col = col
        self.on_press = on_press

    def draw(self, console: Console):
        console.print(self.x, self.y, '' + self.text + '', fg=self.col)

    def ev_keydown(self, event: KeyDown) -> None:
        if event.sym == K_RETURN:
            if self.on_press:
                self.on_press(self)
