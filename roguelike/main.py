import tcod
import tcod.console
import tcod.event

from components.ui import Input, Button, Menu, get_ui_event, UIEvent

import components.client

# Constants
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 30

GAME_TITLE = "Net Test"

FONT = 'assets/font_12x12.png'
FONT_OPTIONS_MASK = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD


class Game:
    menu_stack = []

    def __init__(self, root_console: tcod.console.Console):
        self.root_console = root_console
        self.main_menu = MainMenu(self)

    def _run_main_loop(self):
        while True:
            console = self.root_console
            menu_stack = self.menu_stack

            tcod.console_flush()
            console.clear()

            console.draw_frame(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, clear=False, title='Logue Regacy')

            menu_stack[-1].draw()

            for event in tcod.event.get():
                if event.type == "QUIT":
                    exit()
                if event.type == "KEYDOWN" or event.type == "TEXTINPUT":
                    menu_stack[-1].dispatch(event)

            event = get_ui_event()
            if event:
                if event.type == 'QUIT':
                    raise SystemExit()
                elif event.type == 'CANCEL':
                    menu_stack.pop()
                elif event.type == 'MENU_CONNECT':
                    ip = Input('IP:  ', '127.0.0.1')
                    port = Input('Port:', '7777')
                    menu_stack.append(Menu.create(console, [
                        ip,
                        port,
                        Button('Connect', UIEvent('CONNECT', {'ip': ip, 'port': port})),
                        Button('Cancel', UIEvent('CANCEL'))
                    ], title='Connect to Server'))
                elif event.type == "CONNECT":
                    # TODO create better way to handle event attributes
                    print(event.value['ip'].text, event.value['port'].text)
                print(event)

    def start(self):
        self._run_main_loop()


class MainMenu:
    menu_stack = []

    def __init__(self, game: Game):
        self.main_menu = Menu.create(game.root_console, [
            Button('Create Server', UIEvent('MENU_CREATE_SERVER')),
            Input('Name:'),
            Input('Game:'),
            Input('Lame:'),
            Button('Connect', UIEvent('MENU_CONNECT')),
            Button('Credits'),
            Button('Quit', UIEvent('QUIT'))
        ], title='MENU')

        self.menu_stack.append(self.main_menu)


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


def main():
    root_console = init_tcod()
    Game(root_console).start()


if __name__ == "__main__":
    main()
