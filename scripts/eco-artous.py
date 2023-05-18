import argparse
from bs4 import BeautifulSoup
import pandas as pd
import sys
from timba.src import fetch
from timba.src import soup
from timba.src import table
from timba.src import cache
from urllib.parse import urlparse

def map_each(elem):
    try:
        header = soup.head_rows_to_list(elem)[0]
        body = soup.data_rows_to_list(elem)
        return pd.DataFrame(body, columns=header)
    except ValueError:
        return None


def response_mapping(text):
    html = BeautifulSoup(text, "lxml")
    table = html.find_all("table", attrs={"class": "tablapanel"})

    if not table:
        raise RuntimeError(
            "Incorrect class attr for table: {}.".format("tablapanel")
        )
    return [ map_each(elem) for elem in table if elem ]


def get_artous_table(data):
    for df in data:
        try:
            if 'Especie' in df.columns \
                and df['Especie'].str.contains('Dólar').any():
                df.dropna(inplace=True)
                return df
        except Exception:
            pass
    raise RuntimeError("Table not found in ecovalores")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch a table')
    parser.add_argument('-e', '--expiration', type=int, default=60*60)
    parser.add_argument('rest', nargs='*')
    args = parser.parse_args()

    url = "https://bonos.ecovalores.com.ar/eco/"

    data = cache.fetch_url(
        fetcher = fetch.FetchReqGet(url, headers={}),
        response_mapping = response_mapping,
        cache=cache.CacheFile(args.expiration),
        path = cache.url_to_cache_path(url)
    )

    df = get_artous_table(data)
    df.set_index('Especie', inplace=True)
    df.index.name=None
    df['Último'] = df['Último'].str.replace(',', '.').astype(float)

    for r in args.rest:
        precio = float(r)
        print(precio)
        df['p/d'] = precio/df['Último']
        print(df)
