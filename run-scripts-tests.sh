./run_script scripts/eco-artous.py 1 --testing \
    && ./run_script scripts/dh-artous.py 1 --testing \
    && ./run_script scripts/rav-artous.py 1 --testing \
    && ./run_script scripts/rav_flujofondos.py al30 -e0 \
    && ./run_script scripts/rav_flujofondos.py al30 \
    && ./run_script scripts/yf_historicos.py AAPL -e0  \
    && ./run_script scripts/yf_historicos.py AAPL \
    && ./run_script scripts/yf_historicos.py GOOGL IBM -e0  \
    && ./run_script scripts/yf_historicos.py GOOGL IBM \
    && ./run_script scripts/rav_home.py -e0 \
    && ./run_script scripts/rav_home.py  \
    && ./run_script scripts/rav_historicos.py gd30 -e0 \
    && ./run_script scripts/rav_historicos.py gd30 \
    && ./run_script scripts/rav_historicos_cmp al29 al35 -e0 \
    && ./run_script scripts/rav_historicos_cmp al29 al35 



#./run_script scripts/pue_flujofondos.py AL30 -e0 \
#    && ./run_script scripts/pue_flujofondos.py AL30 \
