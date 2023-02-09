import json
import pandas as pd
import sys
from src import cache

one_day = 60 * 60 * 24

def run(symb):
    token = cache.get_bearer_token()
    data = { 'especie': symb, 'fecha_inicio': "0000-00-00", 'fecha_fin': "2023-02-08" }
    headers = { 'Authorization': 'Bearer ' + token }
    endpoint = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"
    text = cache.get_post(symb, endpoint, data, headers, one_day)
    assert text
    resJson = json.loads(text)
    assert(resJson)
    df = pd.DataFrame(resJson['body'])
    print(df)

if __name__ == "__main__":
    for symb in sys.argv[1:]:
        run(symb)
