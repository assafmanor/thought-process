import json

from .parser_registrator import ParserRegistrator


def get_parser(name):
    parsers = ParserRegistrator.parsers
    if name not in parsers:
        raise NameError(f"no parser called '{name}' was found")
    return parsers[name]


def run_parser(name, data: dict):
    ParserRegistrator.load_parsers()
    parser = get_parser(name)
    return parser.parse(data)