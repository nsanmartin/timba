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

    def get_stored_time(self, path):
        if not self.is_stored(path):
            return None

        stored_time = path.stat().st_mtime

        if self.expiration_time \
            and stored_time + self.expiration_time \
                >= dt.datetime.now().timestamp():
            return stored_time
        else: return None



class CacheDisc(Cache):
    def is_stored(self, path): return path.exists()

class CacheFile(CacheDisc):
    def get(self, path):
        with open(path) as f:
            return f.read()

    def set(self, path, content):
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(content)
        return path.stat().st_mtime

class CacheDataFrame(CacheDisc):
    def get(self, path):
        return pd.read_csv(path)

    def set(self, path, df):
        path.parent.mkdir(exist_ok=True, parents=True)
        df.to_csv(path)
        return path.stat().st_mtime


class CacheMem(Cache):
    store = {}
    expiration = {}

    def is_stored(self, path):
        return path in CacheMem.store
    
    def get_stored_time(self, path):
        if not self.is_stored(path): return None

        if self.expiration_time \
            and CacheMem.expiration[path] + self.expiration_time \
                >= dt.datetime.now().timestamp():
                return CacheMem.expiration[path] 
        else:
            return None


    def get(self, path):
        return CacheMem.store[path]

    def set(self, path, df):
        stored_time = dt.datetime.now().timestamp()
        CacheMem.store[path] = df
        CacheMem.expiration[path] = stored_time
        return stored_time



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
    




def fetch_url(fetcher, response_mapping, cache, path):
    mtime = cache.get_stored_time(path)
    if mtime:
        return fetch.FetchUrlResponse(
            data=response_mapping(cache.get(path)),
            data_was_cached=True,
            mtime=mtime
        )
    else:
        try:
            return fetcher.get(cache, path, response_mapping)
        except requests.exceptions.InvalidSchema as e:
            raise RuntimeError("Error fetching url: " + fetcher.url) from e


