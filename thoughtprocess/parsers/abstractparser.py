import datetime as dt
import pathlib


_DATETIME_FILE_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'


class ParserContext:
    def __init__(self, data_dir, user, snapshot):
        self.data_dir = data_dir
        self.user = user
        self.snapshot = snapshot

    def get_savepath(self, filename):
        sdir = _get_save_dir(self.data_dir,
                             self.user.user_id,
                             self.snapshot.timestamp_ms)
        _create_dir(sdir)
        path = sdir / filename
        return path


class AbstractParser:
    @staticmethod
    def parse(context: ParserContext):
        raise NotImplementedError


def _get_save_dir(data_dir, user_id, timestamp_ms):
    datetime = dt.datetime.fromtimestamp(timestamp_ms/1000.0)
    # show only four digits in microseconds
    dt_format = datetime.strftime(_DATETIME_FILE_FORMAT)[:-2]
    return pathlib.Path(data_dir) / str(user_id) / dt_format


def _create_dir(dir_path):
    dir_path.mkdir(parents=True, exist_ok=True)
