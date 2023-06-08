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
    mn = x.min()[0]
    mx = x.max()[0]
    plt.axhline(mn)
    plt.axhline(mx)
    print("tail:\n{}".format(x.tail()))
    print("min: {}, max: {}.".format(mn, mx))
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch symbol')
    parser.add_argument('rest', nargs='+')
    parser.add_argument('-t', '--tail', type=int, default=0)
    parser.add_argument('-e', '--expiration', type=int, default=one_day)
    args = parser.parse_args()
    symbs = list(OrderedDict.fromkeys(args.rest))

    if len(symbs) < 2:
        print("At least 2 symbols are needed to compare")
        print("Given: {}".format(symbs))
    else:
        print(symbs)
        run(symbs, args.tail, args.expiration)
