from .abstractparser import AbstractParser
from .parser_registrator import ParserRegistrator


@ParserRegistrator.register('pose')
class PoseParser(AbstractParser):
    @classmethod
    def parse(cls, data):
        metadata = cls.get_metadata(data)
        pose = {'translation': data['translation'],
                'rotation': data['rotation']}
        return {**metadata,
                'pose': pose}