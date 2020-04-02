import click
import json
import requests
import shutil

from ..utils.cli_utils import DEFAULT_IP, DEFAULT_API_PORT


CONN_ERROR_MSG = 'Connection error: could not connect to the API server.'


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='get-users')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
def get_users(host, port):
    url = f'http://{host}:{port}/users'
    try:
        print(get(url))
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG)
        return


@cli.command(name='get-user')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
@click.argument('user_id', type=click.INT)
def get_user(host, port, user_id):
    url = f'http://{host}:{port}/users/{user_id}'
    try:
        print(get(url))
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG)
        return

@cli.command(name='get-snapshots')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
@click.argument('user_id', type=click.INT)
def get_snapshots(host, port, user_id):
    url = f'http://{host}:{port}/users/{user_id}/snapshots'
    try:
        print(get(url))
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG)
        return


@cli.command(name='get-snapshot')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
def get_snapshot(host, port, user_id, snapshot_id):
    url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}'
    try:
        print(get(url))
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG)
        return

@cli.command(name='get-result')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
@click.option('-s', '--save', default=None, type=click.Path())
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
@click.argument('result_name', type=click.STRING)
def get_result(host, port, user_id, snapshot_id, result_name, save):
    url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}'
    try:
        result = get(url)
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG)
        return
    if not save:
        print(result)
        return
    if result_name in ['color_image', 'depth_image']:
        shutil.copy(result, save)
    else:
        with open(save, 'w') as f:
            f.write(result)
    print(f">> Result saved to '{save}'.")


def get_error_message(request):
    data = request.json()
    message = data['message']
    return f'ERROR: {message}.'


def get(url):
    r = requests.get(url)
    if r.status_code == 404:
        return(get_error_message(r))
    return r.json()


if __name__ == '__main__':
    cli(prog_name='api')