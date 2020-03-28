import datetime as dt
import json
import pathlib


_RESULTS_PATH = '/tmp/thoughtprocess/data/images/'
_DATETIME_FILE_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'
_COLOR_IMAGE_FILENAME = 'color_image.bin'
_DEPTH_IMAGE_FILENAME = 'depth_image.bin'



class ThoughtContext:
    def __init__(self, user, snapshot):
        self.user = user
        self.snapshot = snapshot

    def get_savedir(self):
        timestamp_ms = self.snapshot.timestamp_ms
        user_id = self.user.user_id
        datetime = dt.datetime.fromtimestamp(timestamp_ms/1000.0)
        # show only four digits in microseconds
        dt_format = datetime.strftime(_DATETIME_FILE_FORMAT)[:-2]
        return pathlib.Path(_RESULTS_PATH) / str(user_id) / dt_format


    def get_savepath(self, filename):
        sdir = self.get_savedir()
        path = sdir / filename
        return path


    def get_json(self):
        user = self.user
        snapshot = self.snapshot
        cimg_w, cimg_h, cimg_data = snapshot.color_image
        dimg_w, dimg_h, dimg_data = snapshot.depth_image
        cimg_path = self.get_savepath(_COLOR_IMAGE_FILENAME)
        dimg_path = self.get_savepath(_DEPTH_IMAGE_FILENAME)
        savedir = self.get_savedir()
        _save_raw_data(savedir, _COLOR_IMAGE_FILENAME, cimg_data)
        _save_raw_data(savedir, _DEPTH_IMAGE_FILENAME, dimg_data)
        data = {'user_id': user.user_id,
                'username': user.username,
                'birthdate': user.birthdate.timestamp(),
                'gender': user.gender,
                'timestamp': snapshot.timestamp_ms,
                'translation': snapshot.translation,
                'rotation': snapshot.rotation,
                'color_image': [cimg_w, cimg_h, str(cimg_path)],
                'depth_image': [dimg_w, dimg_h, str(dimg_path)],
                'feelings': snapshot.feelings}
        return json.dumps(data)


def _save_raw_data(dirpath, filename, data):
    dirpath.mkdir(parents=True, exist_ok=True)
    path = dirpath / filename
    with open(path, 'wb') as f:
        f.write(data)
