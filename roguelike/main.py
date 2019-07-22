import tcod
import tcod.console
import tcod.event
import constants

from components.ui import Input, Button, Menu, calculate_middle
from components import client

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
        self.chat_view = ChatView(self)
        self.main_menu.open()
        self.game_client: client.Client = None

    def _run_main_loop(self):
        while True:
            console = self.root_console

            tcod.console_flush()
            console.clear()

            console.draw_frame(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, clear=False, title='Logue Regacy')

            if self.game_client:
                self.chat_view.draw(console)

            if self.main_menu.is_open():
                self.main_menu.menu_stack[-1].draw()

            for event in tcod.event.get():
                if event.type == "QUIT":
                    exit()
                if event.type == "KEYDOWN" or event.type == "TEXTINPUT":
                    if self.main_menu.is_open():
                        self.main_menu.menu_stack[-1].dispatch(event)
                    elif self.chat_view:
                        self.chat_view.message_input.dispatch(event)

    def start(self):
        self._run_main_loop()

    def connect(self, ip, port):
        self.game_client = client.Client()
        self.game_client.add_event_listener(self.chat_view)
        self.game_client.connect(ip, port)
        self.main_menu.close()


class ChatView:
    console = tcod.console.Console(SCREEN_WIDTH - 4, SCREEN_HEIGHT - 6)
    messages = []
    message_input = Input('Chat:')

    def __init__(self, game: Game):
        self.game = game
        self.message_input.x = 1
        self.message_input.y = self.console.height - 2
        self.message_input.width = self.console.width - 2
        self.message_input.on_enter_pressed = self.send_message

    def send_message(self):
        text = self.message_input.text
        self.message_input.text = ''
        self.add_message(text)
        self.game.game_client.send((constants.GLOBAL_CHAT, {'message': text}))

    def add_message(self, message):
        self.messages.append(message + '\n')

    def on_connection_event(self, event):
        self.add_message(event[1])

    def draw(self, root_console):
        self.console.draw_frame(0, 0, self.console.width, self.console.height)
        self.console.print_box(1, 1, self.console.width - 2, self.console.height - 3, ''.join(self.messages),
                               fg=(255, 244, 122))
        self.message_input.draw(self.console)
        x, y = calculate_middle(root_console, (self.console.width, self.console.height))
        self.console.blit(root_console, x, y)


class MainMenu:
    menu_stack = []
    _menu_open = False

    create_server_button = Button('Create Server')
    join_server_button = Button('Join Server')
    options_button = Button('Options')
    credits_button = Button('Credits')
    quit_button = Button('Quit', lambda _: exit())

    connect_button = Button('Connect')
    ip_input = Input('IP:  ', '86.83.187.168')
    port_input = Input('Port:', '7777')

    def open(self):
        self._menu_open = True

    def close(self):
        self._menu_open = False

    def is_open(self):
        return self._menu_open

    def __init__(self, game: Game):
        self._game = game

        self.join_server_button.on_press = self.open_connect_menu
        self.connect_button.on_press = self.connect

        self.main_menu = Menu.create(game.root_console, [
            self.create_server_button,
            self.join_server_button,
            self.options_button,
            self.credits_button,
            self.quit_button
        ], title='MENU')

        self.menu_stack.append(self.main_menu)

    def cancel(self, _: Button):
        self.menu_stack.pop()

    def open_connect_menu(self, _: Button):
        connect_menu = Menu.create(self._game.root_console, [
            self.ip_input,
            self.port_input,
            self.connect_button,
            Button('Cancel', self.cancel)
        ], title='Connect to Server')

        self.menu_stack.append(connect_menu)

    def connect(self, _: Button):
        ip = self.ip_input.text
        port = self.port_input.text

        port = int(port)
        if not 0 < port < 65535:
            print('Error port gay')
            return

        # TODO sanitize ip

        self._game.connect(ip, port)


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
