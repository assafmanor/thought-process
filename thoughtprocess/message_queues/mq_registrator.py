from furl import furl
import importlib
import pathlib




class MessageQueueRegistrator:
    mqs = {}

    @classmethod
    def register(cls, name):
        def decorator(mq):
            cls.mqs[name] = mq
            return mq
        return decorator

    @staticmethod
    def load_mqs():
        cur_module = pathlib.Path(__file__)
        root = cur_module.parent
        mqs_count = 0
        for path in root.iterdir():
            if path.name == cur_module.name:
                continue
            if path.name.startswith('mq_'):
                package = f'{root.parent.name}.{root.name}'
                importlib.import_module(f'.{path.stem}', package=package)
                mqs_count += 1
        if mqs_count == 0:
            raise ModuleNotFoundError('No message queues available')

    @classmethod
    def get_mq(cls, url):
        f = furl(url)
        mq_name = f.scheme
        if mq_name not in cls.mqs:
            raise KeyError(f"Message queue '{mq_name}' was not found")
        mq_class = cls.mqs[mq_name]
        host = f.host
        port = f.port
        return mq_class.connect(host, port)
