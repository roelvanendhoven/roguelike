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

    def __init__(self, root_console: tcod.console.Console):
        self.root_console = root_console
        self.main_menu = MainMenu(self)

    def _run_main_loop(self):
        while True:
            console = self.root_console

            tcod.console_flush()
            console.clear()

            console.draw_frame(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, clear=False, title='Logue Regacy')

            if self.main_menu.is_open():
                self.main_menu.menu_stack[-1].draw()

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
                    menu_stack.append()
                elif event.type == "CONNECT":
                    # TODO create better way to handle event attributes
                    print(event.value['ip'].text, event.value['port'].text)
                print(event)

    def start(self):
        self._run_main_loop()


class MainMenu:
    menu_stack = []
    _menu_open = False

    create_server_button = Button('Create Server', UIEvent('MENU_CREATE_SERVER'))
    join_server_button = Button('Join Server', UIEvent('MENU_CONNECT'))
    options_button = Button('Options')
    credits_button = Button('Credits'),
    quit_button = Button('Quit', UIEvent('QUIT'))

    connect_button =
    ip_input = Input('IP:  ', '127.0.0.1')
    port_input = Input('Port:', '7777')

    def open(self):
        self._menu_open = True

    def close(self):
        self._menu_open = False

    def is_open(self):
        return self._menu_open

    def __init__(self, game: Game):
        self._game = game

        self.main_menu = Menu.create(game.root_console, [
            self.create_server_button,
            self.join_server_button,
            self.options_button,
            self.credits_button,
            self.quit_button
        ], title='MENU')

        self.menu_stack.append(self.main_menu)

    def open_connect_menu(self):
        connect_menu = Menu.create(self._game.root_console, [
            self.ip_input,
            self.port_input,
            Button('Connect', UIEvent('CONNECT', {'ip': ip, 'port': port})),
            Button('Cancel', UIEvent('CANCEL'))
        ], title='Connect to Server')

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
