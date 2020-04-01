import click
import json
import pathlib
import sys
from .server import run_server
from ..utils.cli_utils import DEFAULT_IP
from ..utils.cli_utils import DEFAULT_SERVER_PORT
from ..message_queues import get_exchange_name
from ..message_queues import MessageQueueRegistrator as MQHandler


@click.group()
def cli(**kwargs):
    pass


@cli.command(name='run-server')
@click.option('-h', '--host', default=DEFAULT_IP, type=click.STRING)
@click.option('-p', '--port', default=DEFAULT_SERVER_PORT, type=click.INT)
@click.argument('url', type=click.STRING)
def cli_run_server(host, port, url):
    callback = lambda message: _callback(url, message)
    run_server(host, port, callback)


def _callback(url, message):
    if not hasattr(_callback, 'initialized'):
        _callback.initialized = False
    if not _callback.initialized:
        _callback.exchange_name = get_exchange_name('server_exchange')
        _callback.mq = _init_mq(url, _callback.exchange_name)
        _callback.initialized = True
    _callback.mq.publish(message, exchange_name=_callback.exchange_name)


def _init_mq(url, exchange_name):
    try:
        MQHandler.load_mqs()
        mq = MQHandler.get_mq(url)
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        return 1
    mq.declare_exchange(exchange_name)
    return mq


if __name__ == '__main__':
    cli(prog_name='server')
