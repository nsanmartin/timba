from timba.scraping import  ScrapingSupplier
from timba.src import data_frame as tdf
from timba.src import soup, fetch, cache
from timba.src import time as tb_time
from urllib.parse import urlparse
import json
import datetime as dt
import pandas as pd

class Url:
    dolars = 'https://www.rava.com/cotizaciones/dolares'
    artous = dolars
    historicos = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"


def response_mapping_home(text):
    assert text
    page = soup.get_soup(text) 
    assert page
    perfil_p = page.find("home-p")
    assert perfil_p
    res = perfil_p.attrs[':res']
    assert res
    resJson = json.loads(res)
    assert(resJson)
    return(resJson)


def response_mapping_historicos(text):
    assert text
    resJson = json.loads(text)
    assert(resJson)
    return tdf.DataFrameDateIx.fromDataFrame(
        pd.DataFrame(resJson['body'])
    )


def response_mapping_flujofondos(text):
    assert text
    page = soup.get_soup(text) 
    assert page
    perfil_p = page.find("perfil-p")
    assert perfil_p
    res = perfil_p.attrs[':res']
    assert res
    resJson = json.loads(res)
    assert(resJson)
    resList = resJson['flujofondos']
    assert(resList)
    flujofondos = resList['flujofondos']
    df = pd.DataFrame(flujofondos)
    df.fillna(0, inplace=True)
    return df

def response_mapping_cotizaciones_dolares(text):
    assert text
    page = soup.get_soup(text) 
    assert page
    main_layout = page.find("main-layout")
    dolares_p = page.find("dolares-p")
    assert dolares_p 
    res = dolares_p.attrs[':datos']
    assert res
    resJson = json.loads(res)
    assert(resJson)
    return(resJson)


class DolarPricesSupplier(ScrapingSupplier):
    def __init__(self, cache_used):
        super().__init__(cache_used)
        self.url = Url.dolars

    def get(self):
        res = cache.fetch_url(
            fetcher = fetch.FetchReqGet(self.url, headers={}),
            response_mapping = response_mapping_cotizaciones_dolares,
            cache = self.cache_used,
            path = cache.url_to_cache_path(self.url)
        )

        df = pd.DataFrame(res.data['body'])
        df = df.drop( df.columns.difference(['ultimo', 'especie']), axis=1)
        df.set_index('especie', inplace=True)
        df.index.name = None
        res.data = df
        return res

def get_historicos(symb, expiration=tb_time.one_day):
    data = {
        'especie': symb,
        'fecha_inicio': "0000-00-00",
        'fecha_fin': dt.datetime.today().strftime("%Y-%m-%d")
    }
    data.update(cache.get_data_for(urlparse(Url.historicos).netloc))

    path = cache.url_to_cache_path(Url.historicos + "/" + symb)
    df = cache.fetch_url(
        fetcher = fetch.FetchReqPost(Url.historicos, path, {}, data),
        response_mapping = response_mapping_historicos,
        cache = cache.CacheFile(expiration),
        path = path
    ).get_data_acting_if_downloaded(               
        lambda : print("Data downloaded from {}".format(Url.historicos))
    )
    return(df)

def dolar_mep(name):
    name = name.upper()
    p = get_historicos(name)
    d = get_historicos(name + 'D')

    return p.df['Close'] / d.df['Close'], p, d

