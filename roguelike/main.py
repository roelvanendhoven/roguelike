import tcod
import tcod.console
import tcod.event

from components import game
from components.ui import Input, Button, create_menu, init_queue, get_ui_event

import components.client

# Constants
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 30

GAME_TITLE = "Net Test"

FONT = 'assets/font_12x12.png'
FONT_OPTIONS_MASK = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD


def init_tcod() -> tcod.console.Console:
    tcod.console_set_custom_font(FONT, FONT_OPTIONS_MASK)
    init_queue()

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

    menu_stack = []

    menu = create_menu(console, [
        Button('Create Server'),
        Input('Name:'),
        Input('Game:'),
        Input('Lame:'),
        Button('Connect', 'MENU_CONNECT'),
        Button('Credits'),
        Button('Quit', 'QUIT')
    ], title='MENU')

    menu_stack.append(menu)

    while True:

        tcod.console_flush()
        console.clear()

        console.draw_frame(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, clear=False, title='Logue Regacy')

        menu_stack[-1].draw(console)

        for event in tcod.event.get():
            if event.type == "QUIT":
                exit()
            if event.type == "KEYDOWN" or event.type == "TEXTINPUT":
                menu_stack[-1].dispatch(event)

        event = get_ui_event()
        if event:
            if event == 'QUIT':
                raise SystemExit()
            elif event == 'CANCEL':
                menu_stack.pop()
            elif event == 'MENU_CONNECT':
                menu_stack.append(create_menu(console, [
                    Input('IP:  ', '127.0.0.1'),
                    Input('Port:', '7777'),
                    Button('Connect','CONNECT'),
                    Button('Cancel','CANCEL')
                ], title='Connect to Server'))

            print(event)


def main():
    root_console = init_tcod()
    game_loop(root_console)
    print("Rogue like Jagger")


if __name__ == "__main__":
    # c = components.client.Client()
    # c.connect('127.0.0.1', 7777)
    # c.send({'say': 'Hello, world!'})
    main()
