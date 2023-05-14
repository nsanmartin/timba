import pandas as pd
import yfinance as yf
import curlify
from src import fetch
from pathlib import Path
import datetime as dt
import requests
import json
import os.path


TIMBA_PATH = str(Path.home()) + '/.timba/'
CACHE_PATH = TIMBA_PATH + 'cache/'

def get_data_for(url):
    path = TIMBA_PATH + 'data/' + url
    with open(path) as f:
        return json.load(f)
    
def get_headers_for(url):
    path = TIMBA_PATH + 'headers/' + url
    if os.path.isfile(path):
        with open(path) as f:
            return json.load(f)
    return {}
    

def url_to_cache_path(url):
    return Path(CACHE_PATH + url.replace('//', '/') + '$')

def time_has_expired(time):
    return time < dt.datetime.now().timestamp()

def cache_is_valid(path, expiration_time):
    if not path.exists():
        return False

    if expiration_time is None:
        return True
    expiration = path.stat().st_mtime + expiration_time
    return expiration >= dt.datetime.now().timestamp()



def fetch_url_get(url, headers, response_mapping, expiration):
    path = url_to_cache_path(url)
    if cache_is_valid(path, expiration):
        with open(path) as f:
            return response_mapping(f.read())
    else:
        try:
            print("fetching " + url)
            r = requests.get(url, headers=headers)
            curl = curlify.to_curl(r.request)
            try:
                if r.status_code != 200:
                    raise Exception(
                        "Response status code was: " \
                            + str(r.status_code)
                    )
                content = response_mapping(r.text)
                path.parent.mkdir(exist_ok=True, parents=True)
                path.write_text(r.text)
                return content
            except Exception as e:
                msg = "error fetching " + url + " from source:\n\n" \
                    + curl + "\n" \
                    + "status code: " + str(r.status_code) + "\n" \
                    + "r.text[:100]: '" + r.text[:100] + "'"
                raise RuntimeError(msg) from e
        except requests.exceptions.InvalidSchema as e:
            raise RuntimeError("Error fetching url: " + url) from e


def fetch_url_post(file, endpoint, headers, data, response_mapping, expiration):
    path = url_to_cache_path(endpoint + "/" + file)
    if cache_is_valid(path, expiration):
        with open(path) as f:
            #return str(path), f.read()
            return response_mapping(f.read())
    else:
        print("fetching " + str(endpoint))
        # print("with data: " + str(data))
        # print("and headers: " + str(headers))
        try:

            r = requests.post(endpoint, data=data, headers=headers)
            curl = curlify.to_curl(r.request)
            try:
                if r.status_code != 200:
                    raise Exception("Response status code was: " + str(r.status_code))
                content = response_mapping(r.text)
                path.parent.mkdir(exist_ok=True, parents=True)
                path.write_text(r.text)
                return content
            except Exception as e:
                msg = "error fetching " + endpoint \
                        + " from source:\n\n" + curl + "\n" \
                        + "status code: " + str(r.status_code) + "\n" \
                        + "r.text[:100]: '" + r.text[:100] + "'"
                raise RuntimeError(msg) from e
        except requests.exceptions.InvalidSchema as e:
            raise RuntimeError(
                "Error fetching endpoint: " + endpoint
            ) from e



def fetch_yf_download(symbol, expiration, response_mapping):
    path = url_to_cache_path("yf/download/" + symbol)
    if cache_is_valid(path, expiration):
        return response_mapping(pd.read_csv(path))
    else:
        try:
            df = yf.download(symbol)
            if df.shape[0] == 0:
                    raise Exception(
                        "No data obtained in yf for: " + symbol
                    )
            res = response_mapping(df)
            path.parent.mkdir(exist_ok=True, parents=True)
            df.to_csv(path)
            return res
        except Exception as e:
            msg = "error fetching " + symbol + " from yf"
            raise RuntimeError(msg) from e
        except requests.exceptions.InvalidSchema as e:
            raise RuntimeError(
                "Error fetching yf.download( " + sumbol +")"
            ) from e

    
