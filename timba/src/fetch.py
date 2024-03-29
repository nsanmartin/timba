import lxml
import yfinance as yf
import requests
import pandas as pd
import re
import curlify


#todo delete
def build_qurl1(base, q):
    return '{}?{}={}'.format(base, q[0], q[1])

class FetchData():
    pass

class FetchReq(FetchData):
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def download(self): raise NotImplementedError()

    def get(self, cache, path, data_mapping):
        r = self.download()
        curl = curlify.to_curl(r.request)
        try:
            if r.status_code != 200:
                raise Exception(
                    "Response status code was: " + str(r.status_code)
                )
            content = data_mapping(r.text)
            mtime = cache.set(path, r.text)
            return FetchUrlResponse(
                data=content,
                data_was_cached=False,
                mtime=mtime
            )
        except Exception as e:
            msg = "error fetching " + self.url + " from source:\n\n" \
                + curl + "\n" \
                + "status code: " + str(r.status_code) + "\n" \
                + "r.text[:100]: '" + r.text[:100] + "'"
            raise RuntimeError(msg) from e


class FetchReqGet(FetchReq):
    def download(self):
        r = requests.get(self.url, headers=self.headers)
        return r



class FetchReqPost(FetchReq):
    def __init__(self, url, path, headers, data):
        super().__init__(url, headers)
        self.path = path
        self.data = data

    def download(self):
        return requests.post(self.url, data=self.data, headers=self.headers)


class FetchDataYf(FetchData):
    def __init__(self, symbol):
        self.symbol = symbol

    def get(self, cache, path, data_mapping):
        try:
            df = yf.download(self.symbol)
            if df.shape[0] == 0:
                    raise Exception("No data obtained in yf for: " + self.symbol)
            res = data_mapping(df)
            mtime = cache.set(path, df)
            return FetchUrlResponse(
                data=res,
                data_was_cached=False,
                mtime=mtime
            )
        except Exception as e:
            msg = "error fetching " + self.symbol + " from yf"
            raise RuntimeError(msg) from e
        except requests.exceptions.InvalidSchema as e:
            raise RuntimeError(
                "Error fetching yf.download( " + self.symbol +")"
            ) from e


class FetchUrlResponse:
    def __init__(self, data, data_was_cached, mtime):
        self.data = data
        self.data_was_cached = data_was_cached
        self.mtime = mtime

    def get_data_acting_if_downloaded(self, action):
        if not self.data_was_cached:
            action()
        return self.data

