class AbstractMQ:
    @classmethod
    def connect(cls, host, port):
        raise NotImplementedError

    def declare_queue(self, name):
        raise NotImplementedError

    def declare_exchange(self, name):
        raise NotImplementedError

    def consume_queue(self, name, callback):
        raise NotImplementedError

    def consume_exchange(self, name, callback):
        raise NotImplementedError

    def start_consuming(self):
        raise NotImplementedError

    def publish(self, message, exchange_name, queue_name):
        raise NotImplementedError