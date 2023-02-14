#!/bin/bash
if [ -z $1 ]; then
    echo you must provide a symbol
else 
    python -m scripts.fetch_table https://www.streetinsider.com/dividend_history.php?q=$1 dividends  
fi
