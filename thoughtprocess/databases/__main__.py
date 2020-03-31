from .abstractdb import AbstractDB
from .db_registrator import DatabaseRegistrator
from .exceptions import DBConnectionError

#TODO: Delete this file
#postgresql://postgres:password@127.0.0.1:5432/postgres
if __name__ == '__main__':
    import sys
    url = sys.argv[1]
    DatabaseRegistrator.load_dbs()
    try:
        db = DatabaseRegistrator.get_db(url)
    except KeyError as e:
        print(f'Key error: {e}.')
        sys.exit()
    except DBConnectionError as e:
        print(f'DB connection error: {e}.')
        sys.exit()
    user = {'user_id': 42,
            'username': 'Assaf Manor',
            'gender': 'm',
            'birthdate': 1585654636}
    #db.save_user(user)
    id = 42
    data = {"user_id": 42,
            "username": "Dan Gittik",
            "birthdate": 699746400.0,
            "gender": "m",
            "timestamp": 1575446885412,
            "translation": [0.15600797533988953, 0.08133671432733536, -0.49068963527679443],
            "rotation": [-0.2959017411322204, -0.16749024140672616, -0.04752900380336424, 0.9392178514199446],
            "color_image": "/tmp/thoughtprocess/data/images/42/2019-12-04_10-08-07-4120/color_image.bin",
            "depth_image": "/tmp/thoughtprocess/data/images/42/2019-12-04_10-08-07-4120/depth_image.bin",
            "feelings": [0.0010000000474974513, 0.003000000026077032, 0.0020000000949949026, 0.0]
    }
    #db.save_data('depth_image', data)
    print(db.get_data(42,8, 'rotation'))