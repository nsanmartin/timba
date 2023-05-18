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


def get_dolar_table(data):
    for df in data:
        try:
            if 'Especie' in df.columns \
                and df['Especie'].str.contains('Dólar').any():
                df.dropna(inplace=True)
                return df
        except Exception:
            pass
    raise RuntimeError("Table not found in ecovalores")


def fetch_dolar_prices(cache_used):
    data = cache.fetch_url(
        fetcher = fetch.FetchReqGet(Url.eco, headers={}),
        response_mapping = response_mapping_dolar,
        cache=cache_used,
        path = cache.url_to_cache_path(Url.eco)
    )

    df = get_dolar_table(data)
    df.set_index('Especie', inplace=True)
    df.index.name=None
    df['Último'] = df['Último'].str.replace(',', '.').astype(float)
    return df