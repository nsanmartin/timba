from collections import OrderedDict
import argparse
import json
import pandas as pd
import sys
from timba.src import cache, fetch
from timba.src import data_frame as tdf
import matplotlib.pyplot as plt

one_day = 60 * 60 * 24

def idfun(x): return x

def run(symbs, tail, expiration):
    dfCache = cache.CacheDataFrame(expiration)
    ls = [
        cache.fetch_url(
            fetcher = fetch.FetchDataYf(s),
            response_mapping = idfun,
            cache = dfCache,
            path = cache.url_to_cache_path("yf/download/" + s)
        ).get_data_acting_if_downloaded(               
            lambda : print("Data for {} downloaded from yf".format(s))
        )
        for s in symbs
    ]

    for df,symb in zip(ls,symbs):
        df['Symb'] = symb

    print(ls)
    df = tdf.DataFrameSymbCmp.fromDataFrameList(ls)
    ratios =  df.getRatios()
    x = ratios.df.iloc[-tail:]
    x.plot()
    if len(symbs) == 2:
        mn = x.min()[0]
        mx = x.max()[0]
        mean = x.mean()[0]
        sd = x.std()[0]
        last = x.iloc[-1,0]
        dist = last-mean
        z = dist/sd
        plt.axhline(mn)
        plt.axhline(mx)
        plt.axhline(mean)
        plt.axhline(last, c='red')
        print("tail:\n{}".format(x.tail()))
        print((
            "min: {:.3f}, max: {:.3f}, mean: {:.3f}, sd: {:.3f}, Z: {:.3f}"
            + ", dist: {:.3f}."
            ).format(mn, mx, mean, sd, z, dist)
        )
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch symbol')
    parser.add_argument('-p', '--plot', action='store_true')
    parser.add_argument('rest', nargs='+')
    parser.add_argument('-t', '--tail', type=int, default=0)
    parser.add_argument('-e', '--expiration', type=int, default=one_day)
    args = parser.parse_args()
    symbs = list(OrderedDict.fromkeys(args.rest))

    if len(symbs) < 2:
        print("At least 2 symbols are needed to compare")
        print("Given: {}".format(sys.argv[1:]))
    else:
        run(symbs, args.tail, args.expiration)
