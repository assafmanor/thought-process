from ..databases import DatabaseRegistrator
from ..utils.cli_utils import DEFAULT_IP, DEFAULT_API_PORT
from ..utils.cli_utils import DEFAULT_DB_URL
from .api import RestfulApi

def run_api_server(host=DEFAULT_IP, port=DEFAULT_API_PORT, database_url=DEFAULT_DB_URL):
    DatabaseRegistrator.load_dbs()
    db = DatabaseRegistrator.get_db(database_url)
    RestfulApi.run(db, host, port)