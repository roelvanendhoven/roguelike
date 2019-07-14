""" Network Client module

This module is responsible for handling network events on the client sides

"""

import components.net_utils
import socket

from threading import Thread

logger = components.net_utils.get_logger()


class Client:

    def __init__(self):
        self.socket = socket.socket()
        self.connection_event_listeners = []

    def connect(self, host, port):
        self.socket.connect((host, port))
        self._run_message_listener()

    def add_event_listener(self, listener):
        self.connection_event_listeners.append(listener)

    def remove_event_listener(self, listener):
        self.connection_event_listeners.remove(listener)

    def send_connection_event(self, event=('', '')):
        for listener in self.connection_event_listeners:
            listener.on_connection_event(event)

    def disconnect(self):
        self.socket.close()

    def send(self, message):
        components.net_utils.send(self.socket, message)

    def on_message_received(self, sock, message):
        self.send_connection_event(('onmessage', message))
        logger.debug('client mss reveived')

    def on_disconnect(self):
        self.send_connection_event(('server_disconnect',))
        logger.debug('Server disconnected')

    def _run_message_listener(self):
        # logger.debug('client mss reveived')
        listener = components.net_utils.MessageListener(self.socket, self)
        t = Thread(target=listener.listen)
        t.start()
