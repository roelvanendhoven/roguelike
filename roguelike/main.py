import tcod
import tcod.console
import tcod.event
import constants

from roguelike.components.ui.widgets.text_input import Input
from roguelike.components.ui.widgets.button import Button
from roguelike.components.ui.widgets.menu import Menu
from roguelike.components.ui.widgets.text_box import Textbox
from roguelike.components.ui.util import calculate_middle
from roguelike.components.net import client

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FONT, FONT_OPTIONS_MASK


class Game:

    def __init__(self, root_console: tcod.console.Console):
        self.root_console = root_console
        self.main_menu = MainMenu(self)
        self.chat_view = ChatView(self)
        self.main_menu.open()
        self.game_client: client.Client = client.Client()

    def _run_main_loop(self):
        while True:
            console = self.root_console

            tcod.console_flush()
            console.clear()

            if self.game_client.connected:
                self.chat_view.draw(console)

            if self.main_menu.is_open():
                self.main_menu.menu_stack[-1].draw()

            for event in tcod.event.get():
                if event.type == "QUIT":
                    if self.game_client.connected:
                        self.game_client.disconnect()
                    exit()
                if event.type == "KEYDOWN" or event.type == "TEXTINPUT":
                    if self.main_menu.is_open():
                        self.main_menu.menu_stack[-1].dispatch(event)
                    elif self.chat_view:
                        self.chat_view.message_input.dispatch(event)
                        self.chat_view.message_box.dispatch(event)

    def start(self):
        self._run_main_loop()

    def connect(self, ip, port):
        self.game_client.add_event_listener(self.chat_view)
        self.game_client.connect(ip, port)
        self.game_client.send((constants.PLAYER_CONNECT, {'name': self.main_menu.player_name_input.text}))
        self.main_menu.close()


class ChatView:
    console = tcod.console.Console(SCREEN_WIDTH - 4, SCREEN_HEIGHT // 3)
    messages = []
    message_input = Input('Chat:')

    def __init__(self, game: Game):
        self.game = game
        self.message_input.x = 1
        self.message_input.y = self.console.height - 2
        self.message_input.width = self.console.width - 2
        self.message_input.on_enter_pressed = self.send_message

        self.message_box = Textbox(self.console)

    def send_message(self):
        text = self.message_input.text
        self.message_input.text = ''
        self.game.game_client.send((constants.GLOBAL_CHAT, {'message': text}))

    def add_message(self, message):
        self.message_box.add_message(message + '\n')

    def on_connection_event(self, event):
        if event[0] == constants.GLOBAL_CHAT:
            self.add_message(event[1]['player'] + ': ' + event[1]['message'])

    def draw(self, root_console):
        self.console.draw_frame(0, 0, self.console.width, self.console.height, clear=False, bg_blend=tcod.BKGND_ADD)
        self.message_box.draw(root_console)
        self.message_input.draw(self.console)
        x, y = calculate_middle(root_console, (self.console.width, self.console.height))
        self.console.blit(root_console, 2, root_console.height - 3 - root_console.height // 3)


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

    player_name_input = Input('Player name:', 'Koldor')

    def open(self):
        self._menu_open = True

    def close(self):
        self._menu_open = False

    def is_open(self):
        return self._menu_open

    def __init__(self, game: Game):
        self._game = game

        self.join_server_button.on_press = self.open_connect_menu
        self.options_button.on_press = self.open_options_menu
        self.connect_button.on_press = self.connect
        self.create_server_button.on_press = self.create_server

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

    def open_options_menu(self, _: Button):
        menu = Menu.create(self._game.root_console, [
            self.player_name_input,
            Button('Go Back', self.cancel)
        ], title='Options', height=6)

        self.menu_stack.append(menu)

    def create_server(self, _: Button):
        # s = server.start_thread(server.Server)
        # TODO cleanup, port shouldnt be hardcoced
        # self._game.connect('localhost', 7777)
        pass

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
