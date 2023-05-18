import argparse
import sys
import pandas as pd
from timba.src import cache, fetch
from timba.scraping.www_rava_com__ import get_dolar_prices

one_day = 60 * 60 * 24
one_year = one_day * 365


def run_cache_file(url, args, c):
    df = get_dolar_prices(c)

    for r in args.rest:
        precio = float(r)
        print(precio)
        df['p/d'] = precio/df['ultimo']
        print(df)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch rava dolars')
    parser.add_argument('-e', '--expiration', type=int, default=1600)
    parser.add_argument('--testing', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('rest', nargs='*')
    args = parser.parse_args()

    url = 'https://www.rava.com/cotizaciones/dolares'

    if args.testing:
        for _ in range(4):
            c = cache.CacheMem(args.expiration)
            run_cache_file(url, args, c)
        
    else:
        c = cache.CacheFile(args.expiration)
        run_cache_file(url, args, c)
