import tcod
import tcod.console
import tcod.event

import constants
from anewrealm.components.net import client
from anewrealm.components.ui.main_menu import MainMenu
from anewrealm.components.ui.screen import Screen
from anewrealm.components.ui.util import align_center
from anewrealm.components.ui.widgets.text_box import Textbox
from anewrealm.components.ui.widgets.text_input import Input
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameClient:

    def __init__(self):
        self.game_screen = Screen()
        self.chat_view = ChatView(self)
        self.game_network_client: client.Client = client.Client()

            # if self.game_client.connected:
            #     self.chat_view.draw(console)
            #
            # if self.main_menu.is_open():
            #     self.main_menu.menu_stack[-1].draw()
            #


    def _open_main_menu(self):
        """Open the game main menu.

        :return: None
        """
        self.game_screen.add_centered_window(MainMenu(self))

    def start(self):
        """Start the game and run the main loop.

        Open the Main menu of the game and start the

        :return: None
        """
        self._open_main_menu()
        self.game_screen.open()

    def connect(self, ip, port):
        self.game_network_client.add_event_listener(self.chat_view)
        self.game_network_client.connect(ip, port)
        self.game_network_client.send((constants.PLAYER_CONNECT,
                                       {
                                   'name':
                                       self.main_menu.player_name_input.text}))
        self.main_menu.close()


class ChatView:
    console = tcod.console.Console(SCREEN_WIDTH - 4, SCREEN_HEIGHT // 3)
    messages = []
    message_input = Input('Chat:')

    def __init__(self, game: GameClient):
        self.game = game
        self.message_input.x = 1
        self.message_input.y = self.console.height - 2
        self.message_input.width = self.console.width - 2
        self.message_input.on_enter_pressed = self.send_message

        self.message_box = Textbox(self.console)

    def send_message(self):
        text = self.message_input.text
        self.message_input.text = ''
        self.game.game_network_client.send((constants.GLOBAL_CHAT, {'message': text}))

    def add_message(self, message):
        self.message_box.add_message(message + '\n')

    def on_connection_event(self, event):
        if event[0] == constants.GLOBAL_CHAT:
            self.add_message(event[1]['player'] + ': ' + event[1]['message'])

    def draw(self, root_console):
        self.console.draw_frame(0, 0, self.console.width, self.console.height,
                                clear=False, bg_blend=tcod.BKGND_ADD)
        self.message_box.draw(root_console)
        self.message_input.draw(self.console)
        x, y = align_center(root_console,
                            (self.console.width, self.console.height))
        self.console.blit(root_console, 2,
                          root_console.height - 3 - root_console.height // 3)


def main():
    GameClient().start()


if __name__ == "__main__":
    main()
