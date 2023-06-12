import argparse
from timba.src import time as tb_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Is open?')
    parser.add_argument('-o', '--open', type=int, default=0)
    parser.add_argument('-c', '--close', type=int, default=24)
    args = parser.parse_args()

    bs_time = tb_time.get_bsas_time()
    print(f'now {bs_time}')

    expiration = tb_time.ExpirationOpened(args.open, args.close) \
        .get_expiration(tb_time.get_bsas_time(), 0) 

    print(f'expiration: {expiration}')

    if expiration == 0:
        print(True)
    else:
        print(False)
