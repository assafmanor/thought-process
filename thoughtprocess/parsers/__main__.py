import click
import json
import pathlib
import sys

from .parser_registrator import ParserRegistrator
from .utils import run_parser, get_parser
from ..message_queues import MQConnectionError

@click.group()
def cli(**kwargs):
    pass


@cli.command(name='parse')
@click.argument('parser_name', type=click.STRING)
@click.argument('data_file', type=click.File('r'))
def cli_parse(parser_name, data_file):
    try:
        data = json.loads(data_file.read())
    except ValueError:
        print(f'Value error: invalid file format.')
        sys.exit(1)
    try:
        parsed_result = run_parser(parser_name, data)
    except NameError as e:
        print(f'Name error: {e}.')
        sys.exit(1)
    print(f"Parsed {parser_name} from '{data_file.name}'.")
    print(f'Parsing result:\n{parsed_result}')


@cli.command(name='run-parser')
@click.argument('parser_name', type=click.STRING)
@click.argument('mq_url', type=click.STRING)
def cli_run_parser(parser_name, mq_url):
    try:
        ParserRegistrator.load_parsers()
    except NameError as e:
        print(f'Name error: {e}.')
        sys.exit(1)
    print(f"Parser '{parser_name}' was successfully loaded!")
    try:
        parser = get_parser(parser_name)
    except NameError as e:
        print(f'Name error: {e}.')
        sys.exit(1)
    try:
        parser.init_mq(mq_url)
    except KeyError as e:
        print(f'Key error: {e}.')
        sys.exit(1)
    except MQConnectionError as e:
        print(f'MQ connection error: {e}.')
        sys.exit(1)


if __name__ == '__main__':
    cli(prog_name='parsers')
