import click
from .utils import get_address_tuple
from .utils import is_address_valid
from . import Reader
from . import run_server
from . import run_webserver
from . import upload_snapshot


ARG_FORMAT_ERROR = 'arguments are not in the correct format.'

_DEFAULT_ADDRESS = ('0.0.0.0', 8000)


class ArgError(Exception):
    pass


@click.group()
def main(**kwargs):
    pass


@main.group()
def server():
    pass


@main.group()
def client():
    pass


@server.command(name='run', short_help='IP:PORT  DATA_DIR')
@click.option('-a', '--address')
@click.argument('data')
def start_server(address, data):
    try:
        if address is None:
            address_tup = _DEFAULT_ADDRESS
        elif not is_address_valid(address):
            raise ArgError
        else:
            address_tup = get_address_tuple(address)
        run_server(address_tup, data)
    except KeyboardInterrupt:
        return
    except ArgError:
        print(f'ERROR: {ARG_FORMAT_ERROR}')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@client.command(name='run', short_help='IP:PORT  FILE_ADDR')
@click.option('-a', '--address')
@click.argument('mindfile_addr')
def upload(address, mindfile_addr):
    try:
        if address is None:
            address_tup = _DEFAULT_ADDRESS
        elif not is_address_valid(address):
            raise ArgError
        else:
            address_tup = get_address_tuple(address)
        with Reader(mindfile_addr) as reader:
            upload_snapshot(address_tup, reader)
    except KeyboardInterrupt:
        return
    except ArgError:
        print(f'ERROR: {ARG_FORMAT_ERROR}')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@main.command(short_help='IP:PORT  DATA_DIR')
@click.option('-a', '--address')
@click.argument('data')
def start_webserver(address, data):
    try:
        if address is None:
            address_tup = _DEFAULT_ADDRESS
        elif not is_address_valid(address):
            raise ArgError
        else:
            address_tup = get_address_tuple(address)
        run_webserver(address_tup, data)
    except KeyboardInterrupt:
        return
    except ArgError:
        print(f'ERROR: {ARG_FORMAT_ERROR}')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@main.command(short_help='FILE_ADDR')
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
