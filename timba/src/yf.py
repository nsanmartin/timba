from timba.src import fetch, cache
from timba.src import time as tb_time

import timba as tb

default_expiration = tb_time.one_day

def get_cached(symb, expiration=default_expiration):
    path = cache.url_to_cache_path("yf/download/" + symb)

    return cache.fetch_url(
        fetcher = fetch.FetchDataYf(symb),
        response_mapping = tb.data_frame.DataFrameDateIx.fromDataFrame,
        cache = cache.CacheDataFrame(expiration),
        path = path
    ).get_data_acting_if_downloaded(               
        lambda : print("Data for {} downloaded from yf".format(symb))
    )

