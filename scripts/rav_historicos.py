import json
import pandas as pd
import sys
from src import cache
from scripts import rav

one_day = 60 * 60 * 24

def run(symb):
    print(rav.get_df(symb))

if __name__ == "__main__":
    for symb in sys.argv[1:]:
        run(symb)
