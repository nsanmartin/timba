import argparse
import json
import pandas as pd
import sys
from timba.src import cache
from timba.src import DataFrame as tdf
import matplotlib.pyplot as plt

one_day = 60 * 60 * 24

def idfun(x): return x

def run(symbs, tail, expiration):
    ls = [ cache.fetch_yf_download(s, idfun, expiration) for s in symbs ]
    for df,symb in zip(ls,symbs):
        df['Symb'] = symb

    print(ls)
    df = tdf.DataFrameSymbCmp.fromDataFrameList(ls)
    ratios =  df.getRatios()
    ratios.df.iloc[-tail:].plot()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch symbol')
    parser.add_argument('-p', '--plot', action='store_true')
    parser.add_argument('rest', nargs='+')
    parser.add_argument('-t', '--tail', type=int, default=0)
    parser.add_argument('-e', '--expiration', type=int, default=one_day)
    args = parser.parse_args()
    symbs = set(args.rest)

    if len(symbs) < 2:
        print("At least 2 symbols are needed to compare")
        print("Given: {}".format(sys.argv[1:]))
    else:
        run(symbs, args.tail, args.expiration)
