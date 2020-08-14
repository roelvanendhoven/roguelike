from tcod import Console

from anewrealm.components.ui.util import Drawable
from anewrealm.components.ui.widgets.window import Window
from anewrealm.constants import ACTION_BAR_HEIGHT, ACTION_BAR_WIDTH, \
    MAPWINDOW_HEIGHT, DEFAULT_UI_BACKGROUND, DEFAULT_UI_FOREGROUND


class EmptyBar(Drawable):
    """Placeholder for empty bar"""

    def draw(self, console: Console) -> None:
        console.print(self.x, self.y, 'A' * self.width, fg=self.fg, bg=self.bg)


class ActionBar(Window):
    """The Window that the Action Bar is drawn in.

    This window is responsible for displaying the action bar. The action bar
    displays the available actions to the player. Things like move, attack,
    cast, inspect, etc.

    """

    def __init__(self):
        super().__init__(
            y=MAPWINDOW_HEIGHT,
            width=ACTION_BAR_WIDTH,
            height=ACTION_BAR_HEIGHT,
        )

        bar = EmptyBar()
        bar.fg = DEFAULT_UI_BACKGROUND
        bar.bg = DEFAULT_UI_FOREGROUND
        bar.width = ACTION_BAR_WIDTH

        self.contents = [
            bar,
        ]

