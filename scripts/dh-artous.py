import pandas as pd
import argparse
import sys
from timba.src import fetch, soup, table, cache
from scripts import utils
import timba.scraping.dolarhoy_com as scrapping_mod
from urllib.parse import urlparse


if __name__ == '__main__':
    args = utils.parse_args_artous()
    expiration = utils.get_expiration(11, 18, args)
    df = utils.get_dolar_table(scrapping_mod, cache.CacheFile(expiration))

    for r in args.rest:
        precio = float(r)
        print(precio)
        #df['p/d'] = precio/df['Último']
        print(df)
