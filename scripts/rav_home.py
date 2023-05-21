from timba.src import cache, fetch
from timba.src import soup
from timba.scraping.www_rava_com import \
    response_mapping_home as response_mapping
import argparse
import json
import pandas as pd
import sys

one_day = 60 * 60 * 24
one_year = one_day * 365



def get_rava(expiration):
    print("rava home")
    url = 'https://www.rava.com/'

    rava = cache.fetch_url(
        fetcher = fetch.FetchReqGet(url, headers={}),
        response_mapping = response_mapping,
        cache = cache.CacheFile(expiration),
        path = cache.url_to_cache_path(url)
    ).get_data_acting_if_downloaded(               
        lambda : print("Data downloaded from {}".format(url))
    )
    return rava

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch rava home')
    parser.add_argument('-e', '--expiration', type=int, default=160)
    parser.add_argument('rest', nargs='*')
    args = parser.parse_args()

    rava = get_rava(args.expiration)
    if len(args.rest) == 0:
        for k,_ in rava.items():
            print(k)
    else:
        for k in args.rest:
            df = pd.DataFrame(rava[k]['body'])
            print(df)



