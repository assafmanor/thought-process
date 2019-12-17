from .utils import Config
from .utils import Hello
from .utils import Listener
from .utils import Parser
from .utils import Snapshot
import threading


_CONFIG_FIELDS = {'translation', 'color_image'}


class ConnectionHandler(threading.Thread):
    '''
    This class handles a connection to the server, with the ability to several
    '''

    # Used for parsing concurrently.
    parsing_lock = threading.Lock()

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    @classmethod
    def set_parsers(cls, parsers):
        cls.parsers = parsers

    def run(self):
        conn = self.connection
        hello = Hello.deserialize(conn.receive_message())
        config = Config(*_CONFIG_FIELDS)
        conn.send_message(config.serialize())
        snapshot = Snapshot.deserialize(conn.receive_message())
        with ConnectionHandler.parsing_lock:
            for parser in ConnectionHandler.parsers.values():
                parser(hello, snapshot)
        print(f'Snapshot received.')


def run_server(address, data_dir):
    parsers = {field: parser for field, parser in Parser.parsers.items()
               if field in _CONFIG_FIELDS}
    Parser.data_dir = data_dir
    ConnectionHandler.set_parsers(parsers)
    host, port = address
    with Listener(port, host) as listener:
        while True:
            connection = listener.accept()
            handler = ConnectionHandler(connection)
            handler.start()
