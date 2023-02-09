import json
import pandas as pd
import sys
from src import cache
from scripts import rav
from src import DataFrame as tdf
import matplotlib.pyplot as plt

one_day = 60 * 60 * 24


def run(symbs):
    ls = [  rav.get_df(s) for s in symbs ]
    df = tdf.DataFrameSymbCmp.fromDataFrameList(ls)
    ratios =  df.getRatios()
    ratios.df.plot()
    plt.show()


if __name__ == "__main__":
    run(sys.argv[1:])
