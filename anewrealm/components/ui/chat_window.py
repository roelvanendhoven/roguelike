from typing import Optional, T, Any

from tcod.event import EventDispatch, KeyDown, TextInput

from anewrealm.components.ui.widgets.window import BorderedWindow
from anewrealm.constants import MAPWINDOW_HEIGHT, \
    CHATWINDOW_WIDTH, CHATWINDOW_HEIGHT, CHATWINDOW_BACKGROUND_COLOR
from anewrealm.components.ui.widgets.text_box import Textbox
from anewrealm.components.ui.widgets.text_input import Input


class ChatWindow(BorderedWindow, EventDispatch):
    """The Window that the map view is drawn in.

    This window is responsible for displaying the map and handling map
    related key events such as movement indication and information popups.

    """

    def __init__(self):
        super().__init__(y=MAPWINDOW_HEIGHT + 1,
                         width=CHATWINDOW_WIDTH,
                         height=CHATWINDOW_HEIGHT)

        self.mode = 'COMMAND'

        self.message_display = Textbox(x=1, y=1, height=self.height,
                                       width=self.width)

        self._setup_input()

        self.contents = [
            self.message_display,
            self.message_input
        ]

    def _setup_input(self):
        self.message_input = Input(f'[{self.mode}] ', x=1, y=self.height - 2,
                                   width=CHATWINDOW_WIDTH)
        self.message_input.bg = CHATWINDOW_BACKGROUND_COLOR
        self.message_input.on_enter_pressed = self.send_message

    def send_message(self):
        text = self.message_input.text
        self.message_input.text = ''
        self.add_message(text)

    def add_message(self, message):
        self.message_display.add_message(message + '\n')

    def ev_keydown(self, event: KeyDown) -> Optional[T]:
        self.message_input.dispatch(event)

    def ev_textinput(self, event: TextInput) -> Optional[T]:
        self.message_input.dispatch(event)

    # def send_message(self):
    #     text = self.message_input.text
    #     self.message_input.text = ''
    #     self.game.game_network_client.send(
    #         (constants.GLOBAL_CHAT, {'message': text}))
