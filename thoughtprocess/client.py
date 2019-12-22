from .utils import Config
from .utils import Connection
from .utils import Snapshot


def upload_snapshot(address, reader):
    hello = reader.get_info()
    hello_ser = hello.serialize()
    host, port = address
    count = 0
    for snapshot in reader:
        with Connection.connect(host, port) as conn:
            conn.send_message(hello_ser)
            config = Config.deserialize(conn.receive_message())
            conn.send_message(
                Snapshot.from_snapshot_config(snapshot, config).serialize())
        count += 1
        print(f'Snapshot #{count} sent.')
    print('Done.')
