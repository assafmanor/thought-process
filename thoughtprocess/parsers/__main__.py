import click
import json
import pathlib

from .parser_registrator import ParserRegistrator
from .utils import run_parser, get_parser

@click.group()
def cli(**kwargs):
    pass


@cli.command(name='parse')
@click.argument('parser_name', type=click.STRING)
@click.argument('data_path', type=click.STRING)
def cli_parse(parser_name, data_path):
    path = pathlib.Path(data_path)
    if not path.is_file():
        print(f'File error: invalid path was provided.')
        return 1
    with open(data_path, 'r') as f:
        try:
            data = json.loads(f.read())
        except ValueError:
            print(f'Value error: invalid file format.')
            return 1
    try:
        parsed_result = run_parser(parser_name, data)
    except NameError as e:
        print(f'Name error: {e}.')
        return 1
    print(f"Parsed {parser_name} from '{data_path}'.")
    print(f'Parsing result:\n{parsed_result}')


@cli.command(name='run-parser')
@click.argument('parser_name', type=click.STRING)
@click.argument('mq_url', type=click.STRING)
def cli_run_parser(parser_name, mq_url):
    try:
        ParserRegistrator.load_parsers()
    except NameError as e:
        print(f'Name error: {e}.')
        return 1
    print(f"Parser '{parser_name}' was successfully loaded!")
    try:
        parser = get_parser(parser_name)
    except NameError as e:
        print(f'Name error: {e}.')
        return 1
    try:
        parser.init_mq(mq_url)
    except KeyError as e:
        print(f'Key error: {e}.')
        return 1


if __name__ == '__main__':
    cli(prog_name='parsers')
