
import json
import pandas as pd
import sys
from timba.src import cache, fetch
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

    path = cache.url_to_cache_path(endpoint + "/" + symb)
    df = cache.fetch_url(
        fetcher=fetch.FetchReqPost(endpoint, path, headers, data),
        response_mapping=response_mapping,
        cache = cache.CacheFile(one_day * 365),
        path=path
    )
    print(df)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Symb is missing.")
    for symb in sys.argv[1:]:
        run(symb)

