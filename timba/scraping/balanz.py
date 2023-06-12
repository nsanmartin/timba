import pandas as pd
import numpy as np
from collections import namedtuple
from itertools import takewhile, dropwhile, islice


def skipSpace(lines):
    return dropwhile(lambda s: s.isspace(), lines)


def parseNext(it):
    it = skipSpace(it)
    n = next(it)
    return it, n.strip()

asset_names = [
    'Acciones', 'Bonos', 'Cedears', 'Corporativos', 'Préstamos - Alquiler'
]


def is_end_of_all_activos(s):
    return s.startswith("La información detallada en este resumen")

def is_not_end_of_activo(s):
    return not (s.startswith("La información detallada en este resumen") 
        or s.startswith('BALANZ'))

def skip_to_next_activo(it):
    it = dropwhile(
        lambda s: not s.startswith("Posición consolidada por concertación"),
        it
    )
    it, _ = parseNext(it)
    return it

header_row = (
    "Especie",
    "Descripción", "Cantidad", "Garantía", "Precio", "Valor", "Actual"
)

def parse_dec(s):
    return s.replace(".", "").replace(",", ".")

def parseActivosRow(row):
    match row.split():
        case ("Especie", desc, cant, garantia, precio, valor, actual):
            return None
        case (ticker, *desc, cant, garantia, monp, precio, monv, valoract):
            return (
                ticker,
                parse_dec(cant),
                monp+monv,
                parse_dec(precio),
                parse_dec(valoract)
            )
        case ('Préstamos', '-', 'Alquiler'):
            return None
        case _:
            raise Exception (f"not match: '{row}'")


def parseActivoAndNext(it):
    it, n = parseNext(it)
    if n in asset_names:
        act = list(takewhile(is_not_end_of_activo, it))
        act = [
            parsed for r in act if (parsed := parseActivosRow(r)) is not None
        ]
        df = pd.DataFrame(
            act,
            columns=("especie", "n", "moneda", "precio", "va"),
        )
        it = skip_to_next_activo(it)
        return it, df, n
    return it, None, n

def parseNActivos(it):
    activos = []
    while True:
        it, act, n = parseActivoAndNext(it)
        if not isinstance(act, pd.DataFrame):
            return it, activos
        activos.append(act)
        if is_end_of_all_activos(n):
            it, _ = parseNext(it)
            return it, activos

def skipToTotal(it):
    return dropwhile(lambda s: not s.startswith('Total'), it)

def parseTotal(it):
    totals = takewhile(
        lambda s: not s.startswith('Tipo de cambio para esa fecha:'), it
    )
    return it, ''.join(totals)

def skipToActivos(it):
    it = dropwhile(
        lambda s: not s.startswith('Distribución por tipo de activos'), it
    )
    it, n = parseNext(it)
    return it


def parseResumen(it):
    it = skipToTotal(it)
    it, total = parseTotal(it)
    it = skipToActivos(it)
    it, acts = parseNActivos(it)
    
    print(f'TOTAL: {total}')
    df = pd.concat(acts)
    df['n'] = pd.to_numeric(df['n'])
    df['precio'] = pd.to_numeric(df['precio'])
    df['va'] = pd.to_numeric(df['va'])

    va = (df['n'] * df['precio']).round()
    va = abs(va - df['va'])
    df['va2'] = va

    pesos = df['va'][df['moneda'] == '$$'].sum()
    dolares = df['va'][df['moneda'] == 'USDUSD'].sum()
    print(f'pesos: {pesos}, dolares: {dolares}')
    return it


def test():
    with open('resumen.txt') as it:
        it = parseResumen(it)

test()

