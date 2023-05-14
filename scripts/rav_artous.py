import argparse
import sys
import pandas as pd
import json
from src import cache
from src import soup

one_day = 60 * 60 * 24
one_year = one_day * 365

def response_mapping_rav_dolars(text):
    assert text
    page = soup.get_soup(text) 
    assert page
    main_layout = page.find("main-layout")
    dolares_p = page.find("dolares-p")
    assert dolares_p 
    res = dolares_p.attrs[':datos']
    assert res
    resJson = json.loads(res)
    assert(resJson)
    return(resJson)



def url_fetch_and_map(url, expiration, response_mapping):
    print(url)
    rava = cache.fetch_url_get(
        url=url,
        headers={},
        response_mapping=response_mapping,
        expiration=expiration
    )
    return rava

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch rava dolars')
    parser.add_argument('-e', '--expiration', type=int, default=1600)
    parser.add_argument('rest', nargs='*')
    args = parser.parse_args()

    rava = url_fetch_and_map(
            'https://www.rava.com/cotizaciones/dolares',
            args.expiration,
            response_mapping_rav_dolars
    )

    for r in args.rest:
        precio = float(r)
        print(precio)

        df = pd.DataFrame(rava['body'])
        df = df.drop(
            df.columns.difference(['ultimo', 'especie']), axis=1
        )

        df['p/d'] = precio/df['ultimo']
        print(df)

