import sys
from ..utils import Config
from ..utils import Connection
from ..utils import Snapshot
from ..readers.reader_protobuf import ProtobufReader
from ..readers.cognition import Cognition

def upload_sample(host, port, path, reader_cls=ProtobufReader):
    try:
        with Cognition(path, reader_cls) as cognition:
            hello = cognition.get_info()
            hello_ser = hello.serialize()
            count = 0
            for snapshot in cognition:
                with Connection.connect(host, port) as conn:
                    conn.send_message(hello_ser)
                    config = Config.deserialize(conn.receive_message())
                    conn.send_message(
                        Snapshot.from_snapshot_config(snapshot, config).serialize())
                count += 1
                print(f'Snapshot #{count} sent.')
        print('Done .')
    except KeyboardInterrupt:
        return
    except Exception as error:
        print(f'ERROR: failed to upload snapshot: {error}.', file=sys.stderr)
        return 1
