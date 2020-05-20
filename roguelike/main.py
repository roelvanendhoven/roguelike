import tcod
import tcod.console
import tcod.event
import constants
from components.ui.main_menu import MainMenu
from components.ui.screen import Screen

from roguelike.components.ui.widgets.text_input import Input
from roguelike.components.ui.widgets.text_box import Textbox
from roguelike.components.ui.util import align_center
from roguelike.components.net import client

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameClient:

    def __init__(self):
        self.screen = Screen()
        self.main_menu = MainMenu(self)
        self.chat_view = ChatView(self)
        self.main_menu.open()
        self.game_client: client.Client = client.Client()

    def _run_main_loop(self):
        while True:
            self.screen.draw()

            # if self.game_client.connected:
            #     self.chat_view.draw(console)
            #
            # if self.main_menu.is_open():
            #     self.main_menu.menu_stack[-1].draw()
            #
            # for event in tcod.event.get():
            #     if event.type == "QUIT":
            #         if self.game_client.connected:
            #             self.game_client.disconnect()
            #         exit()
            #     if event.type == "KEYDOWN" or event.type == "TEXTINPUT":
            #         if self.main_menu.is_open():
            #             self.main_menu.menu_stack[-1].dispatch(event)
            #         elif self.chat_view:
            #             self.chat_view.message_input.dispatch(event)
            #             self.chat_view.message_box.dispatch(event)

    def start(self):
        self._run_main_loop()

    def connect(self, ip, port):
        self.game_client.add_event_listener(self.chat_view)
        self.game_client.connect(ip, port)
        self.game_client.send((constants.PLAYER_CONNECT,
                               {'name': self.main_menu.player_name_input.text}))
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
        self.game.game_client.send((constants.GLOBAL_CHAT, {'message': text}))

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
