import argparse
import json
import pandas as pd
import sys
from timba.src import cache, fetch
from scripts import rav_historicos
from timba.src import data_frame as tdf
import matplotlib.pyplot as plt
import timba as tb

one_day = 60 * 60 * 24

def run(symb, plot, tail, expiration):
    df = tb.yf.get_cached(symb)
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
