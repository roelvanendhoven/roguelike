"""This module contains all logic related to the main menu.

The main_menu module contains all code related to drawing and handling the
main menu interface.

"""
from __future__ import annotations

import typing

from components.ui.widgets.window import Window
from components.ui.widgets.button import Button
from components.ui.widgets.menu import Menu
from components.ui.widgets.text_input import Input

if typing.TYPE_CHECKING:
    # To prevent circular imports, type checking imports should be done
    # inside a block like this. At runtime, TYPE_CHECKING won't evaluate to
    # true. This is an unfortunate hack because I wasn't aware of this
    # dramatic implementation.
    from anewrealm.main import GameClient


class MainMenu(Window):
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

    def __init__(self, game: GameClient):
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
