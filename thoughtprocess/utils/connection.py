import socket
import struct

UINT32 = 'I'
UINT32_SIZE = struct.calcsize(UINT32)

ERROR_MESSAGE = "couldn't receive data from client successfully"


class Connection:

    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        ip, other_port = self.socket.getsockname()
        _, peer_port = self.socket.getpeername()
        return f'<Connection from {ip}:{other_port} \
to {ip}:{peer_port}>'

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

    def send_message(self, message_bytes):
        msg_size = len(message_bytes)
        data = struct.pack(UINT32, msg_size)
        data += message_bytes
        self.send(data)

    def receive_message(self):
        (msg_size, ) = struct.unpack(UINT32, self.receive(UINT32_SIZE))
        return self.receive(msg_size)

    def receive(self, size):
        data = bytearray()
        while len(data) < size:
            packet = self.socket.recv(size - len(data))
            if not packet:
                raise Exception(ERROR_MESSAGE)
            data.extend(packet)
        return bytes(data)

    def close(self):
        self.socket.close()
