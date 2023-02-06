import sys
import pandas as pd
import json
from src import fetch

def run(symb):
    x = fetch.web_page_soup('https://www.rava.com/perfil/' + symb)
    assert x
    perfil_p = x.find("perfil-p")
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


