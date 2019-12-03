import datetime as dt
from .thought import Thought

HEADER_FORMAT = 'QQI'


def upload_thought(connection, user_id, thought):
    message = Thought(user_id, dt.datetime.now(), thought)
    data = message.serialize()
    connection.send(data)
