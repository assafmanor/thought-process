import datetime as dt
import errno
import pathlib
import socket
import struct
import threading
from .thought import Thought
from .utils import Listener
from .utils import Connection


UINT64_SIZE = 8
UINT32_SIZE = 4
HEADER_FORMAT = 'QQI'


class FileHandler:
    def __init__(self, path_str):
        self.path = pathlib.Path(path_str)


    def create_path(self):
        """Creates the missing directories in the path, if there are any."""
        path_list = self.path.parts
        cur_path = pathlib.Path(path_list[0])
        i = 1
        while cur_path.exists() and i < len(path_list):
            cur_path = cur_path / path_list[i]
            i += 1
        #create the missing directories
        if not cur_path.exists():
            cur_path.mkdir()
        while i < len(path_list):
            cur_path = cur_path / path_list[i]
            cur_path.mkdir()
            i += 1


    '''
    Writes message to the end of self.path/dirname/filename.
    if dirname and/or filename do not exists, they will be created.
    A lock is used in order to prevent messages that are to be written to the same file at the same time from writing themselves on top of each other.
    '''
    def write_to_end_of_file(self, dirname, filename, message, lock):
        cur_path = self.path / dirname
        file_path = cur_path / filename
        lock.acquire()
        try:
            if not cur_path.exists():
                cur_path.mkdir()
            if file_path.exists():
                message = '\n' + message
            if file_path.is_dir():
                raise Exception (f'ERROR: file path {file_path} exists as a directory.')
            file_path.open('a+').write(message)
        finally:
            lock.release()


'''
This class handles a connection to the server, with the ability to several 
'''
class ConnectionHandler(threading.Thread):

    recv_lock = threading.Lock()        # Used for receiving messages concurrently.
    writing_lock = threading.Lock()     # Used for writing to the same file concurrently.
    file_handler = None
    
    def __init__(self, connection):
        super().__init__()
        self.connection = connection


    def set_file_handler(file_handler):
        ConnectionHandler.file_handler = file_handler

    
    '''
    Receives data from a client and prints the message to stdout (one sec after receiving), in the following format:
    [{date and time sent}] user {user_id}: {thought}.
    This method uses a Mutex in order to be able to receive thoughts from several clients concurrently and correctly.
    '''
    def run(self):
        ConnectionHandler.recv_lock.acquire()
        try:            
            user_id, timestamp, thought_size = struct.unpack(HEADER_FORMAT, self.connection.receive(2*UINT64_SIZE + UINT32_SIZE))      # critical
            thought = self.connection.receive(thought_size).decode()                                                                   # section
        finally:
            ConnectionHandler.recv_lock.release()
        self.connection.close()
        message = Thought(user_id, dt.datetime.fromtimestamp(timestamp), thought)
        filename = message.timestamp_file_format()
        ConnectionHandler.file_handler.write_to_end_of_file(str(message.user_id), f'{filename}.txt', message.thought, ConnectionHandler.writing_lock)


def run_server(address, data_dir):
    file_handler = FileHandler(data_dir)
    file_handler.create_path()
    ConnectionHandler.set_file_handler(file_handler)
    host, port = address
    listener = Listener(port, host)
    listener.start()
    # accept new connections and receive thoughts until the program is interrupted.
    while True:
        connection = listener.accept()
        handler = ConnectionHandler(connection)
        handler.start()
