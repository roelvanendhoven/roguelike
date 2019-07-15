import tcod
import tcod.console
import tcod.event

from components import game
from components.ui import Input, Button, create_menu

import components.client

# Constants
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 30

GAME_TITLE = "Net Test"

FONT = 'assets/font_12x12.png'
FONT_OPTIONS_MASK = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD


def init_tcod() -> tcod.console.Console:
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


def game_loop(console):

    menu = create_menu(console, [
        Button('Create Server'),
        Button('Connect'),
        Button('Credits'),
        Button('Quit')
    ], title='MENU')
    while True:

        tcod.console_flush()
        console.clear()

        console.draw_frame(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, clear=False, title='Logue Regacy')

        menu.draw(console)

        for event in tcod.event.get():
            if event.type == "QUIT":
                exit()
            if event.type == "KEYDOWN" or event.type == "TEXTINPUT":
                menu.dispatch(event)


def main():
    root_console = init_tcod()
    game_loop(root_console)
    print("Rogue like Jagger")


if __name__ == "__main__":
    # c = components.client.Client()
    # c.connect('127.0.0.1', 7777)
    # c.send({'say': 'Hello, world!'})
    main()
