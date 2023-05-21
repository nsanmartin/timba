from functools import reduce
from timba.scraping import  ScrapingSupplier
from timba.src import soup, fetch, cache
import pandas as pd
from bs4 import BeautifulSoup

class Url:
    home = "https://dolarhoy.com/"
    artous = home


def parse_val(text):
    return  text.str.replace('$', '').astype(float)

def map_each_dolar(elem):
    try:
        a = elem.find("a", attrs={"class": "title"})
        compra = elem.find( "div", attrs={"class": "compra"})           \
                .find("div",attrs={"class": "val"})                     \
                .text.replace('$', '')
        venta = elem.find("div", attrs={"class": "venta"})              \
                .find("div",attrs={"class": "val"})                     \
                .text.replace('$', '')
        return [
            {'Especie':a.text + ' compra', 'último': compra},
            {'Especie':a.text + ' venta', 'último': venta},
        ]
    except Exception as e:
        return None

def reduce_helper(rec, x):
    m = map_each_dolar(x)
    if m:
        for r in m: 
                rec[r['Especie']] = r
    return rec 


def response_mapping_dolar(text):
    html = BeautifulSoup(text, "lxml")
    section = html.find("section", attrs={"class": "modulo__cotizaciones"})
    if not section:
        raise RuntimeError(
            "Incorrect class attr for section: {}.".format(
                "modulo_cotizaciones"
            )
        )

    dls = section.find_all("div", attrs={"class": ["tile", "is-child"]}) 
    dls = reduce(reduce_helper, dls, {})
    table = pd.DataFrame(dls.values())
    table.set_index('Especie', inplace=True)
    table.index.name=None
    table['último'] = table['último'].astype(float)
    return table




class DolarPricesSupplier(ScrapingSupplier):
    def __init__(self, cache_used):
        super().__init__(cache_used)
        self.url = Url.home

    def get(self):
        res = cache.fetch_url(
            fetcher = fetch.FetchReqGet(Url.home, headers={}),
            response_mapping = response_mapping_dolar,
            cache=self.cache_used,
            path = cache.url_to_cache_path(self.url)
        )
        return res
