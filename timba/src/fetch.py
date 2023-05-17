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
    def download(self): raise NotImplementedError()

    def get(self, cache, path, data_mapping):
        print("fetching " + str(self.url))
        r = self.download()
        curl = curlify.to_curl(r.request)
        try:
            if r.status_code != 200:
                raise Exception(
                    "Response status code was: " + str(r.status_code)
                )
            content = data_mapping(r.text)
            cache.set(path, r.text)
            return content
        except Exception as e:
            msg = "error fetching " + self.url + " from source:\n\n" \
                + curl + "\n" \
                + "status code: " + str(r.status_code) + "\n" \
                + "r.text[:100]: '" + r.text[:100] + "'"
            raise RuntimeError(msg) from e


class FetchReqGet(FetchReq):
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def download(self):
        print("downloading " + self.url)
        r = requests.get(self.url, headers=self.headers)
        return r



class FetchReqPost(FetchReq):
    def __init__(self, url, path, headers, data):
        self.url = url
        self.path = path
        self.headers = headers
        self.data = data

    def download(self):
        return requests.post(self.url, data=self.data, headers=self.headers)


class FetchDataYf(FetchData):
    def __init__(self, symbol):
        self.symbol = symbol

    def get(self, cache, path, data_mapping):
        print("fetching " + str(path))
        try:
            df = yf.download(self.symbol)
            if df.shape[0] == 0:
                    raise Exception("No data obtained in yf for: " + self.symbol)
            res = data_mapping(df)
            cache.set(path, df)
            return res
        except Exception as e:
            msg = "error fetching " + self.symbol + " from yf"
            raise RuntimeError(msg) from e
        except requests.exceptions.InvalidSchema as e:
            raise RuntimeError(
                "Error fetching yf.download( " + sumbol +")"
            ) from e

