import click
from .utils import Connection
from . import run_server
from . import run_webserver
from . import upload_thought


@click.group()
def main(**kwargs):
    pass


@main.command(short_help='IP:PORT  DATA_DIR')
@click.argument('address')
@click.argument('data')
def start_server(address, data):
    ip, port = address.split(':')
    try:
        run_server((ip, int(port)), data)
    except KeyboardInterrupt:
        return
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@main.command(short_help='IP:PORT  DATA_DIR')
@click.argument('address')
@click.argument('data')
def start_webserver(address, data):
    ip, port = address.split(':')
    try:
        run_webserver((ip, int(port)), data)
    except KeyboardInterrupt:
        return
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


@main.command(short_help='IP:PORT  USER_ID  THOUGHT')
@click.argument('address')
@click.argument('user')
@click.argument('thought')
def upload(address, user, thought):
    ip, port = address.split(':')
    try:
        with Connection.connect(ip, int(port)) as connection:
            upload_thought(connection, int(user), thought)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    main(prog_name='thought-process')
