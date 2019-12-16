import datetime as dt
from PIL import Image
import json
import pathlib
from .protocols import Hello
from .protocols import Snapshot


_TRANSLATION_FILE_NAME = 'translation.json'
_COLOR_IMAGE_FILE_NAME = 'color_image.jpg'
_DATETIME_FILE_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'


class Parser:
    parsers = dict()
    data_dir = None
    
    @staticmethod
    def add_parser(name):
        def decorator(cls):
            Parser.parsers[name] = cls.parse
            return cls
        return decorator


    @classmethod
    def parse(cls, hello, snapshot):
        raise NotImplementedError


@Parser.add_parser('translation')
class TranslationParser(Parser):
    @classmethod
    def parse(cls, hello, snapshot):
        x, y, z = snapshot.translation
        data = {'x': x, 'y': y, 'z': z}
        sdir = _get_save_dir(cls.data_dir, hello.user_id, snapshot.timestamp_ms)
        _create_dir(sdir)
        path = sdir / _TRANSLATION_FILE_NAME
        with path.open('w') as outfile:
            json.dump(data, outfile)


@Parser.add_parser('color_image')
class ColorImageParser(Parser):
    @classmethod
    def parse(cls, hello, snapshot):
        sdir = _get_save_dir(cls.data_dir, hello.user_id, snapshot.timestamp_ms)
        _create_dir(sdir)
        path = sdir / _COLOR_IMAGE_FILE_NAME
        image = _create_image_from_data(snapshot.color_image)
        image.save(path)



def _get_save_dir(data_dir, user_id, timestamp_ms):
    datetime = dt.datetime.fromtimestamp(timestamp_ms/1000.0)
    # show only four digits in microseconds
    dt_format = datetime.strftime(_DATETIME_FILE_FORMAT)[:-2]
    return pathlib.Path(data_dir) / str(user_id) / dt_format


def _create_dir(dir_path):
    dir_path.mkdir(parents=True, exist_ok=True)


def _create_image_from_data(image_tuple, mode='RGB'):
    width, height, data = image_tuple
    return Image.frombytes(mode, (width, height), data)