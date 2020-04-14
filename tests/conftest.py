import pathlib
import os
import sys

from thoughtprocess.client import upload_sample
from thoughtprocess.readers.reader_protobuf import ProtobufReader
from thoughtprocess.readers.cognition import Cognition

import pytest


_SAMPLE_PATH = pathlib.Path(__file__).absolute().parent / 'files/test_sample.mind.gz'


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def cognition():
    try:
        cognition = Cognition(_SAMPLE_PATH, ProtobufReader)
        cognition.reader.start()
        yield cognition
    finally:
        cognition.reader.stop()