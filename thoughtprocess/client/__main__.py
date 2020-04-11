import click
from .client import upload_sample
from ..utils.cli_utils import DEFAULT_IP
from ..utils.cli_utils import DEFAULT_SERVER_PORT

import sys


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='upload-sample')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_SERVER_PORT, type=click.INT)
@click.argument('path', type=click.Path(exists=True))
def upload(host, port, path):
    try:
        upload_sample(host, port, path)
    except Exception as e:
        print(f'ERROR: failed to upload snapshot: {e}.', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    cli(prog_name='client')
