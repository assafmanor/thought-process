import importlib
import pathlib


class ParserRegistrator:
    parsers = {}

    @classmethod
    def register(cls, name):
        def decorator(parser_cls):
            cls.parsers[name] = parser_cls
            parser_cls.publish_name = name
            return parser_cls
        return decorator

    @staticmethod
    def load_parsers():
        cur_module = pathlib.Path(__file__)
        root = cur_module.parent
        for path in root.iterdir():
            if path.name == cur_module.name:
                continue
            if path.name.startswith('parser_'):
                package = f'{root.parent.name}.{root.name}'
                importlib.import_module(f'.{path.stem}', package=package)