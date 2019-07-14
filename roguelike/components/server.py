import socket
import threading
from components.net_utils import MessageListener, send, get_socket_address

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
        start_thread(listener.listen())
        print('connect: ', get_socket_address(sock))
        self.send_to_all('connect: %s' % get_socket_address(sock))

    def on_disconnect(self, listener):
        self.connected_listeners.remove(listener)
        print('disconnect: ', get_socket_address(listener.socket))
        self.send_to_all('disconnect: %s' % get_socket_address(listener.socket))

    def on_message_received(self, sock, message):
        print('received message: ', (get_socket_address(sock), message))
        self.send_to_all('%s: %s' % (get_socket_address(sock), message))

    def send_to_all(self, message):
        for l in self.connected_listeners:
            print('send message ', message , ' to ' , get_socket_address(l.socket))
            send(l.socket, message)


if __name__ == '__main__':
    Server()
