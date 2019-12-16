import click
from .utils import Connection
from .utils import is_address_valid
from . import run_server
from . import run_webserver
from . import Reader
from . import upload_snapshot


ARG_FORMAT_ERROR = 'arguments are not in the correct format.'


class ArgError(Exception):
    pass


@click.group()
def main(**kwargs):
    pass


@main.command(short_help='IP:PORT  DATA_DIR')
@click.argument('address')
@click.argument('data')
def start_server(address, data):
    try:
        if not is_address_valid(address):
            raise ArgError
        ip, port = address.split(':')
        run_server((ip, int(port)), data)
    except KeyboardInterrupt:
        return
    except ArgError:
        print(f'ERROR: {ARG_FORMAT_ERROR}')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@main.command(short_help='IP:PORT  DATA_DIR')
@click.argument('address')
@click.argument('data')
def start_webserver(address, data):
    try:
        if not is_address_valid(address):
            raise ArgError
        ip, port = address.split(':')
        run_webserver((ip, int(port)), data)
    except KeyboardInterrupt:
        return
    except ArgError:
        print(f'ERROR: {ARG_FORMAT_ERROR}')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@main.command(short_help='IP:PORT  USER_ID  THOUGHT')
@click.argument('address')
@click.argument('mindfile_addr')
def upload(address, mindfile_addr):
    try:
        if not is_address_valid(address):
            raise ArgError
        ip, port = address.split(':')
        with Reader(mindfile_addr) as reader:
            upload_snapshot((ip, int(port)), reader)
    except KeyboardInterrupt:
        return
    except ArgError:
        print(f'ERROR: {ARG_FORMAT_ERROR}')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@main.command(short_help='PATH')
@click.argument('path')
def read(path):
    try:
        with Reader(path) as reader:
            for snapshot in reader:
                print(f'{snapshot}\n')
    except KeyboardInterrupt:
        return
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    main(prog_name='thoughtprocess')
