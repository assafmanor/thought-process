import json

from ..databases import DatabaseRegistrator

class Saver:
    def __init__(self, db_url):
        DatabaseRegistrator.load_dbs()
        self.db = DatabaseRegistrator.get_db(
            db_url, create_tables=True)

    def save(self, parser_name, data: dict):
        # first convert data to json if needed
        parser_data = data[parser_name]
        if isinstance(parser_data, (list, dict)):
            data[parser_name] = json.dumps(parser_data)
        self.db.save_data(parser_name, data)