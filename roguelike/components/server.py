import socket
import threading

import constants
from components.net_utils import send, TCPMessageListener
from managers.sessions import *

"""Server module containing server logic
"""


def start_thread(func):
    t = threading.Thread(target=func)
    t.setDaemon(True)
    t.start()


class Player:
    name = "???"

    def __init__(self, listener):
        self.listener = listener
        self.is_ready = False

    def set_name(self, name):
        self.name = name

    def send(self, msg):
        send(self.listener.socket, msg)


class Server:
    players = []

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
        listener = TCPMessageListener(sock)
        self.players.append(Player(listener))
        start_thread(listener.listen_for_events)

    def on_disconnect(self, listener):
        sessions = self.session_manager.get_sessions_for_player(
            listener.socket)
        if sessions is not None:
            for s in sessions:
                s.leave(listener.socket)

        player = self.get_player_for_socket(listener.socket)
        self.players.remove(player)
        self.send_to_all(player, "disconnected")

    def on_message_received(self, sock, event):
        player = self.get_player_for_socket(sock)
        if player is None:
            print("player not found")

        if event[0] == constants.GLOBAL_CHAT:
            self.send_to_all(player, event[1]['message'])
        elif event[0] == constants.PLAYER_CONNECT:
            player.set_name(event[1]['name'])
            self.send_to_all(player, "connected")
        elif event[0] == constants.LOBBIES:
            self.session_manager.on_lobby_event(player, event[1])
        elif event[0] == constants.PLAYER_INTENT:
            self.session_manager.on_player_intent(player, event[1])

    def get_player_for_socket(self, sock) -> Player:
        for p in self.players:
            if p.listener.socket == sock:
                return p
        return None

    def send_to_all(self, player, message):
        for p in self.players:
            send(p.listener.socket, (constants.GLOBAL_CHAT,
                                     {'message': message,
                                      'player': player.name}))


if __name__ == '__main__':
    Server()
