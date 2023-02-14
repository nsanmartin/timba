import sys
import pandas as pd
import json
from src import cache
from src import soup

one_day = 60 * 60 * 24
one_year = one_day * 365

def response_mapping(text):
    assert text
    page = soup.get_soup(text) 
    assert page
    perfil_p = page.find("perfil-p")
    assert perfil_p
    res = perfil_p.attrs[':res']
    assert res
    resJson = json.loads(res)
    assert(resJson)
    resList = resJson['flujofondos']
    assert(resList)
    flujofondos = resList['flujofondos']
    df = pd.DataFrame(flujofondos)
    df.fillna(0, inplace=True)
    return df


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


