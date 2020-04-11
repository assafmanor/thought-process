import click
import sys

from .run_api_server import run_api_server
from ..databases import DBConnectionError
from ..utils.cli_utils import DEFAULT_IP, DEFAULT_API_PORT
from ..utils.cli_utils import DEFAULT_DB_URL


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='run-server')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
@click.option('-d', '--database', default=DEFAULT_DB_URL, type=click.STRING)
def cli_run_api_server(host, port, database):
    try:
        run_api_server(host, port, database)
    except KeyError as e:
        print(f'Key error: {e}.', file=sys.stderr)
        sys.exit(1)
    except DBConnectionError as e:
        print(f'DB connection error: {e}.', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    cli(prog_name='api')