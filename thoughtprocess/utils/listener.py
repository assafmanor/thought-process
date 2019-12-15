import errno
import socket
from .connection import Connection


class Listener:

    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr

    def __repr__(self):
        return f'Listener(port={self.port}, \
host={self.host!r}, \
backlog={self.backlog}, \
reuseaddr={self.reuseaddr})'

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.server = socket.socket()
        if self.reuseaddr:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server.bind((self.host, self.port))
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print(f'ERROR: port {self.port} is already in use.')
            else:
                print(f'ERROR: {e}')
            return
        self.server.listen(self.backlog)

    def stop(self):
        try:
            self.server.close()
        except AttributeError:
            print('ERROR: Server did not start listening yet.')
        except Exception as e:
            print(e)

    def accept(self):
        client, _ = self.server.accept()
        return Connection(client)
