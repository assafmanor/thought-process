from flask import Flask, make_response
from flask_restful import abort, Api, Resource

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app)


class RestfulApi:
    db = None
    
    @classmethod
    def run(cls, db, host, port):
        cls.db = db
        app.run(host, port)

    class Users(Resource):
        def get(self):
            db = _get_db()
            users = db.get_users()
            for user in users:
                _jsonify_user(user)
            return users

    class UserId(Resource):
        def get(self, user_id):
            db = _get_db()
            user = db.get_user(user_id)
            if not user:
                abort(404, message=f'user {user_id} was not found.')
            return _jsonify_user(user)

    class UserSnapshots(Resource):
        def get(self, user_id):
            db = _get_db()
            snapshots = db.get_user_snapshots(user_id)
            for snapshot in snapshots:
                _jsonify_snapshot(snapshot)
            return snapshots

    class SpecificSnapshot(Resource):
        def get(self, user_id, snapshot_id):
            db = _get_db()
            user = db.get_user(user_id)
            if user is None:
                abort(404, message=f'user {user_id} was not found.')
            snapshot = db.get_snapshot(user_id, snapshot_id)
            if snapshot is None:
                abort(404, message=f'snapshot {snapshot_id} was not found')
            return _jsonify_snapshot(snapshot)

    class Result(Resource):
        def get(self, user_id, snapshot_id, result_name):
            db = _get_db()
            user = db.get_user(user_id)
            if user is None:
                abort(404, message=f'user {user_id} was not found.')
            snapshot = db.get_snapshot(user_id, snapshot_id)
            if snapshot is None:
                abort(404, message=f'snapshot {snapshot_id} was not found')
            result = db.get_data(user_id, snapshot_id, result_name)
            if result is None:
                abort(404, message=f'found no results')
            return result

    class Data(Resource):
        def get(self, user_id, snapshot_id, result_name):
            if result_name not in ['color_image', 'depth_image']:
                abort(404, message='no data to display')
            db = _get_db()
            user = db.get_user(user_id)
            if user is None:
                abort(404, message=f'user {user_id} was not found.')
            snapshot = db.get_snapshot(user_id, snapshot_id)
            if snapshot is None:
                abort(404, message=f'snapshot {snapshot_id} was not found')
            result = db.get_data(user_id, snapshot_id, result_name)
            if result is None:
                abort(404, message=f'found no results')
            with open(result, 'rb') as f:
                image_binary = f.read()
            response = make_response(image_binary)            
            response.headers.set('Content-Type', 'image/jpeg')
            return response
            


api.add_resource(
    RestfulApi.Users,
    '/users')

api.add_resource(
    RestfulApi.UserId,
    '/users/<int:user_id>')

api.add_resource(
    RestfulApi.UserSnapshots,
    '/users/<int:user_id>/snapshots')

api.add_resource(
    RestfulApi.SpecificSnapshot,
    '/users/<int:user_id>/snapshots/<int:snapshot_id>')

api.add_resource(
    RestfulApi.Result,
    '/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')

api.add_resource(
    RestfulApi.Data,
    '/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')


def _get_db():
    return RestfulApi.db

def _jsonify_user(user):
    user['birthdate'] = user['birthdate'].__str__()
    return user

def _jsonify_snapshot(snapshot):
    snapshot['timestamp'] = snapshot['timestamp'].__str__()
    return snapshot