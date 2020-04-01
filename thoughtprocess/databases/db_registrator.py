from furl import furl
import importlib
import pathlib

class DatabaseRegistrator:
    dbs = {}

    @classmethod
    def register(cls, name):
        def decorator(db_cls):
            cls.dbs[name] = db_cls
            return db_cls
        return decorator

    @staticmethod
    def load_dbs():
        cur_module = pathlib.Path(__file__)
        root = cur_module.parent
        for path in root.iterdir():
            if path.name == cur_module.name:
                continue
            if path.name.startswith('db_'):
                package = f'{root.parent.name}.{root.name}'
                importlib.import_module(f'.{path.stem}', package=package)

    @classmethod
    def get_db(cls, url, create_tables=False):
        f = furl(url)
        db_name = f.scheme
        if db_name not in cls.dbs:
            raise KeyError(f"Database '{db_name}' was not found")
        db_class = cls.dbs[db_name]
        return db_class(url, create_tables)