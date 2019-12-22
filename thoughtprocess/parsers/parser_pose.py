from .abstractparser import AbstractParser, ParserContext
from .parser_registrator import ParserRegistrator
import json


_TRANSLATION_FILENAME = 'translation.json'
_ROTATION_FILENAME = 'rotation.json'


@ParserRegistrator.register('translation', 'rotation')
class PoseParser(AbstractParser):
    @staticmethod
    def parse(context: ParserContext):
        trans_path = context.get_savepath(_TRANSLATION_FILENAME)
        x, y, z = context.snapshot.translation
        trans_data = {'x': x, 'y': y, 'z': z}
        with trans_path.open('w') as outfile:
            json.dump(trans_data, outfile)
        rot_path = context.get_savepath(_ROTATION_FILENAME)
        x, y, z, w = context.snapshot.rotation
        rot_data = {'x': x, 'y': y, 'z': z, 'w': w}
        with rot_path.open('w') as outfile:
            json.dump(rot_data, outfile)
