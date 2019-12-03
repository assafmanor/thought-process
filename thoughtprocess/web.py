import pathlib
from flask import Flask

app = Flask(__name__)


_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''


_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''


_USER_PAGE_HTML = '''
<html>
    <head>
    <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {user_thoughts}
        </table>
    </body>
</html>
'''


_USER_THOUGHT_HTML = '''
<tr>
    <td>{thought_time}</td>
    <td>{thought}</td>
</tr>
'''


def register_web_pages(data_dir):

    data_path = pathlib.Path(data_dir)

    @app.route('/')
    def index():
        user_menu = []
        for user_dir in data_path.iterdir():
            user_menu.append(_USER_LINE_HTML.format(user_id=user_dir.name))
        index_html = _INDEX_HTML.format(users='\n'.join(user_menu))
        return index_html, 200

    @app.route('/users/<int:user_id>')
    def user(user_id):
        user_id = str(user_id)
        user_thoughts = []
        if not (data_path / user_id).is_dir():
            return None, 400
        for user_thoughts_file in (data_path / user_id).iterdir():
            thought_time = user_thoughts_file.stem[::-1]. \
                replace('-', ':', 2)[::-1].replace('_', ' ', 1)
            thought = user_thoughts_file.read_text()
            user_thoughts.append(
                _USER_THOUGHT_HTML.format(
                    thought_time=thought_time,
                    thought=thought
                    )
                )
        user_page_html = _USER_PAGE_HTML.format(
            user_id=user_id,
            user_thoughts='\n'.join(user_thoughts)
            )
        return user_page_html, 200


def run_webserver(address, data_dir):
    register_web_pages(data_dir)
    app.run(*address)
