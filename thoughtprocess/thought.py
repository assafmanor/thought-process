import datetime as dt
import struct

UINT64_SIZE = 8
UINT32_SIZE = 4
HEADER_FORMAT = 'QQI'


class Thought:

    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id}, \
timestamp={self.timestamp!r}, \
thought={self.thought!r})'

    def __str__(self):
        time_format = f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        return f'[{time_format}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        return (self.user_id == other.user_id) and \
            (self.timestamp == other.timestamp) and \
            (self.thought == other.thought)

    def serialize(self):
        header = struct.pack(
            HEADER_FORMAT,
            self.user_id,
            int(dt.datetime.timestamp(self.timestamp)),
            len(self.thought)
            )
        return header + self.thought.encode('utf-8')

    def deserialize(data):
        user_id, timestamp, _ = struct.unpack(HEADER_FORMAT, data[:20])
        thought = data[20:].decode('utf-8')
        time = dt.datetime.fromtimestamp(timestamp)
        return Thought(user_id, time, thought)

    def timestamp_file_format(self):
        return self.timestamp.strftime('%Y-%m-%d_%H-%M-%S')
