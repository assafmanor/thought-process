import http.server
import pathlib
from .website import Website


website = Website()
_DATA_DIR = None


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


@website.route('/')
def index():
    users_menu_html = []
    for user_dir in _DATA_DIR.iterdir():
        users_menu_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(users_menu_html))
    return 200, index_html


@website.route('/users/([0-9]+)')
def user(user_id):
    user_thoughts = []
    if not (_DATA_DIR / user_id).is_dir():
        return 404, None
    for user_thoughts_file in (_DATA_DIR / user_id).iterdir():
        thought_time = user_thoughts_file.stem[::-1].replace('-', ':', 2)[::-1].replace('_', ' ', 1)
        thought = user_thoughts_file.read_text()
        user_thoughts.append(_USER_THOUGHT_HTML.format(thought_time=thought_time, thought=thought))
    user_page_html = _USER_PAGE_HTML.format(user_id=user_id, user_thoughts='\n'.join(user_thoughts))
    return 200, user_page_html


def run_webserver(address, data_dir):
    global _DATA_DIR
    _DATA_DIR = pathlib.Path(data_dir)
    website.run(address)


##if __name__ == '__main__':
##    import sys
##    if len(sys.argv) != 3:
##        print(f'USAGE: {argv[0]} <address> <data_dir>')
##        sys.exit(1)
##    address = sys.argv[1].split(':')
##    address[1] = int(address[1])
##    data_dir = sys.argv[2]
##    run_webserver(address, data_dir)
##    sys.exit(0)
