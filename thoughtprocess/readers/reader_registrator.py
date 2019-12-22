import importlib
import pathlib


class ReaderRegistrator:
    readers = dict()

    @staticmethod
    def register(name):
        def decorator(cls):
            ReaderRegistrator.readers[name] = cls
            return cls
        return decorator

    @staticmethod
    def load_readers():
        cur_module = pathlib.Path(__file__)
        root = cur_module.parent
        for path in root.iterdir():
            if path.name == cur_module.name:
                continue
            if path.name.startswith('reader_'):
                package = f'{root.parent.name}.{root.name}'
                importlib.import_module(f'.{path.stem}', package=package)


ReaderRegistrator.load_readers()
