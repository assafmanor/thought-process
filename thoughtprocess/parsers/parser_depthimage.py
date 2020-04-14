import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
import pathlib

from .abstractparser import AbstractParser
from .parser_registrator import ParserRegistrator


_DEPTH_IMAGE_FILENAME = 'depth_image.jpg'


@ParserRegistrator.register('depth_image')
class DepthImageParser(AbstractParser):
    @classmethod
    def parse(cls, data):
        metadata = cls.get_metadata(data)
        width, height, path_str = data['depth_image']
        path = pathlib.Path(path_str)
        savepath = path.parent / _DEPTH_IMAGE_FILENAME
        with path.open('rb') as f:
            img_bytes = f.read()
        path.unlink() # delete file
        image = Image.frombytes('F', (width, height), img_bytes)
        plt.imsave(savepath, image, cmap=cm.RdYlGn)
        return {**metadata,
                'depth_image': str(savepath)}
