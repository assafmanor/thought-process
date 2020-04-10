from datetime import datetime
from flask import abort, Flask, render_template,\
    redirect, request, send_from_directory
import json
import re
import requests

from ..utils.cli_utils import DEFAULT_IP, DEFAULT_API_PORT, DEFAULT_GUI_PORT


BIRTHDATE_STR_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_STR_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def create_app(api_url):
    app = Flask(__name__,
            template_folder='templates',
            static_url_path='/static')
    app.url_map.strict_slashes = False


    @app.route('/')
    def homepage():
        return render_template("homepage.html")


    @app.route('/users')
    def users():
        users_url = f'{api_url}/users'
        r = requests.get(users_url)
        if r.status_code == 404:
            users = None
        else:
            users = r.json()
            for user in users:
                _fix_timestamp(user, 'birthdate', BIRTHDATE_STR_FORMAT)
            users.sort(key=lambda k: k['id'])
        return render_template("users.html",
            users=users)


    @app.route('/user')
    def user_page():
        user_id = request.args.get('id', type=int)
        if not user_id:
            abort(404)
        user_url = f'{api_url}/users/{user_id}'
        snapshots_url = f'{api_url}/users/{user_id}/snapshots'
        snapshot_request = requests.get(snapshots_url)
        if snapshot_request.status_code == 404:
            message = snapshot_request.json()['message']
            abort(404, message)
        snapshots = snapshot_request.json()
        user_request = requests.get(user_url)
        user = user_request.json()
        _fix_timestamp(user, 'birthdate', BIRTHDATE_STR_FORMAT)
        for snapshot in snapshots:
            _fix_timestamp(snapshot, 'timestamp', DATETIME_STR_FORMAT)
        snapshots.sort(key=lambda k: k['timestamp'])
        return render_template("user_page.html",
            user=user,
            snapshots=snapshots)

    @app.route('/snapshot')
    def snapshot():
        user_id = request.args.get('user_id', type=int)
        snapshot_id = request.args.get('snapshot_id', type=int)
        if not user_id or not snapshot_id:
            abort(404)
        snapshot_url = f'{api_url}/users/{user_id}/snapshots/{snapshot_id}'
        req = requests.get(snapshot_url)
        if req.status_code == 404:
            message = req.json()['message']
            abort(404, message)
        snapshot = req.json()
        _fix_timestamp(snapshot, 'timestamp', DATETIME_STR_FORMAT)
        snapshot_url = snapshot_url.replace('api', 'localhost')
        if snapshot['color_image']:
            snapshot['color_image'] = f'{snapshot_url}/color_image/data'
        if snapshot['depth_image']:
            snapshot['depth_image'] = f'{snapshot_url}/depth_image/data'
        user_url = f'{api_url}/users/{user_id}'
        username = requests.get(user_url).json()['name']
        return render_template("snapshot.html",
            snapshot=snapshot,
            username=username)

    @app.route('/search')
    def search():
        user_id = request.args.get('user_id')
        if not user_id:
            return render_template("search.html")
        if not user_id.isdigit():
            abort(404)
        user_id = int(user_id)
        user_url = f'{api_url}/users/{user_id}'
        req = requests.get(user_url)
        if req.status_code == 404:
            return render_template("search.html", user_id=user_id)
        return redirect(f'/user?id={user_id}')

    @app.errorhandler(404)
    def page_not_found(e):
        message = re.sub('404 Not Found: ', '', str(e)).capitalize()+'.'
        return render_template('404.html', message=message), 404


    return app


def run_server(host=DEFAULT_IP, port=DEFAULT_GUI_PORT,
               api_host=DEFAULT_IP, api_port=DEFAULT_API_PORT):
    api_url = f'http://{api_host}:{api_port}'
    app = create_app(api_url)
    app.run(host, port)


def _fix_timestamp(data_dict, key, dt_format):
    ts_str = data_dict[key]
    data_dict[key] = datetime.strptime(
        ts_str, dt_format)
