import datetime as dt
from PIL import Image
import pathlib
import struct


_USER_INFO_FIRST = 'QI'
_USER_INFO_SECOND = 'Ic'
_TIMESTAMP = 'Q'
_TRANSLATION = 'ddd'
_ROTATION = 'dddd'
_IMAGE_DIMS = 'II'
_FEELINGS = 'ffff'

_ERROR_INVALID_FILE = 'file is corrupted.'


class ReaderSnapshot():
    def __init__(self,
        datetime,
        translation, rotation,
        color_image, depth_image,
        hunger, thirst, exhaustion, happiness):
            self.datetime = datetime
            self.translation, self.rotation = translation, rotation
            self.color_image, self.depth_image = color_image, depth_image
            self.hunger, self.thirst, self.exhaustion, self.happiness = \
                hunger, thirst, exhaustion, happiness

    def __str__(self):
        IMG_STR = '<Image: {type} {width}x{height}>'
        cimg = IMG_STR.format(
            type="color",
            width=self.color_image.width, 
            height=self.color_image.height)
        dimg = IMG_STR.format(
            type="depth",
            width=self.depth_image.width,
            height=self.depth_image.height)
        
        return f"""{self.datetime}:
{cimg}
{dimg}
translation=({', '.join(format(val, '.2f') for val in self.translation)}), \
rotation=({', '.join(format(val, '.2f') for val in self.rotation)})
hunger={self.hunger}, thirst={self.thirst}, \
exhaustion={self.exhaustion}, happiness={self.happiness}"""


class Reader:
    def __init__(self, path_str):
        self.path = pathlib.Path(path_str)
        self._bytes_read = 0
        self._gather_user_info()

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.path.absolute()}')"

    def __iter__(self):
        return self

    def __next__(self):
        return self._get_next_snapshot()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _gather_user_info(self):
        with self.path.open(mode='rb') as fp:
            self.user_id, usrn_len = \
                self._read_file(fp, format=_USER_INFO_FIRST)
            self.username = self._read_file(fp, size=usrn_len).decode()
            timestamp, gender_byte = \
                self._read_file(fp, format=_USER_INFO_SECOND)
            self.birthdate = dt.datetime.fromtimestamp(timestamp)
            self.gender = gender_byte.decode()

    def _get_next_snapshot(self):
        format = _TIMESTAMP+_TRANSLATION+\
            _ROTATION+_IMAGE_DIMS
        with self.path.open(mode='rb') as fp:
            fp.seek(self._bytes_read)
            timestamp_ms, t0, t1, t2, r0, r1, r2, r3, h, w = \
                self._read_file(fp, format=format)
            color_image = self._create_image_from_file(
                w, h, fp, self._rgb_image_adder)
            h, w = self._read_file(fp, format=_IMAGE_DIMS)
            depth_image = self._create_image_from_file(
                w, h, fp, self._depth_image_adder, mode='F')
            hunger, thirst, exhaustion, happiness = \
                self._read_file(fp, format=_FEELINGS)
        datetime = dt.datetime.fromtimestamp(timestamp_ms/1000.0)
        translation = (t0, t1, t2)
        rotation = (r0, r1, r2, r3)
        return ReaderSnapshot(datetime,
        translation, rotation,
        color_image, depth_image,
        hunger, thirst, exhaustion, happiness)

    def _create_image_from_file(self, width, height, fp, data_adder, mode='RGB'):
        img_data = data_adder(fp, width*height)
        return Image.frombytes(mode, (width, height), img_data)

    def _rgb_image_adder(self, fp, size):
        colors = bytearray(self._read_file(fp, size=3*size))
        # rearrange image format from bgr to rgb
        for i in range(0, size*3, 3):
            colors[i:i+3] = colors[i:i+3][::-1]
        return bytes(colors)

    def _depth_image_adder(self, fp, size):
        float_size = struct.calcsize('f')
        depth_values = self._read_file(fp, size=size*float_size)
        return depth_values

    def _read_file(self, fp, format=None, size=None):
        if format is None and size is None:
            raise Exception('No header format or size were given.')
        if format is not None and size is not None:
            raise Exception('Both header format and size were given.')
        if size is None:
            size = struct.calcsize(format)
        data = fp.read(size)
        if len(data) != size:   # reached EOF unexpectedly
            raise EOFError(f'ERROR: {_ERROR_INVALID_FILE}')
        self._bytes_read += size
        if format is None:
            return data
        return struct.unpack(format, data)
