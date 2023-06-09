from collections import OrderedDict
from scripts import rav_historicos, utils
from timba.src import DataFrame as tdf
from timba.src import cache
import argparse
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys

from timba.scraping.www_rava_com import \
    response_mapping_historicos as response_mapping

one_day = 60 * 60 * 24


def run(symbs, tail, expiration):
    ls = [
        rav_historicos.get_df(s, response_mapping, expiration)
        for s in symbs
    ]

    df = tdf.DataFrameSymbCmp.fromDataFrameIxList(ls)
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
    parser.add_argument('rest', nargs='+')
    parser.add_argument('-t', '--tail', type=int, default=0)
    parser.add_argument('-e', '--expiration', type=int, default=one_day)
    args = parser.parse_args()
    args.rest = list(map(lambda x: x.upper(), OrderedDict.fromkeys(args.rest)))
    symbs = args.rest

    if len(symbs) < 2:
        print("At least 2 symbols are needed to compare")
        print("Given: {}".format(symbs))
    else:
        print(symbs)
        run(symbs, args.tail, args.expiration)
