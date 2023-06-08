import argparse
from timba.src import cache, fetch, time

def parse_args_artous():
    parser = argparse.ArgumentParser(description='Fetch rava dolars')
    parser.add_argument('-e', '--expiration', type=int, default=1600)
    parser.add_argument(
        '--testing', default=False, action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        '-f',
        '--force-download',
        default=False,
        action=argparse.BooleanOptionalAction
    )
    parser.add_argument('rest', nargs='*')
    return parser.parse_args()

def get_expiration(open_time, close_time, args):
    return time.ExpirationOpened(11, 18)                                  \
            .get_expiration(time.get_bsas_time(), args.expiration)        \
            if not args.force_download else 0

def get_dolar_table(scraping_mod, cache_used):
    return scraping_mod.DolarPricesSupplier(cache_used)                    \
        .get()                                                            \
        .get_data_acting_if_downloaded(               
            lambda : print("Data downloaded from {}".format(
                    scraping_mod.Url.artous
                )
            )
        )

def get_bonds_table (scraping_mod, cache_used):
    return scraping_mod.BondsPricesSupplier(cache_used)                    \
        .get()                                                            \
        .get_data_acting_if_downloaded(               
            lambda : print("Bonds data downloaded from {}".format(
                    scraping_mod.Url.bonos_listado
                )
            )
        )
