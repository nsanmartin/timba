from timba.scraping import  ScrapingSupplier
from timba.src import soup, fetch, cache
import pandas as pd
from bs4 import BeautifulSoup

class Url:
    eco = "https://bonos.ecovalores.com.ar/eco/"



def map_each_dolar(elem):
    try:
        header = soup.head_rows_to_list(elem)[0]
        body = soup.data_rows_to_list(elem)
        return pd.DataFrame(body, columns=header)
    except ValueError:
        return None


def response_mapping_dolar(text):
    html = BeautifulSoup(text, "lxml")
    table = html.find_all("table", attrs={"class": "tablapanel"})
    if not table:
        raise RuntimeError(
            "Incorrect class attr for table: {}.".format("tablapanel")
        )
    return [ map_each_dolar(elem) for elem in table if elem ]



class DolarPricesSupplier(ScrapingSupplier):
    def __init__(self, cache_used):
        super().__init__(cache_used)
        self.url = Url.eco

    def get(self):
        data = cache.fetch_url(
            fetcher = fetch.FetchReqGet(Url.eco, headers={}),
            response_mapping = response_mapping_dolar,
            cache=self.cache_used,
            path = cache.url_to_cache_path(self.url)
        )

        df = get_dolar_table(data)
        df.set_index('Especie', inplace=True)
        df.index.name=None
        df['Último'] = df['Último'].str.replace(',', '.').astype(float)
        return df
