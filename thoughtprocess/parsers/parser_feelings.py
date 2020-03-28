from .abstractparser import AbstractParser
from .parser_registrator import ParserRegistrator


@ParserRegistrator.register('feelings')
class LocationParser(AbstractParser):
    @classmethod
    def parse(cls, data):
        metadata = cls.get_metadata(data)
        return {**metadata,
                'feelings': data['feelings']}
