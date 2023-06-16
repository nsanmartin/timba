from timba.src import fetch, cache
import timba as tb

default_expiration = tb.time.one_day

def run(symb, expiration=default_expiration):
    path = cache.url_to_cache_path("yf/download/" + symb)

    return cache.fetch_url(
        fetcher = fetch.FetchDataYf(symb),
        response_mapping = response_mapping_yf,
        cache = cache.CacheDataFrame(expiration),
        path = path
    ).get_data_acting_if_downloaded(               
        lambda : print("Data for {} downloaded from yf".format(symb))
    )

