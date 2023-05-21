from timba.scraping import  ScrapingSupplier
from timba.src import soup, fetch, cache
import pandas as pd
from bs4 import BeautifulSoup

class Url:
    home = "https://dolarhoy.com/"
    artous = home



def map_each_dolar(elem):
    try:
        a = elem.find("a", attrs={"class": "title"})
        compra = elem.find( "div", attrs={"class": "compra"})\
                .find("div",attrs={"class": "val"})
        venta = elem.find("div", attrs={"class": "venta"})\
                .find("div",attrs={"class": "val"})
        #todo return two rows
        return {'Especie':a.text, 'operación': compra.text, 'precio': venta.text}
    except Exception:
        return None


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
    dls = [ r for d in dls if (r := map_each_dolar(d)) is not None ]
    dls = { (r['Especie'] + r['operación']):r for r in dls }
    table = pd.DataFrame(dls.values())
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
        df = res.data
        df.set_index('Especie', inplace=True)
        df.index.name=None
        df['precio'] = df['precio'].str.replace('$', '').astype(float)
        res.data = df
        return res
