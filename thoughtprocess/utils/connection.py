import socket


ERROR_MESSAGE = "ERROR: Couldn't receive data from client successfully."


class Connection:

    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        server_ip, server_port = self.socket.getpeername()
        client_ip, client_port = self.socket.getsockname()
        return f'<Connection from {client_ip}:{client_port} \
to {server_ip}:{server_port}>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return cls(sock)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data = bytearray()
        while len(data) < size:
            packet = self.socket.recv(size - len(data))
            if not packet:
                raise Exception(ERROR_MESSAGE)
            data.extend(packet)
        return data

    def close(self):
        self.socket.close()
