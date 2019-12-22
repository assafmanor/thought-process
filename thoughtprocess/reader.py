class Reader:
    def __init__(self, path, reader_cls):
        self.reader = reader_cls(path)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.reader})"

    def __iter__(self):
        return self

    def __next__(self):
        return self.reader.next_snapshot()

    def __enter__(self):
        self.reader.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reader.stop()

    def get_info(self):
        return self.reader.hello