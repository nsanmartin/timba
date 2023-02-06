from bs4 import BeautifulSoup
import lxml
import requests
import pandas as pd
import re


def web_page(url):
    return requests.get(url).text

def web_page_soup(url):
    return BeautifulSoup(web_page(url), "lxml")

def build_qurl1(base, q):
    return '{}?{}={}'.format(base, q[0], q[1])

