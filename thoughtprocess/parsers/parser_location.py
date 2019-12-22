from .abstractparser import AbstractParser, ParserContext
from .parser_registrator import ParserRegistrator
# import json


_LOCATION_FILENAME = None  # TODO


@ParserRegistrator.register('translation', 'rotation', 'depth_image')
class LocationParser(AbstractParser):
    @staticmethod
    def parse(context: ParserContext):
        pass  # TODO
