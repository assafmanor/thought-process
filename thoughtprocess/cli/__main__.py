import click
import json
import requests
import shutil
import sys

from ..utils.cli_utils import DEFAULT_IP, DEFAULT_API_PORT
from .utils import *

CONN_ERROR_MSG = 'Connection error: could not connect to the API server.'
BIRTHDATE_STR_FORMAT = "%Y-%m-%d"
DATETIME_STR_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
_GENDER_DICT = {'m': 'Male', 'f':'Female', 'o': 'Other'}


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='get-users')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
def get_users(host, port):
    url = f'http://{host}:{port}/users'
    try:
        users = get(url)
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG, file=sys.stderr)
        sys.exit(1)
    for user in users:
        user['gender'] = _GENDER_DICT[user['gender']]
        format_timestamp(user, 'birthdate', BIRTHDATE_STR_FORMAT)
    users.sort(key=lambda k: k['id'])
    lists = make_list_of_dicts_into_lists(users)
    print_lists_with_padding(lists)


@cli.command(name='get-user')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
@click.argument('user_id', type=click.INT)
def get_user(host, port, user_id):
    url = f'http://{host}:{port}/users/{user_id}'
    try:
        user = get(url)
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG, file=sys.stderr)
        sys.exit(1)
    user['gender'] = _GENDER_DICT[user['gender']]
    format_timestamp(user, 'birthdate', BIRTHDATE_STR_FORMAT)
    lists = make_dict_into_lists(user)
    print_lists_with_padding(lists)

@cli.command(name='get-snapshots')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
@click.argument('user_id', type=click.INT)
def get_snapshots(host, port, user_id):
    url = f'http://{host}:{port}/users/{user_id}/snapshots'
    try:
        snapshots = get(url)
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG, file=sys.stderr)
        sys.exit(1)
    for snapshot in snapshots:
        format_timestamp(snapshot, 'timestamp', DATETIME_STR_FORMAT)
    lists = make_list_of_dicts_into_lists(snapshots)
    print_lists_with_padding(lists)


@cli.command(name='get-snapshot')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_API_PORT, type=click.INT)
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
def get_snapshot(host, port, user_id, snapshot_id):
    url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}'
    try:
        snapshot = get(url)
    except requests.exceptions.ConnectionError:
        print(CONN_ERROR_MSG, file=sys.stderr)
        sys.exit(1)
    format_timestamp(snapshot, 'timestamp', DATETIME_STR_FORMAT)
    # split translation and rotation into two dictionary entries
    snapshot['translation'] = snapshot['pose']['translation']
    snapshot['rotation'] = snapshot['pose']['rotation']
    del snapshot['pose']
    print_listed_dict(snapshot)


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
        print(CONN_ERROR_MSG, file=sys.stderr)
        sys.exit(1)
    if result_name == 'pose':
        d = json.loads(result)
        keys_width = max([len(str(key)) for key in d.keys()]) + 3
        result = '\n'.join([f'{str(key).ljust(keys_width)}{val}' for key,val in d.items()])
    if not save:
        print(result)
        return
    if result_name in ['color_image', 'depth_image']:
        shutil.copy(result, save)
    else:
        with open(save, 'w') as f:
            f.write(result)
    print(f">> Result saved to '{save}'.")


def print_error_and_exit(request):
    data = request.json()
    message = data['message']
    print(f'ERROR: {message}.')
    sys.exit(0)



def get(url):
    r = requests.get(url)
    if r.status_code == 404:
        print_error_and_exit(r)
    return r.json()


if __name__ == '__main__':
    cli(prog_name='api')