import sys
import pandas as pd
import json
from src import cache
from src import soup

def run(symb):
    text = cache.get_url('https://www.rava.com/perfil/' + symb, 10000)
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
    print (df)

if __name__ == "__main__":
    for symb in sys.argv[1:]:
        run(symb)


