# deprecated
# run this with
# $ python -m scripts.table ...
# from timba/

import argparse
import sys
from timba.src import fetch
from timba.src import soup
from timba.src import table
from timba.src import cache
from urllib.parse import urlparse

def print_help(cmd):
    print("usage: {} URL TABLE_NAME".format(cmd))

<<<<<<< Updated upstream:scripts/fetch_table.py
def run(url, table_name):
    print("url: {} table: {}".format(url, table_name))
    tab = table.Tabla(url, None, None, table_name,  "thead", "tbdoy")
    data = tab.fetch(0)

=======
## def run(url, table_name):
##     print("url: {} table: {}".format(url, table_name))
##     tab = table.Tabla(url, None, None, table_name,  "thead", "tbdoy")
##     data = tab.fetch(0)
##     print(data)
>>>>>>> Stashed changes:scripts/table.py

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch a table')
    parser.add_argument('-q', '--query')
    parser.add_argument('-b', '--body')
    parser.add_argument('-C', '--container')
    parser.add_argument('-c', '--ncols', type=int)
    parser.add_argument('-H', '--header_index', type=int, default=0)
    parser.add_argument('-e', '--expiration', type=int, default=60*60)
    parser.add_argument('rest', nargs=2)
    args = parser.parse_args()
    query = None if not args.query else args.query.split("=")
    container = None if not args.container else args.container.split(",")
    body = "tbdoy" if not args.body else args.body
    
    tab = table.Tabla(
        base_url=args.rest[0],
        query=query,
        container=container,
        table_class=args.rest[1],
        header= "thead",
        body=body,
        ncols=args.ncols
    )
    
<<<<<<< Updated upstream:scripts/fetch_table.py
    headers = cache.get_headers_for(urlparse(tab.get_url()).netloc)
    data = tab.fetch(args.header_index, headers, args.expiration)
    print(data)
=======
    #print(tab.get_url())
    data = tab.fetch(args.header_index)
    #print(data)
>>>>>>> Stashed changes:scripts/table.py
