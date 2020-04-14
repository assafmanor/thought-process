from datetime import datetime
import pathlib
import shutil

from thoughtprocess.parsers.abstractparser import AbstractParser
from thoughtprocess.parsers.parser_registrator import ParserRegistrator
from thoughtprocess.parsers.utils import get_parser as get_parser_func

import pytest

_FILES_PATH = pathlib.Path(__file__).parent / 'files'
_COLOR_IMAGE_BIN_PATH = _FILES_PATH / 'color_image.bin'
_COLOR_IMAGE_BIN_TEMP_PATH = _FILES_PATH / '_color_image.bin'
_DEPTH_IMAGE_BIN_PATH = _FILES_PATH / 'depth_image.bin'
_DEPTH_IMAGE_BIN_TEMP_PATH = _FILES_PATH / '_depth_image.bin'
_COLOR_IMAGE_PATH = _FILES_PATH / 'color_image.jpg'
_DEPTH_IMAGE_PATH = _FILES_PATH / 'depth_image.jpg'

@pytest.fixture
def get_parser():
    ParserRegistrator.load_parsers()
    return get_parser_func


@pytest.fixture
def get_data():
    def data_with_parser(Parser):
        return {'parser_name': Parser.publish_name,
                'user_id': 420,
                'username': 'Assaf Manor',
                'birthdate': datetime(1993, 11, 10).timestamp(),
                'gender': 'm',
                'timestamp': 1586784399663,
                'translation': [1.00000000001, 2.000000000002, 3.0000003],
                'rotation': [4.000000004, 5.00000005, 6.00000006, 7.000000007],
                'feelings': [-0.5, 0.0, 0.5, 1.0],
                'color_image': [1920, 1080, str(_COLOR_IMAGE_BIN_TEMP_PATH)],
                'depth_image': [224, 172, str(_DEPTH_IMAGE_BIN_TEMP_PATH)]}
    return data_with_parser


def test_metadata(get_parser, get_data):
    Parser = get_parser('pose')
    data = get_data(Parser)
    parsed_data = Parser.parse(data)
    assert parsed_data['parser_name'] == 'pose'
    assert parsed_data['user_id'] == 420
    assert parsed_data['username'] == 'Assaf Manor'
    assert parsed_data['birthdate'] == datetime(1993, 11, 10).timestamp()
    assert parsed_data['gender'] == 'm'
    assert parsed_data['timestamp'] == 1586784399663


def test_parser_pose(get_parser, get_data):
    Parser = get_parser('pose')
    data = get_data(Parser)
    parsed_data = Parser.parse(data)
    translation = parsed_data['pose']['translation']
    rotation = parsed_data['pose']['rotation']
    assert translation == [1.00000000001, 2.000000000002, 3.0000003]
    assert rotation == [4.000000004, 5.00000005, 6.00000006, 7.000000007]


def test_parser_color_image(get_parser, get_data):
    Parser = get_parser('color_image')
    data = get_data(Parser)
    shutil.copy(_COLOR_IMAGE_BIN_PATH, _COLOR_IMAGE_BIN_TEMP_PATH)
    parsed_data = Parser.parse(data)
    assert parsed_data['color_image'] == str(_COLOR_IMAGE_PATH)
    assert _COLOR_IMAGE_BIN_TEMP_PATH.exists() == False
    assert _COLOR_IMAGE_PATH.exists()
    _COLOR_IMAGE_PATH.unlink()


def test_parser_depth_image(get_parser, get_data):
    Parser = get_parser('depth_image')
    data = get_data(Parser)
    shutil.copy(_DEPTH_IMAGE_BIN_PATH, _DEPTH_IMAGE_BIN_TEMP_PATH)
    parsed_data = Parser.parse(data)
    assert parsed_data['depth_image'] == str(_DEPTH_IMAGE_PATH)
    assert _DEPTH_IMAGE_BIN_TEMP_PATH.exists() == False
    assert _DEPTH_IMAGE_PATH.exists()
    _DEPTH_IMAGE_PATH.unlink()


def test_parser_feelings(get_parser, get_data):
    Parser = get_parser('feelings')
    data = get_data(Parser)
    parsed_data = Parser.parse(data)
    assert parsed_data['feelings'] == [-0.5, 0.0, 0.5, 1.0]
