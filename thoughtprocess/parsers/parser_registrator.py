import inspect
import importlib
import pathlib


_TRANSLATION_FILE_NAME = 'translation.json'
_COLOR_IMAGE_FILE_NAME = 'color_image.jpg'
_DATETIME_FILE_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'


class ParserRegistrator:
    parsers = set()
    fields = set()

    @classmethod
    def register(cls, *names):
        cls.fields.update(names)

        def decorator(obj):
            if inspect.isclass(obj):
                parser = obj.parse
            elif inspect.isfunction(obj):
                parser = obj
            else:
                raise ValueError
            cls.parsers.add(parser)
            return obj
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


ParserRegistrator.load_parsers()
