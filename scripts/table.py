import argparse
import sys
from src import fetch
from src import soup
from src import table


#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')


def print_help(cmd):
    print("usage: {} URL TABLE_NAME".format(cmd))

def run(url, table_name):
    print("url: {} table: {}".format(url, table_name))
    tab = table.Tabla(url, None, None, table_name,  "thead", "tbdoy")
    data = tab.fetch(0)
    print(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch a table')
    parser.add_argument('-q', '--query')
    parser.add_argument('-b', '--body')
    parser.add_argument('-c', '--ncols', type=int)
    parser.add_argument('rest', nargs=2)
    args = parser.parse_args()
    query = None if not args.query else args.query.split("=")
    body = "tbody" if not args.body else args.body

    tab = table.Tabla(
        base_url=args.rest[0],
        query=query,
        container=None,
        table_class=args.rest[1],
        header= "thead",
        body=body,
        ncols=args.ncols
    )
    
    print(tab.get_url())
    data = tab.fetch(0)
    print(data)
