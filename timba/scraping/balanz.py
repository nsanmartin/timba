import pandas as pd
from collections import namedtuple
from itertools import takewhile, dropwhile, islice

#decimal_regexp = re.compile('^(\d+(?:\.\d+)?)$')
#
#def is_num_es(s):
#    return s and decimal_regexp.match(s.replace('.', ''))

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

def parseActivoAndNext(it):
    it, n = parseNext(it)
    if n in asset_names:
        #print(f'parsing n: {n}')
        act = list(takewhile(is_not_end_of_activo, it))
        #print(f'read: {"".join(act)}')
        it = skip_to_next_activo(it)
        return it, act, n
    return it, None, n

def parseNActivos(it):
    activos = []
    while True:
        it, act, n = parseActivoAndNext(it)
        if not act:
            return it, activos
        print(''.join(act))
        activos.append(list(act))
        if is_end_of_all_activos(n):
            it, _ = parseNext(it)
            print(n)
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
    
    acts = '----\n'.join([ "".join(a) for a in acts ])
    print(f'TOTAL: {total}')
    print(f'ACTIVOS: {acts}')
    return it


def test():
    with open('resumen.txt') as it:
        it = parseResumen(it)

test()


