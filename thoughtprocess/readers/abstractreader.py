import pathlib


class AbstractReader:
    def __init__(self, path_str):
        self.path = pathlib.Path(path_str)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.path.absolute()}')"

    def __str__(self):
        return self.__class__.__name__

    def start(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError

    def next_snapshot(self):
        raise NotImplementedError
