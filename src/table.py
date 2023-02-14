import pandas as pd
from bs4 import BeautifulSoup
import itertools
from src import fetch
from src import soup
from src import cache

class Tabla():
    def __init__(self, base_url, query, container, table_class, header, body, ncols=None):
        self.base_url = base_url
        self.query = query
        self.container = container
        self.table_class = table_class
        # table header tag
        self.header = header
        # table body tag
        self.body = body
        self.ncols = ncols

    def get_url(self):
        if self.query is None:
            return self.base_url
        else:
            return fetch.build_qurl1(self.base_url, self.query)


    def response_mapping(self, text):
        html = BeautifulSoup(text, "lxml")
        table = html.find("table", attrs={"class": self.table_class})

        if not table:
            raise RuntimeError("Incorrect class attr for table: {}.".format(self.table_class))

        ## expect first row to be the header
        header = soup.head_rows_to_list(table)[0]
        body = soup.data_rows_to_list(table)
        return pd.DataFrame(body, columns=header)


    def fetch(self, header_index, headers, expiration):
        self.header_index=header_index
        data = cache.fetch_url_get(self.get_url(), headers, self.response_mapping, expiration)
        return data


def esp_text_to_num_text(text):
    if text == '-': return '0'
    return text.strip().replace('.', '').replace(',', '.')

def soup_to_table(table):
    header = soup.head_rows_to_list(table)
    rows = soup.data_rows_to_list(table)
    width = len(header)
