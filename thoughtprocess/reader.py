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


class ReaderSnapshot:
    def __init__(self,
        timestamp_ms,
        translation, rotation,
        color_image, depth_image,
        feelings):
            self.timestamp_ms = timestamp_ms
            self.translation, self.rotation = translation, rotation
            self.color_image, self.depth_image = color_image, depth_image
            self.feelings = feelings

    def __str__(self):
        IMG_STR = '<Image: {type} {width}x{height}>'
        w, h = self.color_image[:2]
        cimg = IMG_STR.format(
            type="color",
            width=w, 
            height=h)
        w, h = self.depth_image[:2]
        datetime = dt.datetime.fromtimestamp(self.timestamp_ms/1000.0)
        dimg = IMG_STR.format(
            type="depth",
            width=w,
            height=h)
        hu, th, ex, ha = self.feelings
        return f"""{datetime}:
{cimg}
{dimg}
translation=({', '.join(format(val, '.2f') for val in self.translation)}), \
rotation=({', '.join(format(val, '.2f') for val in self.rotation)})
hunger={hu}, thirst={th}, \
exhaustion={ex}, happiness={ha}"""


class Reader:
    def __init__(self, path_str):
        self.path = pathlib.Path(path_str)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.path.absolute()}')"

    def __iter__(self):
        return self

    def __next__(self):
        return self._get_next_snapshot()

    def __enter__(self):
        self.fp = self.path.open(mode='rb')
        self._gather_user_info()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()

    def _gather_user_info(self):
        self.user_id, usrn_len = \
            self._read_file(format=_USER_INFO_FIRST)
        self.username = self._read_file(size=usrn_len).decode()
        timestamp, gender_byte = \
            self._read_file(format=_USER_INFO_SECOND)
        self.birthdate = dt.datetime.fromtimestamp(timestamp)
        self.gender = gender_byte.decode()

    def _get_next_snapshot(self):
        format = _TIMESTAMP+_TRANSLATION+\
            _ROTATION+_IMAGE_DIMS
        timestamp_ms, t_x, t_y, t_z, \
        r_x, r_y, r_z, r_w, \
        h, w = self._read_file(format=format)
        color_img = self._create_image_tuple(w, h, self._rgb_image_reader)
        h, w = self._read_file(format=_IMAGE_DIMS)
        depth_img = self._create_image_tuple(w, h, self._depth_image_adder)
        feelings = self._read_file(format=_FEELINGS)
        translation = (t_x, t_y, t_z)
        rotation = (r_x, r_y, r_z, r_w)
        return ReaderSnapshot(timestamp_ms,
                                translation, rotation,
                                color_img, depth_img,
                                feelings)
    
    def _create_image_tuple(self, width, height, image_reader):
        image_data = image_reader(width*height)
        return (width, height, image_data)


    def _rgb_image_reader(self, size):
        colors = bytearray(self._read_file(size=3*size))
        # rearrange image format from bgr to rgb
        for i in range(0, size*3, 3):
            colors[i:i+3] = colors[i:i+3][::-1]
        return bytes(colors)

    def _depth_image_adder(self, size):
        float_size = struct.calcsize('f')
        depth_values = self._read_file(size=size*float_size)
        return bytes(depth_values)

    def _read_file(self, format=None, size=None):
        if format is None and size is None:
            raise Exception('No header format or size were given.')
        if format is not None and size is not None:
            raise Exception('Both header format and size were given.')
        if size is None:
            size = struct.calcsize(format)
        data = self.fp.read(size)
        if len(data) != size:   # reached EOF unexpectedly
            raise EOFError(f'ERROR: {_ERROR_INVALID_FILE}')
        if format is None:
            return data
        return struct.unpack(format, data)
