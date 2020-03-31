import datetime as dt
import json
import pathlib

from ..message_queues import get_exchange_name
from ..message_queues import MessageQueueRegistrator as MQHandler


class AbstractParser:

    mq = None
    consumed_name = None
    publish_name = None

    @classmethod
    def parse(cls, data: dict):
        raise NotImplementedError

    @classmethod
    def get_metadata(cls, data: dict):
        return {'parser_name': cls.publish_name,
                'user_id': data['user_id'],
                'username': data['username'],
                'birthdate': data['birthdate'],
                'gender': data['gender'],
                'timestamp': data['timestamp']}

    @classmethod
    def init_mq(cls, url):
        MQHandler.load_mqs()
        cls.mq = MQHandler.get_mq(url)
        cls._init_consumed_exchange(url)
        cls._init_publish_queue()

    @classmethod
    def _init_consumed_exchange(cls, url):
        cls.consumed_name = get_exchange_name('server_exchange')
        cls.mq.declare_exchange(cls.consumed_name)
        cls.mq.consume_exchange(cls.consumed_name, cls._callback)

    @classmethod
    def _init_publish_queue(cls):
        cls.mq.declare_queue(cls.publish_name)
    
    @classmethod
    def _callback(cls, data_json):
        print(f">> Received data from exchange '{cls.consumed_name}'.")
        print('>> Parsing data...')
        data = json.loads(data_json)
        parsed_data = cls.parse(data)
        cls.mq.publish(json.dumps(parsed_data),
                       queue_name=cls.publish_name)
        print(f">> Done!\n>> Published results to queue '{cls.publish_name}'.")
        print(f'>> Parsed data: {parsed_data}')