from src import cache
from urllib.parse import urlparse
import datetime as dt
import json
import pandas as pd
import sys

one_day = 60 * 60 * 24

def response_mapping(text):
    assert text
    resJson = json.loads(text)
    assert(resJson)
    return pd.DataFrame(resJson['body'])


def get_df(symb):
    endpoint = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"
    data = {
        'especie': symb,
        'fecha_inicio': "0000-00-00",
        'fecha_fin': dt.datetime.today().strftime("%Y-%m-%d")
    }
    data.update(cache.get_data_for(urlparse(endpoint).netloc))
    df = cache.fetch_url_post(
        file=symb,
        endpoint=endpoint,
        headers={},
        data=data,
        response_mapping=response_mapping,
        expiration=one_day
    )
    return(df)

def run(symb):
    print(get_df(symb))

if __name__ == "__main__":
    for symb in sys.argv[1:]:
        run(symb)
