class ReaderRegistrator:
    readers = dict()

    @staticmethod
    def register(name):
        def decorator(cls):
            ReaderRegistrator.readers[name] = cls
            return cls
        return decorator