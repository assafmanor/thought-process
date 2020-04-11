import click
import requests
import sys

from ..utils.cli_utils import DEFAULT_IP, DEFAULT_API_PORT, DEFAULT_GUI_PORT
from .web import run_server

CONN_ERROR_MSG = 'Connection error: could not connect to the API server.'


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='run-server')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_GUI_PORT, type=click.INT)
@click.option('-H', '--api-host', default=DEFAULT_IP, type=click.STRING)
@click.option('-P', '--api-port', default=DEFAULT_API_PORT, type=click.INT)
def get_user(host, port, api_host, api_port):
    api_url = f'http://{api_host}:{api_port}'
    try:
        requests.get(api_url)
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG, file=sys.stderr)
        sys.exit(1)
    run_server(host, port, api_host, api_port)


if __name__ == '__main__':
    cli(prog_name='gui')