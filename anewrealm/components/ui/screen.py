"""Screen module relating to the screen that's drawn to.

The screen module contains all code related to setting up the screen for the
game and initializing tcod. Next to that it also provides a screen class
which can create windows and draw their contents
"""
from typing import List

import tcod
from tcod.console import Console

from anewrealm.components.ui.widgets.window import Window
from anewrealm.constants import *
from components.ui.util import align_center


def init_tcod() -> Console:
    """Initialize tcod library functionality and boilerplate.

    Initialize tcod by setting the custom font and creating a root console.
    For now and for easier animation, steadily lock the framerate at 30 fps.

    The height and width of the game are currently locked at a 16:9
    resolution. This may be altered later so all elements should be drawn
    relative to eachother and there should ideally be limited amount of
    hardcoded coordinates.

    :return: A tcod.Console upon which all drawing is done.
    """
    tcod.console_set_custom_font(FONT, FONT_OPTIONS_MASK)

    root_console = tcod.console_init_root(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        GAME_TITLE,
        renderer=tcod.RENDERER_SDL2,
        fullscreen=False,
        vsync=True,
        order='F')

    tcod.sys_set_fps(30)
    return root_console


class Screen:
    """Screen class that contains windows and draws them to a tcod Console.

    The screen class is the topmost class related to drawing to a tcod root
    Console. The root console can be seen as the main "game client" window.
    In it, all other sub windows and menu's/pop-ups are drawn.

    Screens can be provided with a title. The title, if provided, is drawn to
    the bordering frame of the screen. Not the actual window, but the border
    of the inner frame. Useful for fullscreen application.
    """

    def __init__(self, title=''):
        """Initialize the screen by creating a tcod root console.

        Initialize the Screen with an empty list of windows and a tcod root
        console.

        """
        tcod_root = init_tcod()
        self._root_console = tcod_root
        self._title = title
        self._windows = []

    @property
    def title(self) -> str:
        """Return the title of the screen.

        :return: The title of the window as a string.
        """
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        """Set the title of the window.

        :param title: A string that encapsulates the title of the screen
        well. Examples include but are not limited to: "Game", "Screen" or
        even "Display of various graphical objects."
        """
        self._title = title

    @property
    def root_console(self) -> Console:
        """Return the root console for this window.

        :return: The root tcod.Console upon which all graphical objects are
        drawn.
        """
        return self._root_console

    @root_console.setter
    def root_console(self, root_console: Console) -> None:
        """Set the root console for this window.

        :param root_console: A tcod.Console. This console will be used by
        this screen to draw all it's contents upon.
        """
        self._root_console = root_console

    @property
    def windows(self) -> List[Window]:
        """Return the list of windows the screen contains.

        :return: A list of window objects
        """
        return self._windows

    @windows.setter
    def windows(self, windows: List[Window]) -> None:
        """Set the list of window objects the screen should contain

        :param windows: A list of Windows the screen should draw.
        """
        self._windows = windows

    def add_window(self, window: Window):
        """Add a window to the screens contents.

        Add a window to the end of the list of contained windows by this
        screen. This means the window is drawn last upon the screen and a
        such overlays all other windows.

        :param window: A window object to add to the screen
        :return: None
        """
        self.windows.append(window)

    def add_centered_window(self, window: Window):
        """Add a window to the screen after center aligning it to the screen.

        :param window: A window object to add to the screen
        :return: None
        """
        window.x, window.y = align_center(self._root_console, (window.width,
                                                               window.height))
        self.add_window(window)

    def remove_window(self, window: Window):
        """Remove a window by it's reference.

        Remove a window from the screen by its reference.

        :param window: The window object to remove from the screens contents.
        :return: None
        """
        self.windows.remove(window)

    def draw(self) -> None:
        """Clears the screen and redraws it's contents.

        The draw method redraws the screen every frame. It does this by
        flushing the console, clearing it, and then drawing the root Screen
        frame (at max size).

        Then it loops over all the containing windows and draws them to the
        screen.

        :return:
        """
        tcod.console_flush()
        self.root_console.clear()
        self.root_console.draw_frame(0, 0, self.root_console.width,
                                     self.root_console.height,
                                     clear=False, bg_blend=tcod.BKGND_ADD,
                                     title=self.title
                                     )
        for window in self.windows:
            window.draw(self.root_console)

    def _run_draw_input_loop(self):
        """Run the draw and input loop.

        First draws all contents to the screen and after that handle all input.

        :return: None
        """
        while True:
            self.draw()
            # self.handle_input()

    def open(self):
        """Open the screen, start drawing and handling input.

        :return: None
        """
        self._run_draw_input_loop()
