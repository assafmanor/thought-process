from ctypes import c_int64
import datetime as dt
import struct


_UID_FORMAT = 'Q'
_UINT32 = 'I'
_BDATE_GENDER_FORMAT = 'Ic'
_SNAPSHOT_FIRST = 'Qddddddd'
_IMAGE_DIMS = 'II'
_FEELINGS = 'ffff'
_ALLOWED_FIELDS = {'translation',
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
        timestamp = int(self.birthdate.timestamp())
        data.extend(struct.pack('I', timestamp))
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
        self.fields = set(fields)

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
                 timestamp_ms,
                 translation=(0, 0, 0),
                 rotation=(0, 0, 0, 0),
                 color_image=(0, 0, None),
                 depth_image=(0, 0, None),
                 feelings=(0, 0, 0, 0)):
        self.timestamp_ms = timestamp_ms
        self.translation, self.rotation = translation, rotation
        self.color_image, self.depth_image = color_image, depth_image
        self.feelings = feelings

    def __str__(self):
        if '_cached_str' in self.__dict__:
            return self._cached_str
        IMG_STR = '<Image: {type} {width}x{height}>\n'
        cimg = ''
        w, h = self.color_image[:2]
        if w > 0 and h > 0:
            cimg = IMG_STR.format(type="color", width=w, height=h)
        dimg = ''
        w, h = self.depth_image[:2]
        datetime = dt.datetime.fromtimestamp(self.timestamp_ms/1000.0)
        if w > 0 and h > 0:
            dimg = IMG_STR.format(type="depth", width=w, height=h)
        hu, th, ex, ha = self.feelings
        self._cached_str = f"""{datetime}:
{cimg}{dimg}\
translation=({', '.join(format(val, '.2f') for val in self.translation)}), \
rotation=({', '.join(format(val, '.2f') for val in self.rotation)})
hunger={hu}, thirst={th}, exhaustion={ex}, happiness={ha}"""
        return self._cached_str

    def __repr__(self):
        return self.__str__()

    def serialize(self):
        data = bytearray()
        data.extend(struct.pack(
            _SNAPSHOT_FIRST,
            self.timestamp_ms,
            *self.translation,
            *self.rotation)
            )
        w, h, img_data = self.color_image
        data.extend(struct.pack(_IMAGE_DIMS, w, h))
        if w > 0 and h > 0:
            data.extend(img_data)
        w, h, img_data = self.depth_image
        data.extend(struct.pack(_IMAGE_DIMS, w, h))
        if w > 0 and h > 0:
            data.extend(img_data)
        data.extend(struct.pack(_FEELINGS, *self.feelings))
        return bytes(data)

    @classmethod
    def deserialize(cls, data):
        bytes_read = c_int64(0)  # a mutable integer
        timestamp_ms, t0, t1, t2, r0, r1, r2, r3, w, h = \
            _read_data(data, bytes_read, _SNAPSHOT_FIRST+_IMAGE_DIMS)
        color_image = _create_image_tuple(
            data, bytes_read, w, h, _rgb_image_reader)
        w, h = _read_data(data, bytes_read, format=_IMAGE_DIMS)
        depth_image = _create_image_tuple(
            data, bytes_read, w, h, _depth_image_reader)
        feelings = _read_data(data, bytes_read, _FEELINGS)
        translation = (t0, t1, t2)
        rotation = (r0, r1, r2, r3)
        return cls(timestamp_ms,
                   translation, rotation,
                   color_image, depth_image,
                   feelings)

    @classmethod
    def from_reader_snapshot(cls, reader_snapshot, config):
        rs = reader_snapshot
        timestamp_ms = rs.timestamp_ms
        kwargs = {name: val for name, val in rs.__dict__.items()
                  if name in config.fields}
        return cls(timestamp_ms=timestamp_ms, **kwargs)


def _create_image_tuple(data, bytes_read, width, height, image_reader):
    image_data = None
    if width > 0 and height > 0:
        image_data = image_reader(data, bytes_read, width*height)
    return (width, height, image_data)


def _rgb_image_reader(data, bytes_read, size):
    # read width*height*3 bytes - for each r,g,b value
    return _read_bytes(data, bytes_read, 3*size)


def _depth_image_reader(data, bytes_read, size):
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
        ret = data[bytes_read.value: bytes_read.value + size]
    except Exception as e:
        print(f'ERROR: {e}')
    bytes_read.value += size
    return ret


def _read_str(data, bytes_read):
    (usrn_len, ) = _read_data(data, bytes_read, _UINT32)
    try:
        ret_str = data[bytes_read.value: bytes_read.value+usrn_len].decode()
    except Exception as e:
        print(f'ERROR: {e}')
    bytes_read.value += usrn_len
    return ret_str
