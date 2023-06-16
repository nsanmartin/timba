import requests, json
import pandas as pd

artous = 'https://artous.onrender.com/pong'
artous = 'http://localhost:5001/pong'


if __name__ == "__main__":
    r = requests.get(artous)
    txt = r.text
    print(txt)
    x = json.loads(txt)
    print(x)

