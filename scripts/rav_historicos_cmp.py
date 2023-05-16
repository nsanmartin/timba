import json
import pandas as pd
import sys
from timba.src import cache
from scripts import rav_historicos
from timba.src import DataFrame as tdf
import matplotlib.pyplot as plt

from timba.scraping.www_rava_com__ import \
    response_mapping_historicos as response_mapping

one_day = 60 * 60 * 24


def run(symbs):
    ls = [
        rav_historicos.get_df(s, response_mapping) for s in symbs
    ]

    df = tdf.DataFrameSymbCmp.fromDataFrameList(ls)
    ratios =  df.getRatios()
    ratios.df.plot()
    plt.show()


if __name__ == "__main__":
    symbs = set(sys.argv[1:])
    if len(symbs) < 2:
        print("At least 2 symbols are needed to compare")
        print("Given: {}".format(sys.argv[1:]))
    else:
        run(symbs)
