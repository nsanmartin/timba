from timba.src import DataFrame as tdf
from timba.src import soup, fetch, cache
import json
import pandas as pd

class Url:
    dolars = 'https://www.rava.com/cotizaciones/dolares'


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


def get_dolar_prices(cache_used):
    rava = cache.fetch_url(
        fetcher = fetch.FetchReqGet(Url.dolars, headers={}),
        response_mapping = response_mapping_cotizaciones_dolares,
        cache = cache_used,
        path = cache.url_to_cache_path(Url.dolars)
    )

    df = pd.DataFrame(rava['body'])
    df = df.drop( df.columns.difference(['ultimo', 'especie']), axis=1)
    df.set_index('especie', inplace=True)
    df.index.name = None
    return df

