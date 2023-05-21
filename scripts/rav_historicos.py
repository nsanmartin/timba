from timba.src import cache, fetch
from timba.scraping.www_rava_com import \
    response_mapping_historicos as response_mapping
from urllib.parse import urlparse
import argparse
import datetime as dt
import json
import matplotlib.pyplot as plt
import sys

one_day = 60 * 60 * 24


def get_df(symb, response_mapping, expiration=one_day):
    endpoint = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"
    data = {
        'especie': symb,
        'fecha_inicio': "0000-00-00",
        'fecha_fin': dt.datetime.today().strftime("%Y-%m-%d")
    }
    data.update(cache.get_data_for(urlparse(endpoint).netloc))

    path = cache.url_to_cache_path(endpoint + "/" + symb)
    df = cache.fetch_url(
        fetcher = fetch.FetchReqPost(endpoint, path, {}, data),
        response_mapping = response_mapping,
        cache = cache.CacheFile(expiration),
        path = path
    ).get_data_acting_if_downloaded(               
        lambda : print("Data downloaded from {}".format(endpoint))
    )
    return(df)

def run(symb, plot, tail, expiration):
    df = get_df(symb, response_mapping, expiration)
    df = df.df.iloc[-tail:]
    if plot:
        df['Close'].plot()
        plt.title(symb)
        plt.show()
    else:
        print(df)

description = 'Fetch symbol from rava.' 
epilog = "access_token must be set in timba's dir " \
        + "(default is $HOME/.timba/data/clasico.rava.com)."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('-p', '--plot', action='store_true')
    parser.add_argument('rest', nargs='+')
    parser.add_argument('-t', '--tail', type=int, default=0)
    parser.add_argument('-e', '--expiration', type=int, default=one_day)
    args = parser.parse_args()

    for symb in args.rest:
        run(symb, args.plot, args.tail, args.expiration)
