from src import fetch
from pathlib import Path
import datetime as dt

CACHE_PATH = str(Path.home()) + '/.timba/'

def url_to_cache_path(url):
    return Path(CACHE_PATH + url.replace('//', '/'))

def time_has_expired(time):
    return time < dt.datetime.now().timestamp()

def cache_is_valid(path, expiration_time):
    return path.exists() \
        and (not expiration_time \
            or not time_has_expired(path.stat().st_mtime + expiration_time))



def get_url(url, expiration_time=None):
    path = url_to_cache_path(url)
    if cache_is_valid(path, expiration_time):
        with open(path) as f:
            return f.read()
    else:
        print("fetching " + url)
        content = fetch.web_page(url)
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(content)
        return content

