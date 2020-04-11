import click
import json
import pathlib
import sys

from .server import run_server
from ..utils.cli_utils import DEFAULT_IP
from ..utils.cli_utils import DEFAULT_SERVER_PORT
from ..message_queues import get_exchange_name
from ..message_queues import MessageQueueRegistrator as MQHandler
from ..message_queues import MQConnectionError


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='run-server')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_SERVER_PORT, type=click.INT)
@click.argument('url', type=click.STRING)
def cli_run_server(host, port, url):
    mq = _init_mq(url, get_exchange_name('server_exchange'))
    callback = lambda message: _callback(url, message, mq)
    try:
        run_server(host, port, callback)
    except ConnectionAbortedError as e:
        print(f'Connection lost: {e}.')
        sys.exit(1)


def _callback(url, message, mq):
    mq.publish(message,
               exchange_name=get_exchange_name('server_exchange'))


def _init_mq(url, exchange_name):
    try:
        MQHandler.load_mqs()
    except ModuleNotFoundError as e:
        print(f'MQ error: {e}.', file=sys.stderr)
        sys.exit(1)
    try:
        mq = MQHandler.get_mq(url)
    except KeyError as e:
        print(f'Key error: {e}.', file=sys.stderr)
        sys.exit(1)
    except MQConnectionError as e:
        print(f'MQ connection error: {e}.', file=sys.stderr)
        sys.exit(1)
    mq.declare_exchange(exchange_name)
    return mq


if __name__ == '__main__':
    cli(prog_name='server')
