from collections import OrderedDict
import pandas as pd
import numpy as np
import argparse
import sys
from timba.src import fetch, soup, table, cache, time
import timba.scraping.bonos_ecovalores_com_ar as scraping_mod
from scripts import utils
from urllib.parse import urlparse


if __name__ == '__main__':
    args = utils.parse_args_artous()
    expiration = utils.get_expiration(11, 18, args)

    df = utils.get_bonds_table(scraping_mod, cache.CacheFile(expiration))


    symbs = list(map(lambda s: s.upper(), OrderedDict.fromkeys(args.rest)))
    if any([s for s in symbs if s not in df.index]):
        raise RuntimeError("Invalid symbol name in {}". format(symbs))

    if len(symbs) > 1:
        ratios = pd.DataFrame(index=symbs, columns=symbs)

        for i,s in enumerate(symbs):
            for t in symbs[i:]:
                pass
                ratios.loc[s,t] = df.loc[s,'Precio'] / df.loc[t,'Precio']
                #ratios.iloc[i,j] = df.iloc[i,0] / df.iloc[j,0]
                #ratios.iloc[i,j] = df.iloc[s,0] / df.iloc[t,0]


        ratios = ratios.astype(float).round(3)
        np.fill_diagonal(ratios.values, 1)
        print(df.loc[symbs])
        print(ratios)
    else:
        print(df)
