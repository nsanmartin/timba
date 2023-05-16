import sys
import pandas as pd
import json
from timba.src import cache
from timba.src import soup
from timba.scraping.www_rava_com__ import \
        response_mapping_flujofondos as response_mapping

one_day = 60 * 60 * 24
one_year = one_day * 365


def run(symb):
    df = cache.fetch_url_get(
        url='https://www.rava.com/perfil/' + symb,
        headers={},
        response_mapping=response_mapping,
        expiration=one_year * 3
    )

    print (df)
    print(df.sum(axis=0, numeric_only=True))

if __name__ == "__main__":
    for symb in sys.argv[1:]:
        run(symb)


