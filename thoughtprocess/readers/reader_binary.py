import datetime as dt
import pathlib
from .abstractreader import AbstractReader
from .reader_registrator import ReaderRegistrator
from ..utils import BinaryFile
from ..utils import Hello, Snapshot

_USER_INFO_FIRST = 'QI'
_USER_INFO_SECOND = 'Ic'
_TIMESTAMP = 'Q'
_TRANSLATION = 'ddd'
_ROTATION = 'dddd'
_IMAGE_DIMS = 'II'
_FEELINGS = 'ffff'


@ReaderRegistrator.register('binary')
class BinaryReader(AbstractReader):
    def __init__(self, path_str):
        self.path = pathlib.Path(path_str)

    def start(self):
        file = self.path.open(mode='rb')
        self.bin_file = BinaryFile(file)
        self._gather_user_info()

    def stop(self):
        self.bin_file.close()

    def _gather_user_info(self):
        user_id, usrn_len = \
            self.bin_file.read(format=_USER_INFO_FIRST)
        username = self.bin_file.read(size=usrn_len).decode()
        timestamp, gender_byte = \
            self.bin_file.read(format=_USER_INFO_SECOND)
        birthdate = dt.datetime.fromtimestamp(timestamp)
        gender = gender_byte.decode()
        self.hello = Hello(user_id, username, birthdate, gender)

    def next_snapshot(self):
        if self.bin_file.is_eof():
            raise StopIteration
        bin_f = self.bin_file
        format = _TIMESTAMP + _TRANSLATION + \
            _ROTATION + _IMAGE_DIMS
        timestamp_ms, t_x, t_y, t_z, \
            r_x, r_y, r_z, r_w, \
            h, w = bin_f.read(format=format)
        color_img = _create_image_tuple(bin_f, w, h, _rgb_image_reader)
        h, w = bin_f.read(format=_IMAGE_DIMS)
        depth_img = _create_image_tuple(bin_f, w, h, _depth_image_adder)
        feelings = bin_f.read(format=_FEELINGS)
        translation = (t_x, t_y, t_z)
        rotation = (r_x, r_y, r_z, r_w)
        return Snapshot(timestamp_ms,
                        translation, rotation,
                        color_img, depth_img,
                        feelings)


def _create_image_tuple(bin_file, width, height, image_reader):
    image_data = image_reader(bin_file, width*height)
    return (width, height, image_data)


def _rgb_image_reader(bin_file, size):
    colors = bytearray(bin_file.read(size=3*size))
    # rearrange image format from bgr to rgb
    for i in range(0, size*3, 3):
        colors[i:i+3] = colors[i:i+3][::-1]
    return bytes(colors)


def _depth_image_adder(bin_file, size):
    return bin_file.read(format=f'{size}f')
