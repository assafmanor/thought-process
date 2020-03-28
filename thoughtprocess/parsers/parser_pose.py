from .abstractparser import AbstractParser
from .parser_registrator import ParserRegistrator


@ParserRegistrator.register('pose')
class PoseParser(AbstractParser):
    @classmethod
    def parse(cls, data):
        metadata = cls.get_metadata(data)
        return {**metadata,
                'translation': data['translation'],
                'rotation': data['rotation']}