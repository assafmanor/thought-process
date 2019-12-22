from PIL import Image

from .abstractparser import AbstractParser
from .abstractparser import ParserContext
from .parser_registrator import ParserRegistrator

_COLOR_IMAGE_FILE_NAME = 'color_image.jpg'


@ParserRegistrator.register('color_image')
class ColorImageParser(AbstractParser):
    @staticmethod
    def parse(context: ParserContext):
        path = context.get_savepath(_COLOR_IMAGE_FILE_NAME)
        width, height, data = context.snapshot.color_image
        image = Image.frombytes('RGB', (width, height), data)
        image.save(path)
