import click
import json
import threading

from .saver import Saver
from ..databases import DBConnectionError
from ..message_queues import MessageQueueRegistrator as MQHandler

_DEFAULT_DB_URL = 'postgresql://postgres:password@127.0.0.1:5432/postgres'
_PARSER_NAMES = {'color_image', 'depth_image', 'feelings', 'pose'}


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='save')
@click.option('-d', '--database', default=_DEFAULT_DB_URL, type=click.STRING)
@click.argument('parser_name', type=click.STRING)
@click.argument('data_file', type=click.File('r'))
def cli_save(database, parser_name, data_file):
    if parser_name not in _PARSER_NAMES:
        print(f"Parser error: parser '{parser_name}' was not found.")
        return
    saver = _init_saver(database)
    if saver is None:
        return
    data = json.loads(data_file.read())
    saver.save(parser_name, data)
    print(f">> '{parser_name}' data from '{data_file.name}'", end=' ')
    print('was successfully saved to database.')

    


@cli.command(name='run-saver')
@click.argument('db_url', type=click.STRING)
@click.argument('mq_url', type=click.STRING)
def cli_run_saver(db_url, mq_url):
    saver = _init_saver(db_url)
    if saver is None:
        return
    mq = _init_mq(mq_url)
    for queue_name in _PARSER_NAMES:
        print(f">> Subscribing to queue '{queue_name}'")
        _subscribe_to_queue(mq, saver, queue_name)
    mq.start_consuming()
    print('>> Waiting for data...')

def _init_saver(url):
    try:
        saver = Saver(url)
    except KeyError as e:
        print(f'Key error: {e}.')
        return None
    except DBConnectionError as e:
        print(f'DB connection error: {e}.')
        return None
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
    saver.save(parser_name, data)
    print('>> Done!')


if __name__ == '__main__':
    cli(prog_name='saver')