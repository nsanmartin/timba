import pandas as pd
import yfinance as yf
import curlify
from timba.src import fetch
from pathlib import Path
import datetime as dt
import requests
import json
import os.path




def url_to_cache_path(url):
    return Path(Cache.CACHE_PATH + url.replace('//', '/') + '$')


class Cache:
    TIMBA_PATH = str(Path.home()) + '/.timba/'
    CACHE_PATH = TIMBA_PATH + 'cache/'

    def __init__(self, expiration_time):
        self.expiration_time = expiration_time

    def is_stored(self, path): raise NotImplementedError()

    def is_valid(self, path):
        if not self.is_stored(path):
            return False

        if self.expiration_time is None:
            return True
        expiration = path.stat().st_mtime + self.expiration_time
        return expiration >= dt.datetime.now().timestamp()


class CacheDisc(Cache):
    def is_stored(self, path): return path.exists()

class CacheFile(CacheDisc):
    def get(self, path):
        with open(path) as f:
            return f.read()

    def set(self, path, content):
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(content)

class CacheDataFrame(CacheDisc):
    def get(self, path):
        return pd.read_csv(path)

    def set(self, path, df):
        path.parent.mkdir(exist_ok=True, parents=True)
        df.to_csv(path)


class CacheMem(Cache):
    store = {}
    expiration = {}

    def is_stored(self, path):
        return path in CacheMem.store
    
    def is_valid(self, path):
        if not self.is_stored(path): return False
        if self.expiration_time is None: return True

        expiration = CacheMem.expiration[path] + self.expiration_time
        return expiration >= dt.datetime.now().timestamp()

    def get(self, path):
        return CacheMem.store[path]

    def set(self, path, df):
        CacheMem.store[path] = df
        CacheMem.expiration[path] = dt.datetime.now().timestamp()



def get_data_for(url):
    path = Cache.TIMBA_PATH + 'data/' + url
    with open(path) as f:
        return json.load(f)
    
def get_headers_for(url):
    path = Cache.TIMBA_PATH + 'headers/' + url
    if os.path.isfile(path):
        with open(path) as f:
            return json.load(f)
    return {}
    

def cache_is_valid(path, expiration_time):
    if not path.exists():
        return False

    if expiration_time is None:
        return True
    expiration = path.stat().st_mtime + expiration_time
    return expiration >= dt.datetime.now().timestamp()


class FetchUrlResponse:
    def __init__(self, data, data_was_cached):
        self.data = data
        self.data_was_cached = data_was_cached

    def get_data_acting_if_downloaded(self, action):
        if not self.data_was_cached:
            action()
        return self.data


def fetch_url(fetcher, response_mapping, cache, path):
    if cache.is_valid(path):
        return FetchUrlResponse(
            data=response_mapping(cache.get(path)),
            data_was_cached=True
        )
    else:
        try:
            return FetchUrlResponse(
                data=fetcher.get(cache, path, response_mapping),
                data_was_cached=False
            )
        except requests.exceptions.InvalidSchema as e:
            raise RuntimeError("Error fetching url: " + fetcher.url) from e


