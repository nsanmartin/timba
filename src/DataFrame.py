import pandas as pd
import os

## headers for pandas data frames
# symb, open, close, min, max, vol, date, time

def standarize_column_name(name):
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

def df_standarize_header(*args):
    for df in args:
        df.rename(columns= { k:standarize_column_name(k) for k in df.columns }, inplace=True)

def df_map_time(df):
    assert_has_column(df, 'time')
    df['time'] = pd.to_datetime(df['time'], unit='s').dt.date

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
    df_standarize_header(df)
    df_map_time(df)
    df_set_index_to_time(df)

def df_concat_cols(colname, dfs):
    #series = [ df[colname].rename(df[colname][0]) for df in dfs]
    series = [ df[colname].rename(df['symb'][0]) for df in dfs]
    return pd.concat(series, axis=1)



## DataFrame subtypes

class DataFrameRaw():

    @classmethod
    def copyDataFrame(cls, other):
        return cls(other.df, initialize = False)


    def copy(self):
        return self.copyDataFrame(self)

    def initialize(self):
        pass

    def __init__(self, df, initialize = True):
        self.df = df
        if initialize:
            self.initialize()

    def __repr__(self):
        return repr(self.df)


class DataFrameStdHead(DataFrameRaw):
    @classmethod
    def fromFilename(cls, fname):
        return cls(pd.read_csv(fname))


    def initialize(self):
        super().initialize()
        df_standarize_header(self.df)



class DataFrameDateIx(DataFrameStdHead):

    def initialize(self):
        super().initialize()
        df_map_time(self.df)
        df_set_index_to_time(self.df)



class DataFrameSymbCmp(DataFrameRaw):
    @classmethod
    def fromDataFrameList(cls, dfs):
        dfs = [ DataFrameDateIx(df).df for df in dfs]
        return cls(df_concat_cols('close', dfs))

    @classmethod
    def fromDirectory(cls, dirname):
        fnames = [ dirname + f for f in os.listdir(dirname) if f.endswith(".csv") ]
        return cls.fromDataFrameList([pd.read_csv(f) for f in fnames]) 

    def __init__(self, df, initialize=False):
        # we ignore initialize, it was added to distinguish betweem copy and construct
        self.df = df

    def getRatiosBetween(self, other):
        newcols = []
        newcolnames = []
        for c_i in self.df.columns:
            for c_j in other.df.columns:
                newcols.append(self.df[c_i] / other.df[c_j])
                newcolnames.append(c_i + "/" + c_j)
        return pd.concat(newcols, axis=1, keys=newcolnames)


    def getRatios(self):
        cnames = self.df.columns
        newcols = []
        newcolnames = []
        for i in range(len(cnames)):
            for j in range(i + 1, len(cnames)):
                c_i = cnames[i]
                c_j = cnames[j]
                newcols.append(self.df[c_i] / self.df[c_j])
                newcolnames.append(c_i + "/" + c_j)

        return pd.concat(newcols, axis=1, keys=newcolnames)
