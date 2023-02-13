import curlify
from src import fetch
from pathlib import Path
import datetime as dt
import requests
import json


CACHE_PATH = str(Path.home()) + '/.timba/cache/'

def get_data_for(url):
    path = CACHE_PATH + 'data/' + url
    with open(path) as f:
        return json.load(f)
    
def get_headers_for(url):
    path = CACHE_PATH + 'headers/' + url
    with open(path) as f:
        return json.load(f)
    

def url_to_cache_path(url):
    return Path(CACHE_PATH + url.replace('//', '/'))

def time_has_expired(time):
    return time < dt.datetime.now().timestamp()

def cache_is_valid(path, expiration_time):
    if not path.exists():
        return False

    if expiration_time is None:
        return True
    expiration = path.stat().st_mtime + expiration_time
    return expiration >= dt.datetime.now().timestamp()



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


def get_post(file, endpoint, data, headers, expiration_time=None):
    path = url_to_cache_path(endpoint + "/" + file)
    if cache_is_valid(path, expiration_time):
        with open(path) as f:
            return str(path), f.read()
    else: 
        print("fetching " + endpoint)
        print(data)
        print(headers)
        r = requests.post(endpoint, data=data, headers=headers)
        curl = curlify.to_curl(r.request)
        if r.status_code == 200:
            content = r.text
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text(content)
            return curl, content
        else:
            curl, None

