from .utils import Config
from .utils import Hello
from .utils import Listener
from .parsers import ParserContext, ParserRegistrator
from .utils import Snapshot
import threading


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

    @classmethod
    def set_datadir(cls, data_dir):
        cls.data_dir = data_dir

    def run(self):
        conn = self.connection
        user = Hello.deserialize(conn.receive_message())
        config = Config(*ParserRegistrator.fields)
        conn.send_message(config.serialize())
        snapshot = Snapshot.deserialize(conn.receive_message())
        data_dir = ConnectionHandler.data_dir
        with ConnectionHandler.parsing_lock:
            for parser in ConnectionHandler.parsers:
                context = ParserContext(data_dir, user, snapshot)
                parser(context)
        print(f"Snapshot saved at \'{context.get_savepath('').absolute()}\'.")


def run_server(address, data_dir):
    ConnectionHandler.set_datadir(data_dir)
    ConnectionHandler.set_parsers(ParserRegistrator.parsers)
    host, port = address
    with Listener(port, host) as listener:
        while True:
            connection = listener.accept()
            handler = ConnectionHandler(connection)
            handler.start()
