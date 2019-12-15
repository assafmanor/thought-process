from ctypes import c_int64
import datetime as dt
from PIL import Image
import struct


_UID_FORMAT = 'Q'
_UINT32 = 'I'
_BDATE_GENDER_FORMAT = 'Ic'
_SNAPSHOT_FIRST = 'Qddddddd'
_IMAGE_DIMS = 'II'
_FEELINGS = 'ffff'
_ALLOWED_FIELDS = { 'timestamp',
                    'translation',
                    'rotation',
                    'color_image',
                    'depth_image',
                    'feelings'}


class Hello:
    def __init__(self, user_id, username, birthdate, gender):
        self.user_id = user_id
        self.username = username
        self.birthdate = birthdate
        self.gender = gender

    def __repr__(self):
        return f"{self.__class__.__name__}(\
id={self.user_id}, \
username={self.username!r}, \
birthdate={self.birthdate}, \
gender={self.gender})"

    def serialize(self):
        usrn_len = len(self.username)
        data = bytearray()
        data.extend(struct.pack(_UID_FORMAT+_UINT32, self.user_id, usrn_len))
        data.extend(self.username.encode())
        data.extend(struct.pack('I', self.birthdate))
        data.extend(self.gender.encode())
        return bytes(data)

    @classmethod
    def deserialize(cls, data):
        bytes_read = c_int64(0)  # a mutable integer
        (user_id, ) = _read_data(data, bytes_read, _UID_FORMAT)
        username = _read_str(data, bytes_read)
        timestamp, gender_byte = \
            _read_data(data, bytes_read, format=_BDATE_GENDER_FORMAT)
        birthdate = dt.datetime.fromtimestamp(timestamp)
        gender = gender_byte.decode()
        return cls(user_id, username, birthdate, gender)


class Config:
    def __init__(self, *fields):
        if not _ALLOWED_FIELDS.issuperset(fields):
            print(f'ERROR: Some of the fields are not allowed.\n\
Allowed fields are:\n{_ALLOWED_FIELDS}.')
        self.fields = fields

    def __repr__(self):
        return f"Config{self.fields}"

    def serialize(self):
        data = bytearray()
        data.extend(struct.pack(_UINT32, len(self.fields)))
        for field in self.fields:
            data.extend(struct.pack(_UINT32, len(field)))
            data.extend(field.encode())
        return bytes(data)
    
    @classmethod
    def deserialize(cls, data):
        bytes_read = c_int64(0)  # a mutable integer
        (num_fields, ) = _read_data(data, bytes_read, _UINT32)
        fields = []
        for i in range(num_fields):
            fields.append(_read_str(data, bytes_read))
        return cls(*fields)


class Snapshot:
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
        IMG_STR = '<Image: {type} {width}x{height}>\n'
        cimg = ''
        if self.color_image is not None:
            cimg = IMG_STR.format(
                type="color",
                width=self.color_image.width, 
                height=self.color_image.height)
        dimg = ''
        if self.depth_image is not None:
            dimg = IMG_STR.format(
                type="depth",
                width=self.depth_image.width,
                height=self.depth_image.height)
        
        return f"""{self.datetime}:
{cimg}{dimg}translation=({', '.join(format(val, '.2f') for val in self.translation)}), \
rotation=({', '.join(format(val, '.2f') for val in self.rotation)})
hunger={self.hunger}, thirst={self.thirst}, \
exhaustion={self.exhaustion}, happiness={self.happiness}"""

    def __repr__(self):
        return self.__str__()

    def serialize(self):
        ts_ms = int(self.datetime.timestamp()*1000)
        data = bytearray()
        data.extend(struct.pack(
            _SNAPSHOT_FIRST, ts_ms, *self.translation, *self.rotation)
            )
        if self.color_image is None:
            data.extend(struct.pack(_IMAGE_DIMS, 0, 0))
        else:
            w, h = self.color_image.width, self.color_image.height
            data.extend(struct.pack(_IMAGE_DIMS, w, h))
            #serialize color_image
            pixels = self.color_image.getdata()
            img_data = [j for i in pixels for j in i]
            data.extend(img_data)
        if self.depth_image is None:
            data.extend(struct.pack(_IMAGE_DIMS, 0, 0))
        else:
            w, h = self.depth_image.width, self.depth_image.height
            data.extend(struct.pack(_IMAGE_DIMS, w, h))
            floats = self.depth_image.getdata()
            for f in floats:
                data.extend(struct.pack('f', f))
        feelings = self.hunger, self.thirst, self.exhaustion, self.happiness
        data.extend(struct.pack(_FEELINGS, *feelings))
        return bytes(data)
    
    @classmethod
    def deserialize(cls, data):
        bytes_read = c_int64(0)  # a mutable integer
        timestamp_ms, t0, t1, t2, r0, r1, r2, r3, w, h = \
            _read_data(data, bytes_read, _SNAPSHOT_FIRST+_IMAGE_DIMS)
        color_image = None
        if w > 0 and h > 0:
            color_image = cls._create_image_from_data(
                w, h, data, bytes_read, cls._rgb_image_reader)
        w, h = _read_data(data, bytes_read, format=_IMAGE_DIMS)
        depth_image = None
        if w > 0 and h > 0:
            depth_image = cls._create_image_from_data(
                w, h, data, bytes_read, cls._depth_image_reader, mode='F')
        hunger, thirst, exhaustion, happiness = \
                _read_data(data, bytes_read, _FEELINGS)
        datetime = dt.datetime.fromtimestamp(timestamp_ms/1000.0)
        translation = (t0, t1, t2)
        rotation = (r0, r1, r2, r3)
        return cls(datetime,
        translation, rotation,
        color_image, depth_image,
        hunger, thirst, exhaustion, happiness)

    @classmethod
    def _create_image_from_data( \
        cls, width, height, data, bytes_read, image_reader, mode='RGB'):
        img_data = image_reader(data, bytes_read, width*height)
        return Image.frombytes(mode, (width, height), img_data)

    @classmethod
    def _rgb_image_reader(cls, data, bytes_read, size):
        # read width*height*3 bytes - for each r,g,b value
        return _read_bytes(data, bytes_read, 3*size)

    @classmethod
    def _depth_image_reader(cls, data, bytes_read, size):
        float_size = struct.calcsize('f')
        depth_values = _read_bytes(data, bytes_read, size*float_size)
        return depth_values


def _read_data(data, bytes_read, format):
    size = struct.calcsize(format)
    try:
        ret = struct.unpack_from(format, data, offset=bytes_read.value)
    except Exception as e:
        print(f'ERROR: {e}')
    bytes_read.value += size
    return ret


def _read_bytes(data, bytes_read, size):
    try:
        ret = data[bytes_read.value : bytes_read.value + size]
    except Exception as e:
        print(f'ERROR: {e}')
    bytes_read.value += size
    return ret


def _read_str(data, bytes_read):
    (usrn_len, ) = _read_data(data, bytes_read, _UINT32)
    try:
        ret_str = data[bytes_read.value : bytes_read.value+usrn_len].decode()
    except Exception as e:
        print(f'ERROR: {e}')
    bytes_read.value += usrn_len
    return ret_str