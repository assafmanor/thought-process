import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image

from .abstractparser import AbstractParser, ParserContext
from .parser_registrator import ParserRegistrator


_DEPTH_IMAGE_FILENAME = 'depth_image.jpg'


@ParserRegistrator.register('depth_image',)
class DepthImageParser(AbstractParser):
    @staticmethod
    def parse(context: ParserContext):
        width, height, data = context.snapshot.depth_image
        path = context.get_savepath(_DEPTH_IMAGE_FILENAME)
        image = Image.frombytes('F', (width, height), data)
        plt.imsave(path, image, cmap=cm.RdYlGn)
