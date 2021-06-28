import pandas as pd
import itertools
from src import fetch
from src import soup

class Tabla():
    def __init__(self, base_url, query, container, table_class, header, body, ncols=None):
        self.base_url = base_url
        self.query = query
        self.container = container
        self.table_class = table_class
        self.header = header
        self.body = body
        self.ncols = ncols

    def get_url(self):
        if self.query is None:
            return self.base_url
        else:
            return fetch.build_qurl1(self.base_url, self.query)

    def get_header(self, html, header_index):
        header = soup.head_rows_to_list(html.find(self.header))[header_index]
        return header

    def get_rows(self, html, ncols):
        body = soup.data_rows_to_list(html.find(self.body))
        body = list(
            itertools.dropwhile(
                lambda x:len(x) != ncols,
                body
            )
        )
        body = list(
            itertools.takewhile(
                lambda x: len(x) == ncols,
                body
            )
        )
        return body

    def fetch(self, header_index):
        html = fetch.web_page_soup(self.get_url())
        if self.container:
            html = html.find(self.container[0], attrs={"class": self.container[1]})
        header = self.get_header(html, header_index)
        print(header)
        ncols = len(header)
        if self.ncols is not None:
            ncols = self.ncols
        body = self.get_rows(html, ncols)
        return pd.DataFrame(body, columns=header)


def esp_text_to_num_text(text):
    if text == '-': return '0'
    return text.strip().replace('.', '').replace(',', '.')

def soup_to_table(table):
    header = soup.head_rows_to_list(table)
    print(header)
    rows = soup.data_rows_to_list(table)
    width = len(header)
