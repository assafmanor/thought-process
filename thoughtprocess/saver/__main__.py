import click
import json
import sys
import threading

from .saver import Saver
from ..databases import DBConnectionError, UserInfoError
from ..message_queues import MessageQueueRegistrator as MQHandler
from ..message_queues import MQConnectionError
from ..utils.cli_utils import DEFAULT_DB_URL


_PARSER_NAMES = {'color_image', 'depth_image', 'feelings', 'pose'}


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='save')
@click.option('-d', '--database', default=DEFAULT_DB_URL, type=click.STRING)
@click.argument('parser_name', type=click.STRING)
@click.argument('data_file', type=click.File('r'))
def cli_save(database, parser_name, data_file):
    if parser_name not in _PARSER_NAMES:
        print(f"Parser error: parser '{parser_name}' was not found.", file=sys.stderr)
        sys.exit(1)
    saver = _init_saver(database)
    if saver is None:
        sys.exit(1)
    data = json.loads(data_file.read())
    try:
        saver.save(parser_name, data)
        print(f">> '{parser_name}' data from '{data_file.name}'", end=' ')
        print('was successfully saved to database.')
    except UserInfoError as e:
        print(f'User info error: {e}.', file=sys.stderr)
        sys.exit(1)


@cli.command(name='run-saver')
@click.option('-d', '--database', default=DEFAULT_DB_URL, type=click.STRING)
@click.argument('mq_url', type=click.STRING)
def cli_run_saver(database, mq_url):
    saver = _init_saver(database)
    if saver is None:
        print("Error: saver could not be initialized", file=sys.stderr)
        sys.exit(1)
    try:
        mq = _init_mq(mq_url)
    except MQConnectionError as e:
        print(f'MQ connection error: {e}.', file=sys.stderr)
        sys.exit(1)
    for queue_name in _PARSER_NAMES:
        print(f">> Subscribing to queue '{queue_name}'")
        _subscribe_to_queue(mq, saver, queue_name)
    mq.start_consuming()
    print('>> Waiting for data...')


def _init_saver(url):
    try:
        saver = Saver(url)
    except KeyError as e:
        print(f'Key error: {e}.', file=sys.stderr)
        sys.exit(1)
    except DBConnectionError as e:
        print(f'DB connection error: {e}.', file=sys.stderr)
        sys.exit(1)
    print('>> Connected to database.')
    return saver


def _init_mq(url):
    MQHandler.load_mqs()
    return MQHandler.get_mq(url)


def _subscribe_to_queue(mq, saver, name):
    mq.declare_queue(name)
    callback = lambda message: _callback(saver, name, message)
    mq.consume_queue(name, callback)


def _callback(saver, parser_name, data_json):
    print(f">> Received '{parser_name}' data from queue.")
    print('>> Saving data in database...')
    data = json.loads(data_json)
    try:
        saver.save(parser_name, data)
        print('>> Done!')
    except UserInfoError as e:
        print(f'User info error: {e}.', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    cli(prog_name='saver')