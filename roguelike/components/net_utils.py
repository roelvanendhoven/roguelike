import json
import logging
import struct
from socket import socket


# TODO: Make sure to error handle the json decoding
# TODO: Make a parent class to handle common network functionality


def get_logger():
    logging.basicConfig(filename='server.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    return logging.getLogger('tcpserver')


logger = get_logger()





class Event:
    """Models an event as sent and received by the network communication.
    """

    def __init__(self, target: str, calls: str, parameters: dict):
        self.target = target
        self.calls = calls
        self.parameters = parameters


class EventDelegator:
    """Takes an event and delegates its processing to the subscribed listener.
    """

    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Set up empty listener dictionary"""
        self.listeners = {}

    def add_listener(self, name: str, listener):
        self.listeners[name] = listener

    def remove_listener(self, name: str):
        self.listeners.pop(name)

    def delegate(self, event: Event):
        target = self.listeners.get(event.target, None)
        if target is None:
            raise NotImplementedError(f'{event.target} is not a registered '
                                      f'listener')
        try:
            func = getattr(target, event.calls)
            func(**event.parameters)
        except AttributeError as e:
            raise NotImplementedError(f'{event.calls} is not implemented on '
                                      f'the listener class') from e


class EventSerializer:
    """Serialize network events to command objects.
    """

    def _validate_message(self, message: tuple) -> bool:
        """
        :param: message Message as
        :return: True if event passes validation
        """
        pass

    def deserialize_event(self, event: Event):
        return (event.target,
                event.calls,
                event.parameters)

    def serialize_event(self, message: tuple):
        return Event(message[0], message[1], message[2])
        pass


class TCPMessageListener:
    """Message listener class for network level packet handling.

    The MessageListener class handles tcp level inbound packet communication
    by reading bytes from a socket and relaying the decoded messages upwards
    to higher level event handlers. It's also responsible for handling all
    errors related to a listening socket.
    """

    def __init__(self, sock: socket):
        """Initialize class by setting the socket and a listener

        :param sock: a socket
        """
        self.delegator = EventDelegator.get()
        self.serializer = EventSerializer()
        self.socket = sock

    def _read_blob(self, size) -> str:
        """Read data according to given size and return it.

        This method creates a buffer and reads size bytes from the objects
        socket connection. It then decodes the contents in utf-8 and returns
        the contents of the buffer.

        :param size: The size to read in bytes.
        :return: the contents of the buffer as utf-8 decoded string.
        """
        buf = ""
        while len(buf) != size:
            ret = self.socket.recv(size - len(buf)).decode('utf-8')
            if not ret:
                raise Exception("Socket closed")
            buf += ret
        return buf

    def _read_long(self) -> int:
        """Reads initial 'header' packet containing payload size.

        Read long is the first call that the MessageListener waits for when
        dealing with client or server messages. It reads a long from the socket
        and uses this to feed the read_blob function, indicating the size of
        the blob to be read.

        :return: an unpacked long extracted from the data packet
        """
        size = struct.calcsize("<L")
        data = self.socket.recv(size)
        if data == '':
            # TODO: Relay this as an event
            raise Exception('Socket has disconnected')
        # returning first element because unpack returns a tuple
        return struct.unpack("<L", data)[0]

    def _read_message(self) -> tuple:
        """Read an entire network message and return a dictionary.

        read_message decodes json messages coming from the socket and
        returns the result as a dictionary.

        :return: json decoded dictionary containing the message content.
        """
        datasize = self._read_long()
        data = self._read_blob(datasize)
        return json.loads(data)

    def listen_for_events(self) -> None:
        """Loop and listen for events until the socket disconnects.

        listen_for_events loops the objects _read_message method and passes
        along network related events to listening event delegators.
        """
        while True:
            try:
                message = self._read_message()
                event = self.serializer.serialize_event(message)
                self.delegator.delegate(event)
            # Maybe actually handle the exception, we actually just want to
            # break the loop
            except Exception as e:
                print(e)
                event = Event(
                    'ConnectionEventListener',
                    'disconnect',
                    {'socket': self.socket}
                )
                self.delegator.delegate(event)
                self.socket.close()
                break


def send(conn, event: Event):
    json_data = json.dumps(EventSerializer().deserialize_event(event)).encode(
        'utf-8')
    conn.sendall(struct.pack("<L", len(json_data)))
    conn.sendall(json_data)


def get_socket_address(sock):
    return str(sock.getpeername())

