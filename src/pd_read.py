import pandas as pd
## headers for pandas data frames
# symb
# open
# close
# min
# max
# vol
# date
# time

def map_column_name(name):
    name = name.lower()
    if name == 'especie':
        return 'symb'
    if name == 'fecha':
        return 'date'
    if name == 'apertura':
        return 'open'
    if name == 'cierre':
        return 'close'
    if name == 'maximo':
        return 'max'
    if name == 'minimo':
        return 'min'
    if name == 'volumen':
        return 'vol'
    if name == 'timestamp':
        return 'time'


def assert_has_column(df, colname):
    assert colname in df.columns,\
        "df with no '"+ colname +"'. Names are: " + str(list(df.columns))

def df_map_header(*args):
    for df in args:
        df.rename(columns= { k:map_column_name(k) for k in df.columns }, inplace=True)

def df_map_time(df):
    assert_has_column(df, 'time')
    df['time'] = pd.to_datetime(df['time'], unit='s')

def df_set_index_to_time(df):
    assert_has_column(df, 'time')
    df.set_index('time', inplace=True)


def df_merge_on(x, y, colname):
    assert_has_column(x, colname)
    assert_has_column(y, colname)
    return x.merge(y, left_on=colname, right_on=colname)

def df_get_ratio(df, colname, invert=False):
    xcol = colname + '_x'
    ycol = colname + '_y'
    assert_has_column(df, xcol)
    assert_has_column(df, ycol)
    if invert:
        return df[ycol] / df[xcol]
    else :
        return df[xcol] / df[ycol]

def df_standarize(df):
    df_map_header(df)
    df_map_time(df)
    df_set_index_to_time(df)

def df_concat_cols(colname, *args):
    series = [ df[colname].rename(df['symb'][0]) for df in args]
    return pd.concat(series, axis=1)