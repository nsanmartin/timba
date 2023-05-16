import argparse
import json
import pandas as pd
import sys
from timba.src import cache
from scripts import rav_historicos
from timba.src import DataFrame as tdf
import matplotlib.pyplot as plt

one_day = 60 * 60 * 24

def response_mapping_yf(df):
    df = tdf.DataFrameDateIx.fromDataFrame(df)
    return df

def run(symb, plot, tail, expiration):
    df = cache.fetch_yf_download(symb, expiration, response_mapping_yf)
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

    for symb in args.rest:
        run(symb, args.plot, args.tail, args.expiration)
