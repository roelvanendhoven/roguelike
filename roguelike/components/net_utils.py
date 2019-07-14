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


def send(conn, message):
    jdata = json.dumps(message).encode('utf-8')
    conn.sendall(struct.pack("L", len(jdata)))
    conn.sendall(jdata)


def get_socket_address(sock):
    return str(sock.getpeername())


class MessageListener:
    # TODO make public
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

                self.listener.on_message_received(self.socket, data)
            # Maybe actually handle the exeption, we actually just want to break the loop
            except Exception:
                break

        self.listener.on_disconnect(self)
        self.socket.close()
