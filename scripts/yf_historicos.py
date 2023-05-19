import argparse
import json
import pandas as pd
import sys
from timba.src import cache, fetch
from scripts import rav_historicos
from timba.src import DataFrame as tdf
import matplotlib.pyplot as plt

one_day = 60 * 60 * 24

def response_mapping_yf(df):
    df = tdf.DataFrameDateIx.fromDataFrame(df)
    return df

def run(symb, plot, tail, expiration):
    path = cache.url_to_cache_path("yf/download/" + symb)

    df = cache.fetch_url(
        fetcher = fetch.FetchDataYf(symb),
        response_mapping = response_mapping_yf,
        cache = cache.CacheDataFrame(expiration),
        path = path
    ).get_data_acting_if_downloaded(               
        lambda : print("Data for {} downloaded from yf".format(symb))
    )

    df = df.df.iloc[-tail:]

    if plot:
        df.iloc[-tail:]['Close'].plot()
        plt.title(symb)
        plt.show()
    else:
        print(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch symbol')
    parser.add_argument('-p', '--plot', action='store_true')
    parser.add_argument('rest', nargs='+')
    parser.add_argument('-t', '--tail', type=int, default=0)
    parser.add_argument('-e', '--expiration', type=int, default=one_day)
    args = parser.parse_args()

    for symb in set(args.rest):
        run(symb, args.plot, args.tail, args.expiration)
