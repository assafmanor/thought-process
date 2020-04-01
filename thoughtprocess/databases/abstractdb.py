class AbstractDB:
    def __init__(self, url, create_tables=False):
        raise NotImplementedError

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def connect(self, url):
        raise NotImplementedError

    def save_data(self, req_data_name, data: dict):
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