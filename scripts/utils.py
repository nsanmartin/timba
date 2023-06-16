import argparse
from timba.src import cache, fetch, time

class CliArgs:
    def __init__(self, desc, def_exp):
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument('-e', '--expiration', type=int, default=def_exp)
        parser.add_argument(
            '-f',
            '--force-download',
            default=False,
            action=argparse.BooleanOptionalAction
        )
        parser.add_argument(
            '--testing', default=False, action=argparse.BooleanOptionalAction
        )
        parser.add_argument('rest', nargs='*')
        self.parser = parser

    def parse_args(self):
        return self.parser.parse_args()

class CliHistArgs(CliArgs):
    def __init__(self, desc):
        super().__init__(desc, time.one_day)
        self.parser.add_argument('-p', '--plot', action='store_true')
        self.parser.add_argument('rest', nargs='+')
        self.parser.add_argument('-t', '--tail', type=int, default=0)
        self.parser.add_argument('-d', '--dates')

def parse_args_artous():
    parser = CliArgs('Fetch rava dolars', 1600)
    return parser.parse_args()

def get_expiration(open_time, close_time, args):
    return time.ExpirationOpened(11, 18)                                  \
            .get_expiration(time.get_bsas_time(), args.expiration)        \
            if not args.force_download else 0

def get_dolar_mep_table(scraping_mod, cache_used):
    return scraping_mod.DolarMepSupplier(cache_used)                   \
        .get()                                                            \
        .get_data_acting_if_downloaded(               
            lambda : print("Data downloaded from {}".format(
                    scraping_mod.Url.artous
                )
            )
        )
def get_dolar_table(scraping_mod, cache_used):
    return scraping_mod.DolarPricesSupplier(cache_used)                   \
        .get()                                                            \
        .get_data_acting_if_downloaded(               
            lambda : print("Data downloaded from {}".format(
                    scraping_mod.Url.artous
                )
            )
        )

def get_bonds_table (scraping_mod, cache_used):
    return scraping_mod.BondsPricesSupplier(cache_used)                   \
        .get()                                                            \
        .get_data_acting_if_downloaded(               
            lambda : print("Bonds data downloaded from {}".format(
                    scraping_mod.Url.bonos_listado
                )
            )
        )
