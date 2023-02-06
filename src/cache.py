from src import fetch
from pathlib import Path
import datetime as dt

CACHE_PATH = str(Path.home()) + '/.timba/'
EXPIRATION_TIME = 60 * 60 * 24

def url_to_cache_path(url):
    return Path(CACHE_PATH + url.replace('//', '/'))

def path_has_expired(path, expiration_time):
    now = dt.datetime.now().timestamp()
    return not path.exists()\
            or path.stat().st_mtime + EXPIRATION_TIME < now


def get_url(url, expiration_time=EXPIRATION_TIME):
    path = url_to_cache_path(url)

    if path_has_expired(path, expiration_time):
        content = fetch.web_page(url)
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(content)
        return content
    else:
        with open(path) as f:
            return f.read()

