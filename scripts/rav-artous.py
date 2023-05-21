import scripts.utils as utils
import sys
import pandas as pd
from timba.src import cache, fetch, time
import timba.scraping.www_rava_com as scraping_mod

def run_cache_file(args, c):
    df = utils.get_dolar_table(scraping_mod, c)

    for r in args.rest:
        precio = float(r)
        print(precio)
        df['p/d'] = precio/df['ultimo']
        print(df)



if __name__ == "__main__":
    args = utils.parse_args_artous()
    expiration = utils.get_expiration(11, 18, args)


    if args.testing:
        c = cache.CacheMem(0)
        run_cache_file(args, c)
        for _ in range(3):
            c = cache.CacheMem(time.one_day)
            run_cache_file(args, c)
        
    else:
        c = cache.CacheFile(expiration)
        run_cache_file(args, c)
