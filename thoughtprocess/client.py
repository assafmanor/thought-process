from .utils import Config
from .utils import Connection
from .utils import Hello
from .utils import Snapshot


def upload_snapshot(address, reader):
    hello = Hello(
        reader.user_id, reader.username, reader.birthdate, reader.gender)
    hello_ser = hello.serialize()
    host, port = address
    counter = 0
    for rsnapshot in reader:
        with Connection.connect(host, port) as conn:
            conn.send_message(hello_ser)
            config = Config.deserialize(conn.receive_message())
            conn.send_message(
                Snapshot.from_reader_snapshot(rsnapshot, config).serialize())
        counter += 1
        print(f'Snapshot #{counter} sent.')
