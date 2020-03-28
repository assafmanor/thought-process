import json
import pathlib

def get_exchange_name(exchange_key):
    path = pathlib.Path(__file__).parent / 'topics.json'
    with path.open('r') as f:
        data = f.read()
    topic_names = json.loads(data)
    return topic_names[exchange_key]