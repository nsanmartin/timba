import pandas as pd
from bs4 import BeautifulSoup
import itertools
from src import fetch
from src import soup

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
        self.data = fetch.web_page(self.get_url())

    def get_url(self):
        if self.query is None:
            return self.base_url
        else:
            return fetch.build_qurl1(self.base_url, self.query)

    def get_header(self, html, header_index):
        header = soup.head_rows_to_list(html.find(self.header))[header_index]
        return header

    def get_rows(self, html, ncols):
        body = html.find(self.body)
        if not body:
            raise RuntimeError("Incorrect body tag: {} for table.".format(self.body))

        body_rows = soup.data_rows_to_list(body)
        if ncols == None:
            lens = list(map(len,body_rows))
            ncols = max(set(lst), key=lst.count)
        body_rows = list(
            itertools.dropwhile(
                lambda x:len(x) != ncols,
                body_rows
            )
        )
        body_rows = list(
            itertools.takewhile(
                lambda x: len(x) == ncols,
                body_rows
            )
        )
        return body_rows

    def fetch(self, header_index):
        html = BeautifulSoup(self.data, "lxml")
        
        if self.container:
            tag, classname = self.container
            html = html.find(tag, attrs={"class": classname})
        table = html.find("table", attrs={"class": self.table_class})

        if not table:
            raise RuntimeError("Incorrect class attr for table: {}.".format(
                self.table_class
            ))

        header = self.get_header(table, header_index)
        ncols = len(header)
        if self.ncols is not None:
            ncols = self.ncols
        
        body = self.get_rows(table, ncols)
        
        return pd.DataFrame(body, columns=header)
        #if len(header) != ncols:
        #    return pd.DataFrame(body)
        #else:
        #    return pd.DataFrame(body, columns=header)


def esp_text_to_num_text(text):
    if text == '-': return '0'
    return text.strip().replace('.', '').replace(',', '.')

def soup_to_table(table):
    header = soup.head_rows_to_list(table)
    rows = soup.data_rows_to_list(table)
    width = len(header)
