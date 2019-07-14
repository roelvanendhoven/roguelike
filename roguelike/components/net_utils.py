import socket
import logging
import threading
import json
import struct


# TODO: Make sure to error handle the json decoding
# TODO: Make a parent class to handle common network functionality


def get_logger():
    logging.basicConfig(filename='server.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    return logging.getLogger('tcpserver')

logger = get_logger()

# define helper function for reading large data blobs
def read_blob(sock, size):
    logger.debug('entering readblob')
    buf = ""
    while len(buf) != size:
        ret = sock.recv(size - len(buf)).decode('utf-8')
        if not ret:
            raise Exception("Socket closed")
        buf += ret
        logger.debug('this is going to shit most likely, %s' % ret)
    logger.debug('exiting readblob, %s' % ret)
    return buf


# define helper functions for reading header data
def read_long(sock):
    logger.debug('enterting readlong')
    size = struct.calcsize("L")
    # TODO: Make sure to throw if empty packet comes through
    data = sock.recv(size)
    logger.debug(str(struct.unpack("L", data)))
    # returning first element because unpack returns a tuple
    return struct.unpack("L", data)[0]


class _MessageListener:
    socket = None

    def __init__(self, socket, listener):
        self.listener = listener
        self.socket = socket

    def listen(self):
        while True:
            try:
                logger.debug('(client): message incoming')
                datasize = read_long(self.socket)
                data = read_blob(self.socket, datasize)
                jdata = json.loads(data)
                logger.debug('[client]: %s' % str(jdata))

                self.listener.on_message_received(data)
            # Maybe actually handle the exeption, we actually just want to break the loop
            except Exception:
                raise

        self.listener.on_disconnect(socket)
        self.socket.close()


class ConnectionListenerThread:
    _maxclients = 10

    def __init__(self, server, socket):
        self.socket = socket
        self.server = server

    def run(self):
        logger.debug('(ConnectionListener) Started listening for connections')
        s = self.socket
        while True:
            conn, addr = s.accept()  # Establish connection with client.
            logger.debug('(ConnectionListener) Incoming connection from %s' % str(addr))
            client = ClientThread(conn, addr)
            client.network_event_listener = self.server
            t = threading.Thread(target=client.listen)
            # Daemonize thread so it shuts down when main thread exits
            # do not care to clean this up, at least ubuntu frees the ports up
            t.setDaemon(True)
            t.start()
        s.close()


class Server:
    connected_clients = []
    connection_event_listeners = []

    def __init__(self):
        s = socket.socket()  # Create a socket object
        host = '0.0.0.0'
        port = 7777  # Reserve a port for your service.

        s.bind((host, port))  # Bind to the port
        s.listen(5)  # Now wait for client connection.
        self._listen(s)

    def _listen(self, sock):
        connectionListener = ConnectionListenerThread(self, sock)
        t = threading.Thread(target=connectionListener.run)
        # Daemonize thread so it shuts down when main thread exits
        # do not care to clean this up, at least ubuntu frees the ports up
        t.setDaemon(True)
        t.start()

    def add_event_listener(self, listener):
        self.connection_event_listeners.append(listener)

    def remove_event_listener(self, listener):
        self.connection_event_listener.remove(listener)

    def send_to_all(self, message):
        for connection in self.connected_clients:
            logger.debug('(Server): Sending %s to all' % str(message))
            self.send(connection, message)

    def send_connection_event(self, event=('', '')):
        for listener in self.connection_event_listeners:
            listener.on_connection_event(event)

    def send(self, conn, message):
        jdata = json.dumps(message).encode('utf-8')
        conn.sendall(struct.pack("L", len(jdata)))
        conn.sendall(jdata)

    def on_new_client(self, conn, addr):
        self.connected_clients.append(conn)
        self.send_connection_event(('connect', str(addr)))
        logger.info('New connection for %s' % str(addr))

    def on_message_received(self, conn, addr, message):
        self.send_to_all('%s: %s' % (str(addr[0]), message))
        self.send_connection_event(('onmessage', (str(addr), message)))
        logger.info("%s: %s" % (str(addr), message))

    def on_client_disconnect(self, conn, addr):
        self.connected_clients.remove(conn)
        self.send_connection_event(('disconnect', str(addr)))
        logger.info('Client %s disconnected' % str(addr))


class ClientThread:

    def __init__(self, conn, addr):
        logger.debug('(ClientThread) created a client for %s' % str(addr))
        self.network_event_listener = None
        self.conn = conn
        self.addr = addr

    def listen(self):
        self.network_event_listener.on_new_client(self.conn, self.addr)
        while True:
            try:
                logger.debug('attempting to read some data')
                datasize = read_long(self.conn)
                if datasize == '':
                    break
                data = read_blob(self.conn, datasize)
                jdata = json.loads(data)

                self.network_event_listener.on_message_received(self.conn, self.addr, data)
            # Maybe actually handle the exeption, we actually just want to break the loop
            except Exception:
                break

        self.network_event_listener.on_client_disconnect(self.conn, self.addr)
        self.conn.close()
        logger.debug('(ClientThread) Connection closed: %s' % str(self.addr))


if __name__ == '__main__':
    Server()
