"""
This module provides caches to store data locally and reduce the number of 
network requests
"""

from pathlib import Path
import datetime as dt
import json
import os.path
import pandas as pd
import requests

from timba.src import fetch



def url_to_cache_path(url):
    'Given an url, generate a local path for it'
    return Path(Cache.CACHE_PATH + url.replace('//', '/') + '$')


class Cache:
    "Cache base class"
    TIMBA_PATH = str(Path.home()) + '/.timba/'
    CACHE_PATH = TIMBA_PATH + 'cache/'

    def __init__(self, expiration_time):
        self.expiration_time = expiration_time

    def is_stored(self, path):
        'returns whether the caches stores the resourse, pure virtual'
        raise NotImplementedError()

    def get_stored_time(self, path):
        'If stored, return its modification time. If not, None'
        if not self.is_stored(path):
            return None

        stored_time = path.stat().st_mtime

        if self.expiration_time \
            and stored_time + self.expiration_time \
                >= dt.datetime.now().timestamp():
            return stored_time
        return None



class CacheDisc(Cache):
    'Cache implementation for local disc storage'
    def is_stored(self, path):
        return path.exists()

class CacheFile(CacheDisc):
    'Cache implementation for local regular file storage'
    def get(self, path):
        'Read file'
        with open(path) as f:
            return f.read()

    def set(self, path, content):
        'Store content at path'
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(content)
        return path.stat().st_mtime

class CacheDataFrame(CacheDisc):
    'Cache implementation for local csv file storage'
    def get(self, path):
        'Read csv'
        return pd.read_csv(path)

    def set(self, path, df):
        'Store data frame at path'
        path.parent.mkdir(exist_ok=True, parents=True)
        df.to_csv(path)
        return path.stat().st_mtime


class CacheMem(Cache):
    'Cache implementation in memory'
    store = {}
    expiration = {}

    def is_stored(self, path):
        return path in CacheMem.store

    def get_stored_time(self, path):
        if not self.is_stored(path):
            return None

        if self.expiration_time \
            and CacheMem.expiration[path] + self.expiration_time \
                >= dt.datetime.now().timestamp():
            return CacheMem.expiration[path]

        return None


    def get(self, path):
        'Get resource from sore'
        return CacheMem.store[path]

    def set(self, path, df):
        'Store in memory'
        stored_time = dt.datetime.now().timestamp()
        CacheMem.store[path] = df
        CacheMem.expiration[path] = stored_time
        return stored_time



def get_data_for(url):
    'Get http request data from local folder configuration'
    path = Cache.TIMBA_PATH + 'data/' + url
    with open(path) as f:
        return json.load(f)

def get_headers_for(url):
    'Get http request headers from local folder configuration'
    path = Cache.TIMBA_PATH + 'headers/' + url
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}





def fetch_url(fetcher, response_mapping, cache, path):
    '''
    Fetch and transform data with response_mapping using cache as cache.
    '''
    mtime = cache.get_stored_time(path)
    if mtime:
        return fetch.FetchUrlResponse(
            data=response_mapping(cache.get(path)),
            data_was_cached=True,
            mtime=mtime
        )

    try:
        return fetcher.get(cache, path, response_mapping)
    except requests.exceptions.InvalidSchema as e:
        raise RuntimeError("Error fetching url: " + fetcher.url) from e
