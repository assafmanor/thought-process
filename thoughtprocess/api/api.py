from flask import Flask, make_response
from flask_restful import abort, Api, Resource
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app)


NO_USERS_MSG = 'no users yet'
USER_NOT_FOUND_MSG = 'user {user_id} was not found'
USER_NO_SNAPSHOTS_MSG = 'user {user_id} has no snapshots'
SNAPSHOT_NOT_FOUND_MSG = 'snapshot {snapshot_id} was not found for user {user_id}'
NO_RESULTS_MSG = "no '{result_name}' data was found for snapshot {snapshot_id}"
NO_DATA_MSG = 'no data to display'

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
            if not users:
                abort(404, message=NO_USERS_MSG)
            for user in users:
                del user["gender"]
                del user["birthdate"]
            return users

    class UserId(Resource):
        def get(self, user_id):
            db = _get_db()
            user = db.get_user(user_id)
            if not user:
                message = USER_NOT_FOUND_MSG.format(user_id=user_id)
                abort(404, message=message)
            return _jsonify_user(user)

    class UserSnapshots(Resource):
        def get(self, user_id):
            db = _get_db()
            user = db.get_user(user_id)
            if not user:
                message = USER_NOT_FOUND_MSG.format(user_id=user_id)
                abort(404, message=message)
            snapshots = db.get_user_snapshots(user_id)
            if not snapshots:
                message = USER_NO_SNAPSHOTS_MSG.format(user_id=user_id)
                abort(404, message=message)
            for snapshot in snapshots:
                _jsonify_snapshot(snapshot)
            return snapshots

    class SpecificSnapshot(Resource):
        def get(self, user_id, snapshot_id):
            db = _get_db()
            user = db.get_user(user_id)
            if not user:
                message = USER_NOT_FOUND_MSG.format(user_id=user_id)
                abort(404, message=message)
            snapshot = db.get_snapshot(user_id, snapshot_id)
            if not snapshot:
                message = SNAPSHOT_NOT_FOUND_MSG.format(
                    snapshot_id=snapshot_id,
                    user_id=user_id)
                abort(404, message=message)
            snapshot_dict = _jsonify_snapshot(snapshot)
            if snapshot_dict['pose']:
                snapshot_dict['pose'] = json.loads(snapshot_dict['pose'])
            if snapshot_dict['feelings']:
                snapshot_dict['feelings'] = json.loads(snapshot_dict['feelings'])
            return snapshot_dict

    class Result(Resource):
        def get(self, user_id, snapshot_id, result_name):
            db = _get_db()
            user = db.get_user(user_id)
            if not user:
                message = USER_NOT_FOUND_MSG.format(user_id=user_id)
                abort(404, message=message)
            snapshot = db.get_snapshot(user_id, snapshot_id)
            if not snapshot:
                message = SNAPSHOT_NOT_FOUND_MSG.format(
                    snapshot_id=snapshot_id,
                    user_id=user_id)
                abort(404, message=message)
            # make result names such as 'color_image' invalid
            result_name = result_name.replace('_', '*')
            result_name = result_name.replace('-', '_')
            result = db.get_data(user_id, snapshot_id, result_name)
            if not result:
                message = NO_RESULTS_MSG.format(
                    result_name=result_name,
                    snapshot_id=snapshot_id)
                abort(404, message=message)
            return result

    class Data(Resource):
        def get(self, user_id, snapshot_id, result_name):
            if result_name not in ['color_image', 'depth_image']:
                abort(404, message=NO_DATA_MSG)
            db = _get_db()
            user = db.get_user(user_id)
            if not user:
                message = USER_NOT_FOUND_MSG.format(user_id=user_id)
                abort(404, message=message)
            snapshot = db.get_snapshot(user_id, snapshot_id)
            if not snapshot:
                message = SNAPSHOT_NOT_FOUND_MSG.format(
                    snapshot_id=snapshot_id,
                    user_id=user_id)
                abort(404, message=message)
            result = db.get_data(user_id, snapshot_id, result_name)
            if not result:
                message = NO_RESULTS_MSG.format(
                    result_name=result_name,
                    snapshot_id=snapshot_id)
                abort(404, message=message)
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
    user['birthdate'] = user['birthdate'].timestamp()
    return user


def _jsonify_snapshot(snapshot):
    snapshot['timestamp'] = snapshot['timestamp'].timestamp()
    return snapshot