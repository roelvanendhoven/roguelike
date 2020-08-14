import constants
from anewrealm.components.map import Map
from anewrealm.components.net import client
from anewrealm.components.ui.action_bar import ActionBar
from anewrealm.components.ui.chat_window import ChatWindow
from anewrealm.components.ui.main_menu import MainMenu
from anewrealm.components.ui.map_window import MapWindow
from anewrealm.components.ui.screen import Screen
from anewrealm.components.ui.status_window import StatusWindow
from components.ui.map_view import MapView


class GameClient:

    def __init__(self):
        self.game_screen = Screen()
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

    def _open_main_screen(self):
        map_window = MapWindow()
        self.game_screen.add_window(map_window)
        self.game_screen.add_window(StatusWindow())
        self.game_screen.add_window(ActionBar())

        chat_window = ChatWindow()
        self.game_screen.focused_window = chat_window
        self.game_screen.add_window(chat_window)

    def start(self):
        """Start the game and run the main loop.

        Open the Main menu of the game and start the

        :return: None
        """
        self._open_main_screen()
        self.game_screen.open()

    def connect(self, ip, port):
        self.game_network_client.add_event_listener(self.chat_view)
        self.game_network_client.connect(ip, port)
        self.game_network_client.send((constants.PLAYER_CONNECT,
                                       {
                                           'name':
                                               self.main_menu.player_name_input.text}))
        self.main_menu.close()


def main():
    GameClient().start()


if __name__ == "__main__":
    main()
