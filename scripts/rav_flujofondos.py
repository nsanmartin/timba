import argparse
import sys
import pandas as pd
import json
from timba.src import cache, fetch
from timba.src import soup
from timba.scraping.www_rava_com import \
        response_mapping_flujofondos as response_mapping

one_day = 60 * 60 * 24
one_year = one_day * 365


def run(symb, expiration):
    url = 'https://www.rava.com/perfil/' + symb
    path = cache.url_to_cache_path(url)
    df = cache.fetch_url(
        fetcher = fetch.FetchReqGet(url, headers={}),
        response_mapping=response_mapping,
        cache=cache.CacheFile(expiration),
        path=path
    ).get_data_acting_if_downloaded(               
        lambda : print("Data downloaded from {}".format(url))
    )

    print (df)
    print(df.sum(axis=0, numeric_only=True))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rava Flujo Fondos')
    parser.add_argument('rest', nargs='+')
    parser.add_argument('-e', '--expiration', type=int, default=one_day * 3)
    args = parser.parse_args()

    for symb in args.rest:
        run(symb, args.expiration)


