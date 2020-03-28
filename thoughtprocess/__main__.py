import click
from . import run_server
from . import run_webserver
#from .client import upload_snapshot
from .readers import ReaderRegistrator
from .utils import get_address_tuple, is_address_valid


ARG_FORMAT_ERROR = 'arguments are not in the correct format.'
INVALID_READER_CLASS_ERROR = 'Invalid reader class.\nValid types: {readers}'


_DEFAULT_ADDRESS = '0.0.0.0:8000'


readers = ReaderRegistrator.readers


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
    client.add_command(upload, name='run')


@server.command(name='run', short_help="<DATA_DIR>")
@click.option('-a', '--address', default=_DEFAULT_ADDRESS,
              metavar='', help='<IP:PORT> or <PORT>')
@click.argument('data')
def start_server(address, data):
    try:
        if not is_address_valid(address):
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

'''
@client.command(name='run', short_help="<FILE_ADDR>")
@click.option('-a', '--address', default=_DEFAULT_ADDRESS,
              metavar='', help='<IP:PORT> or <PORT>')
@click.option('-r', '--reader-str', type=click.STRING, default='protobuf',
              metavar='', help="'protobuf' or 'binary'")
@click.argument('mindfile_path', type=click.Path(exists=True))
def upload(address, mindfile_path, reader_str):
    reader_str = reader_str.lower()
    if reader_str not in readers:
        error_msg = INVALID_READER_CLASS_ERROR.format(readers=tuple(readers))
        print(f'ERROR: {error_msg}')
        return 1
    reader_cls = readers[reader_str]
    try:
        if not is_address_valid(address):
            raise ArgError
        else:
            address_tup = get_address_tuple(address)
        with Reader(mindfile_path, reader_cls) as reader:
            upload_snapshot(address_tup, reader)
    except KeyboardInterrupt:
        return
    except ArgError:
        print(f'ERROR: {ARG_FORMAT_ERROR}')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1
'''

@main.command(short_help="<DATA_DIR>")
@click.option('-a', '--address', default=_DEFAULT_ADDRESS,
              metavar='', help='<IP:PORT> or <PORT>')
@click.argument('data')
def start_webserver(address, data):
    try:
        if not is_address_valid(address):
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


'''
@main.command(short_help='<FILE_ADDR>')
@click.option('-r', '--reader_str', type=click.STRING, default='protobuf',
              metavar='', help="'protobuf' or 'binary'")
@click.argument('path')
def read(path, reader_str):
    reader_str = reader_str.lower()
    if reader_str not in readers:
        print(f'ERROR: \
              {INVALID_READER_CLASS_ERROR.format(readers=tuple(readers))}')
        return 1
    reader_cls = readers[reader_str]
    try:
        with Reader(path, reader_cls) as reader:
            for snapshot in reader:
                print(f'{snapshot}\n')
    except KeyboardInterrupt:
        return
    except Exception as error:
        print(f'ERROR: {error}')
        return 1
'''

if __name__ == '__main__':
    main(prog_name='thoughtprocess')
