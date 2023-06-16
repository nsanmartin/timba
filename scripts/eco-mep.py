import numpy as np
import pandas as pd
import argparse
import sys
from timba.src import fetch, soup, table, cache, time
import timba.scraping.bonos_ecovalores_com_ar as scraping_mod
from scripts import utils
from urllib.parse import urlparse


if __name__ == '__main__':
    args = utils.parse_args_artous()
    expiration = utils.get_expiration(11, 18, args)

    df = utils.get_dolar_mep_table(scraping_mod, cache.CacheFile(expiration))
    u  = df['Último']

    dolares = (df.index[df.index.str.len() == 4] + 'D')\
        .intersection(df.index)
    pesos = dolares.map(lambda s: s.rstrip('D'))
    ratios = u.loc[pesos] / u.loc[dolares].values
    preciop = u.loc[pesos]
    preciod = u.loc[dolares]
    preciod.index = preciop.index

    norm = ratios/ ratios.min()
    res = pd.DataFrame(
        {'ratios': ratios, 'norm': norm, 'pesos': preciop, 'dolares':preciod}
    )
    print(res)
    print(f'promedio: {ratios.mean().round(2)}')
    print(f'min: {ratios.min().round(2)}')
    print(f'max: {ratios.max().round(3)} ({(100*(norm.max()-1)).round(2)}%)')

