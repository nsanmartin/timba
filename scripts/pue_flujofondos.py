
import json
import pandas as pd
import sys
from timba.src import cache
from urllib.parse import urlparse
import datetime as dt

one_day = 60 * 60 * 24

def response_mapping(text):
    assert text
    resJson = json.loads(text)
    assert(resJson)
    mapFlujosDTO = resJson['mapFlujosDTO']
    assert mapFlujosDTO
    return [pd.DataFrame(v) for k, v in mapFlujosDTO.items()][0]



def run(symb):
    endpoint = 'https://www.puentenet.com/herramientas/flujo-de-fondos/calcular' 
    data = '{ \"BONO_' + symb + '\": \"100\"}'
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Accept': 'application/json, text/plain, */*' ,
        'Accept-Encoding': 'gzip, deflate, br' ,
        'Content-Type': 'application/json;charset=utf-8' ,
        'Origin': 'https://www.puentenet.com' ,
        'Referer': 'https://www.puentenet.com/herramientas/flujo-de-fondos/' 
    }
    headers.update(cache.get_headers_for(urlparse(endpoint).netloc))
    df = cache.fetch_url_post(
        file=symb,
        endpoint=endpoint,
        headers=headers,
        data=data,
        response_mapping=response_mapping,
        expiration=one_day * 365
    )
    print(df)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Symb is missing.")
    for symb in sys.argv[1:]:
        run(symb)

