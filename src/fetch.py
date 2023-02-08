import lxml
import requests
import pandas as pd
import re


def web_page(url):
    return requests.get(url).text

def build_qurl1(base, q):
    return '{}?{}={}'.format(base, q[0], q[1])

