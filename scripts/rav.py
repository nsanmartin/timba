import json
import pandas as pd
import sys
from src import cache
from urllib.parse import urlparse
import datetime as dt

one_day = 60 * 60 * 24

def get_df(symb):
    endpoint = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"
    data = {
        'especie': symb,
        'fecha_inicio': "0000-00-00",
        'fecha_fin': dt.datetime.today().strftime("%Y-%m-%d")
    }
    data.update(cache.get_data_for(urlparse(endpoint).netloc))
    src, text = cache.get_post(symb, endpoint, data, {}, one_day)
    try:
        assert text
        resJson = json.loads(text)
        assert(resJson)
        return pd.DataFrame(resJson['body'])
    except Exception as e:
        raise RuntimeError("error fetching " + symb + " from source:\n\n" + src) from e


