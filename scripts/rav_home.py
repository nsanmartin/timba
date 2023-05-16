from timba.src import cache
from timba.src import soup
from timba.scraping.www_rava_com__ import \
    response_mapping_home as response_mapping
import argparse
import json
import pandas as pd
import sys

one_day = 60 * 60 * 24
one_year = one_day * 365



def get_rava(expiration):
    print("rava home")
    rava = cache.fetch_url_get(
        url='https://www.rava.com/',
        headers={},
        response_mapping=response_mapping,
        expiration=expiration
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



