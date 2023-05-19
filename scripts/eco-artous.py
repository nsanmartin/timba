import pandas as pd
import argparse
import sys
from timba.src import fetch
from timba.src import soup
from timba.src import table
from timba.src import cache
from timba.scraping.bonos_ecovalores_com_ar import DolarPricesSupplier, Url
from urllib.parse import urlparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch a table')
    parser.add_argument('-e', '--expiration', type=int, default=60*60)
    parser.add_argument('rest', nargs='*')
    args = parser.parse_args()

    df = DolarPricesSupplier(cache.CacheFile(args.expiration))         \
        .get()                                                         \
        .get_data_acting_if_downloaded(               
            lambda : print("Data downloaded from {}".format(Url.eco))
        )

    for r in args.rest:
        precio = float(r)
        print(precio)
        df['p/d'] = precio/df['Último']
        print(df)
