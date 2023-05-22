import unittest
import requests_mock
from timba.src import fetch, time, cache

url_mock        = "https://foo.bar"
path_mock       = "/path/mock"
headers_mock    = { 'a': 'b' }
data_mock       = { "one": "uno", "two": "dos" }
cache_mock      = cache.CacheMem(time.one_day)

class TestFetch(unittest.TestCase):
    def test_build_qurl1(self):
        url = fetch.build_qurl1("a", ("b", "c"))
        self.assertEqual(
            url,
            "a?b=c"
        )

class TestFetchReq(unittest.TestCase):
    def test_ctor(self):
        fetch_req = fetch.FetchReq(url_mock, headers_mock)
        self.assertEqual(fetch_req.url, url_mock)
        self.assertEqual(fetch_req.headers, headers_mock)

    def test_download(self):
        fetch_req = fetch.FetchReq(url_mock, headers_mock)
        self.assertRaises(NotImplementedError, fetch_req.download)

    def test_get(self):
        '''
        FetchReq does implments get but dnot download so it will throw
        '''
        with requests_mock.Mocker() as m:
            m.get(url_mock, text="") 
            fetch_req = fetch.FetchReq(url_mock, headers_mock)
            self.assertRaises(
                NotImplementedError,
                lambda: fetch_req.get(None, None, None)
            )


class TestFetchReqGet(unittest.TestCase):
    def test_ctor(self):
        fetch_req = fetch.FetchReq(url_mock, headers_mock)
        self.assertEqual(fetch_req.url, url_mock)
        self.assertEqual(fetch_req.headers, headers_mock)

    def test_download(self):
        with requests_mock.Mocker() as m:
            m.get(url_mock, text="") 
            response_text = "response.text"
            fetch_req = fetch.FetchReqGet(url_mock, headers_mock)
            downloaded = fetch_req.download()
            self.assertEqual(downloaded.text, "")
        

    def test_get(self):
        with requests_mock.Mocker() as m:
            response_text = "response.text"
            m.get(url_mock, text=response_text) 
            fetch_req = fetch.FetchReqGet(url_mock, headers_mock)
            res = fetch_req.get(cache_mock, None, lambda x:x)
            self.assertEqual(res.data, response_text)

class TestFetchReqPost(unittest.TestCase):
    def test_ctor(self):
        fetch_req = fetch.FetchReq(url_mock, headers_mock)
        self.assertEqual(fetch_req.url, url_mock)
        self.assertEqual(fetch_req.headers, headers_mock)

    def test_download(self):
        with requests_mock.Mocker() as m:
            m.post(url_mock, text="", headers=headers_mock)
            response_text = "response.text"
            fetch_req = fetch.FetchReqPost(
                url=url_mock,
                path=path_mock,
                headers=headers_mock,
                data=data_mock
            )
            downloaded = fetch_req.download()
            self.assertEqual(downloaded.text, "")
        

    def test_get(self):
        with requests_mock.Mocker() as m:
            response_text = "response.text"
            m.post(url_mock, text=response_text, headers=headers_mock)
            fetch_req = fetch.FetchReqPost(
                url=url_mock,
                path=path_mock,
                headers=headers_mock,
                data=data_mock
            )
            res = fetch_req.get(cache_mock, None, lambda x:x)
            self.assertEqual(res.data, response_text)


class TestFetchDataYf(unittest.TestCase):
    def test_ctor(self):
        fetch_req = fetch.FetchDataYf("symbol")
        self.assertEqual(fetch_req.symbol, "symbol")

class TestFetchUrlResponse(unittest.TestCase):
    def test_ctor(self):
        content_mock = "content"
        res = fetch.FetchUrlResponse(content_mock, True, None)
        self.assertEqual(res.data, content_mock)
        self.assertEqual(res.data_was_cached, True)
        self.assertEqual(res.mtime, None)

    def test_get_data_acting_if_downloaded(self):
        content_mock = "content"
        res = fetch.FetchUrlResponse(content_mock, True, None)
        content = res.get_data_acting_if_downloaded(lambda:None)
        self.assertEqual(content, content_mock)

