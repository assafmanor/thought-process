from thoughtprocess.databases.db_registrator import DatabaseRegistrator
from thoughtprocess.databases.db_postgres import PostgresDB
import pytest


def test_load_db():
    DatabaseRegistrator.load_dbs()
    dbs = DatabaseRegistrator.dbs
    assert len(dbs) == 1
    assert 'postgresql' in dbs.keys()
    assert dbs['postgresql'] == PostgresDB