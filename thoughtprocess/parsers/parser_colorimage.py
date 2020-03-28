from PIL import Image
import pathlib

from .abstractparser import AbstractParser
from .parser_registrator import ParserRegistrator


_COLOR_IMAGE_FILE_NAME = 'color_image.jpg'


@ParserRegistrator.register('color_image')
class ColorImageParser(AbstractParser):
    @classmethod
    def parse(cls, data):
        metadata = cls.get_metadata(data)
        width, height, path_str = data['color_image']
        path = pathlib.Path(path_str)
        savepath = path.parent / _COLOR_IMAGE_FILE_NAME
        with path.open('rb') as f:
            img_bytes = f.read()
        image = Image.frombytes('RGB', (width, height), img_bytes)
        image.save(savepath)
        return {**metadata,
                'color_image': str(savepath)}

