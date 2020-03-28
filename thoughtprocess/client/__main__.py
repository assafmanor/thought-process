import click
from .client import upload_sample
from ..utils.cli_utils import DEFAULT_IP
from ..utils.cli_utils import DEFAULT_PORT


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='upload-sample')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_PORT, type=click.INT)
@click.argument('path', type=click.Path(exists=True))
def upload(host, port, path):
    upload_sample(host, port, path)


if __name__ == '__main__':
    cli(prog_name='client')
