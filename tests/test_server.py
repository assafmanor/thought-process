from thoughtprocess.thoughts import ThoughtContext
from thoughtprocess.utils import Snapshot

from datetime import datetime
import json
import pathlib

import pytest


_SAVE_DIR = '.data/images/420/2020-04-13_16-26-39-6630'
_COLOR_IMAGE_PATH = f'{_SAVE_DIR}/color_image.bin'
_DEPTH_IMAGE_PATH = f'{_SAVE_DIR}/depth_image.bin'


@pytest.fixture
def context(cognition):
    user = cognition.get_info()
    snapshot = cognition.__next__()
    return ThoughtContext(user, snapshot)


def test_save_dir(context):
    assert context.get_savedir() == pathlib.Path(_SAVE_DIR)


def test_context_json(context):
    ctx_json = context.get_json()
    data = json.loads(ctx_json)
    assert data['user_id'] == 420
    assert data['username'] == 'Assaf Manor'
    assert data['gender'] == 'm'
    assert data['birthdate'] == datetime(1993, 11, 10).timestamp()
    assert data['timestamp'] == 1586784399663
    assert data['translation'] == [1.00000000001, 2.000000000002, 3.0000003]
    assert data['rotation'] == [4.000000004, 5.00000005, 6.00000006, 7.000000007]
    assert data['feelings'] == [-0.5, 0.0, 0.5, 1.0]
    assert data['color_image'] == [0, 0, _COLOR_IMAGE_PATH]
    assert data['depth_image'] == [0, 0, _DEPTH_IMAGE_PATH]