import os
import struct


_UINT32 = 'I'
_ERROR_INVALID_FILE = 'file is corrupted'


class BinaryFile:
    def __init__(self, file):
        self.file = file

    def read(self, format=None, size=None):
        if format is None and size is None:
            raise Exception('No header format or size were given.')
        if format is not None and size is not None:
            raise Exception('Both header format and size were given.')
        if size is None:
            size = struct.calcsize(format)
        data = self.file.read(size)
        if len(data) != size:   # reached EOF unexpectedly
            raise EOFError(f'ERROR: {_ERROR_INVALID_FILE}.')
        if format is None:
            return data
        return struct.unpack(format, data)

    def read_message(self):
        (message_len, ) = self.read(format=_UINT32)
        return self.read(size=message_len)

    def is_eof(self):
        data = self.file.read(1)
        if not data:
            return True
        self.file.seek(-1, os.SEEK_CUR)
        return False

    def close(self):
        self.file.close()


class BinaryData:
    def __init__(self, data):
        self.data = data
        self.bytes_read = 0

    def read_data(self, format):
        size = struct.calcsize(format)
        ret = struct.unpack_from(format, self.data, offset=self.bytes_read)
        self.bytes_read += size
        return ret

    def read_bytes(self, size):
        ret = self.data[self.bytes_read: self.bytes_read + size]
        self.bytes_read += size
        return ret

    def read_str(self):
        (str_len, ) = self.read_data(_UINT32)
        return self.read_bytes(str_len).decode()
