class AbstractDB:
    @classmethod
    def connect(cls, url):
        raise NotImplementedError

    def save_data(self, parser_name, data: dict):
        raise NotImplementedError

    def save_user(self, data: dict):
        raise NotImplementedError

    def get_users(self):
        raise NotImplementedError

    def get_user(self, user_id):
        raise NotImplementedError

    def get_user_snapshots(self, user_id):
        raise NotImplementedError

    def get_snapshot(self, user_id, snapshot_id):
        raise NotImplementedError

    def get_data(self, user_id, snapshot_id, result_name):
        raise NotImplementedError