from ..utils import Config
from ..utils import Hello
from ..utils import Listener
from ..utils import ALLOWED_FIELDS
from ..utils import Snapshot
import threading
from ..thoughts import ThoughtContext

class ConnectionHandler(threading.Thread):
    '''
    This class handles a connection to the server, with the ability to several
    '''

    lock = threading.Lock()

    def __init__(self, connection, publish):
        super().__init__()
        self.connection = connection
        self.publish = publish

    def run(self):
        conn = self.connection
        user = Hello.deserialize(conn.receive_message())
        config = Config(*ALLOWED_FIELDS)
        conn.send_message(config.serialize())
        snapshot = Snapshot.deserialize(conn.receive_message())
        context = ThoughtContext(user, snapshot)
        data_json = context.get_json()
        with ConnectionHandler.lock:
            self.publish(data_json)
        print('Thought published!')


def run_server(host, port, publish):
    print('Server started')
    with Listener(port, host) as listener:
        while True:
            print('Waiting for connections...')
            connection = listener.accept()
            print(connection)
            handler = ConnectionHandler(connection, publish)
            handler.start()
