from .abstractparser import AbstractParser, ParserContext
from .parser_registrator import ParserRegistrator
import json


_FEELINGS_FILENAME = 'feelings.json'


@ParserRegistrator.register('feelings',)
class FeelingsParser(AbstractParser):
    @staticmethod
    def parse(context: ParserContext):
        path = context.get_savepath(_FEELINGS_FILENAME)
        hunger, thirst, exhaustion, happiness = context.snapshot.feelings
        data = {'hunger': hunger,
                'thirst': thirst,
                'exhaustion': exhaustion,
                'happiness': happiness}
        with path.open('w') as outfile:
            json.dump(data, outfile)
