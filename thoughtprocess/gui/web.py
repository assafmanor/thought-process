from flask import abort, Flask, render_template,\
    redirect, request, Response, send_from_directory
import re
import requests

from ..utils.cli_utils import DEFAULT_IP, DEFAULT_API_PORT, DEFAULT_GUI_PORT
from .utils import *

_GENDER_DICT = {'m': 'Male', 'f':'Female', 'o': 'Other'}


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
                user['gender'] = _GENDER_DICT[user['gender']]
                format_timestamp(user, 'birthdate')
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
        user['gender'] = _GENDER_DICT[user['gender']]
        format_timestamp(user, 'birthdate')
        for snapshot in snapshots:
            format_timestamp(snapshot, 'timestamp')
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
        format_timestamp(snapshot, 'timestamp')
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

    @app.route('/stats')
    def stats():
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            abort(404)
        user_url = f'{api_url}/users/{user_id}'
        snapshots_url = f'{api_url}/users/{user_id}/snapshots'
        req = requests.get(snapshots_url)
        if req.status_code == 404:
            message = req.json()['message']
            abort(404, message)
        snapshots = req.json()
        user_request = requests.get(user_url)
        user = user_request.json()
        user['gender'] = _GENDER_DICT[user['gender']]
        format_timestamp(user, 'birthdate')
        snapshot_url = f'{api_url}/users/{user_id}/snapshots/' + '{id}'
        avg_snapshot = calc_average(snapshot_url, snapshots)
        return render_template("stats.html",
            user=user,
            average=avg_snapshot)

    @app.errorhandler(404)
    def page_not_found(e):
        message = re.sub('404 Not Found: ', '', str(e)).capitalize()+'.'
        return render_template('404.html', message=message), 404

    @app.route('/feeling_plot.png')
    def plot_png():
        user_id = request.args.get('user_id', type=int)
        feeling_name = request.args.get('type')
        if not user_id:
            abort(404)
        names = {'hunger': 0, 'thirst': 1, 'exhaustion': 2, 'happiness': 3}
        if feeling_name not in names:
            abort(404)
        snapshots_url = f'{api_url}/users/{user_id}/snapshots'
        req = requests.get(snapshots_url)
        if req.status_code == 404:
            message = req.json()['message']
            abort(404, message)
        snapshots = req.json()
        snapshot_url = f'{api_url}/users/{user_id}/snapshots/' + '{id}'
        feeling_lst = get_arranged_feelings(snapshot_url, snapshots)[names[feeling_name]]
        feeling_lst_perc = [val*100 for val in feeling_lst]
        fig = create_figure(feeling_lst_perc,
            f'{feeling_name.capitalize()} Over Time',
            f'{feeling_name.capitalize()} in %')
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

    return app


def run_server(host=DEFAULT_IP, port=DEFAULT_GUI_PORT,
               api_host=DEFAULT_IP, api_port=DEFAULT_API_PORT):
    api_url = f'http://{api_host}:{api_port}'
    app = create_app(api_url)
    app.run(host, port)
