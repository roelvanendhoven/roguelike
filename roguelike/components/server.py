import socket
import threading
import constants
from components.net_utils import MessageListener, get_socket_address
from managers.sessions import *

"""Server module containing server logic
"""


def start_thread(func):
    t = threading.Thread(target=func)
    t.setDaemon(True)
    t.start()


class Server:
    connected_listeners = []

    def __init__(self):
        print('start server')
        self.session_manager = SessionManager()
        self.server_sock = s = socket.socket()  # Create a socket object
        host = '0.0.0.0'
        port = 7777  # Reserve a port for your service.

        s.bind((host, port))  # Bind to the port
        s.listen(5)

        start_thread(self.listen_for_connections())

    def listen_for_connections(self):
        print('start listening for connections')
        while True:
            sock, addr = self.server_sock.accept()
            self.on_connect(sock)
        self.server_sock.close()

    def on_connect(self, sock):
        listener = MessageListener(sock, self)
        self.connected_listeners.append(listener)
        print('connect: ', get_socket_address(sock))
        self.send_to_all('connect: %s' % get_socket_address(sock))
        start_thread(listener.listen)

    def on_disconnect(self, listener):
        sessions = self.session_manager.get_sessions_for_player(listener.socket)
        if sessions is not None:
            for s in sessions:
                s.leave(listener.socket)

        self.connected_listeners.remove(listener)
        self.send_to_all('disconnect: %s' % get_socket_address(listener.socket))

    def on_message_received(self, sock, event):
        if event[0] == constants.GLOBAL_CHAT:
            self.send_to_all((constants.GLOBAL_CHAT, event[1]))
        elif event[0] == constants.LOBBIES:
            self.session_manager.on_lobby_event(sock, event[1])
        elif event[0] == constants.PLAYER_INTENT:
            self.session_manager.on_player_intent(sock, event[1])

    def send_to_all(self, message):
        for l in self.connected_listeners:
            print('send message ', message, ' to ', get_socket_address(l.socket))
            send(l.socket, message)


if __name__ == '__main__':
    Server()
