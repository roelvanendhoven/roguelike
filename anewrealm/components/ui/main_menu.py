"""This module contains all logic related to the main menu.

The main_menu module contains all code related to drawing and handling the
main menu interface.

"""
from __future__ import annotations

import typing

from anewrealm.constants import DEFAULT_MENU_HEIGHT, DEFAULT_MENU_WIDTH
from anewrealm.components.ui.widgets.window import Window, BorderedWindow
from anewrealm.components.ui.widgets.button import Button
from anewrealm.components.ui.widgets.menu_mixin import MenuMixin
from anewrealm.components.ui.widgets.text_input import Input

if typing.TYPE_CHECKING:
    # To prevent circular imports, type checking imports should be done
    # inside a block like this. At runtime, TYPE_CHECKING won't evaluate to
    # true. This is an unfortunate hack because I wasn't aware of this
    # dramatic implementation.
    from anewrealm.main import GameClient


class MainMenu(BorderedWindow, MenuMixin):
    # TODO: This is a free for all. Nothing makes sense here.

    create_server_button = Button('Create Server')
    join_server_button = Button('Join Server')
    options_button = Button('Options')
    credits_button = Button('Credits')
    quit_button = Button('Quit', lambda _: exit())

    player_name_input = Input('Player name:', 'Koldor')

    def __init__(self, game: GameClient):
        contents = [
            self.create_server_button,
            self.join_server_button,
            self.options_button,
            self.credits_button,
            self.quit_button
        ]
        super().__init__(DEFAULT_MENU_WIDTH, DEFAULT_MENU_HEIGHT, contents,
                         title='MENU')
        self.selected_index = 0
        self._game = game
        self.join_server_button.on_press = self.open_connect_menu
        self.options_button.on_press = self.open_options_menu
        self.create_server_button.on_press = self.create_server



    def open_connect_menu(self, _: Button):
        connect_menu = MenuMixin.create(self._game.root_console, [
            self.ip_input,
            self.port_input,
            self.connect_button,
            Button('Cancel', self.cancel)
        ], title='Connect to Server')

        self.menu_stack.append(connect_menu)

    def open_options_menu(self, _: Button):
        menu = MenuMixin.create(self._game.root_console, [
            self.player_name_input,
            Button('Go Back', self.cancel)
        ], title='Options', height=6)

    def create_server(self, _: Button):
        # s = server.start_thread(server.Server)
        # TODO cleanup, port shouldnt be hardcoced
        # self._game.connect('localhost', 7777)
        pass


class ConnectMenu(Window):
    """Menu to connect to a server.

    ConnectMenu contains an IP and port input. It also handles the
    validation of the IP and port.
    """
    connect_button = Button('Connect')
    ip_input = Input('IP:  ', '86.83.187.168')
    port_input = Input('Port:', '7777')

    def __init__(self, game_client: GameClient):
        self._game_client = game_client
        self.connect_button.on_press = self.connect_pressed

    def connect_pressed(self, _: Button):
        ip = self.ip_input.text
        port = self.port_input.text

        port = int(port)
        if not 0 < port < 65535:
            print('Error port gay')
            return

        # TODO sanitize ip

        self._game_client.connect(ip, port)
