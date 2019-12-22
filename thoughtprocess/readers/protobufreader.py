import datetime as dt
import gzip
from .abstractreader import AbstractReader
from ..utils import BinaryFile
from .cortex_pb2 import User as ProtobufUser
from .cortex_pb2 import Snapshot as ProtobufSnapshot
from .reader_registrator import ReaderRegistrator
from ..utils.protocols import Snapshot, Hello


gender_dict = {0: 'm', 1: 'f', 2: 'o'}


@ReaderRegistrator.register('protobuf')
class ProtobufReader(AbstractReader):
    def start(self):
        file = gzip.open(self.path, mode='rb')
        self.bin_file = BinaryFile(file)
        pb_user = ProtobufUser()
        pb_user.ParseFromString(self.bin_file.read_message())
        birthdate = birthdate = dt.datetime.fromtimestamp(pb_user.birthday)
        gender = gender_dict[pb_user.gender]
        self.hello = Hello(pb_user.user_id,
                           pb_user.username,
                           birthdate,
                           gender)

    def stop(self):
        self.bin_file.close()

    def next_snapshot(self):
        if self.bin_file.is_eof():
            raise StopIteration
        pb_snapshot = ProtobufSnapshot()
        pb_snapshot.ParseFromString(self.bin_file.read_message())
        datetime = pb_snapshot.datetime
        translation = (pb_snapshot.pose.translation.x,
                       pb_snapshot.pose.translation.y,
                       pb_snapshot.pose.translation.z)
        rotation = (pb_snapshot.pose.rotation.x,
                    pb_snapshot.pose.rotation.y,
                    pb_snapshot.pose.rotation.z,
                    pb_snapshot.pose.rotation.w)
        color_image = (pb_snapshot.color_image.width,
                       pb_snapshot.color_image.height,
                       pb_snapshot.color_image.data)
        depth_image = (pb_snapshot.depth_image.width,
                       pb_snapshot.depth_image.height,
                       pb_snapshot.depth_image.data)
        feelings = (pb_snapshot.feelings.hunger,
                    pb_snapshot.feelings.thirst,
                    pb_snapshot.feelings.exhaustion,
                    pb_snapshot.feelings.happiness)
        return Snapshot(datetime, 
                        translation,
                        rotation,
                        color_image,
                        depth_image,
                        feelings)