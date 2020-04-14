from datetime import datetime

import pytest


def test_user(cognition):
    user = cognition.get_info()
    assert user.user_id == 420
    assert user.username == 'Assaf Manor'
    assert user.gender == 'm'
    assert user.birthdate == datetime(1993, 11, 10)


def test_snapshot(cognition):
    snapshot = cognition.__next__()
    assert snapshot.timestamp_ms == 1586784399663
    assert snapshot.translation == (1.00000000001, 2.000000000002, 3.0000003)
    assert snapshot.rotation == (4.000000004, 5.00000005, 6.00000006, 7.000000007)
    assert snapshot.feelings == (-0.5, 0.0, 0.5, 1.0)
    assert snapshot.color_image == (0, 0, b'')
    assert snapshot.depth_image == (0, 0, [])
