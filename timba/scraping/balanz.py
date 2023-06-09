import pandas as pd

def tenencia(df, ticker):
    mask = (df['CantidadOperada'] != -1) & (df['PrecioOperado'] != -1)
    mask = mask & (df['Ticker'] == ticker)
    sign = df['Operacion']\
            .str.startswith('Compra').transform(lambda x: 1 if x else -1)
    ops = df[mask]['CantidadOperada'] * sign
    return ops.sum()

    
