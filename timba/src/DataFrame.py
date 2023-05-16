import os
import datetime as dt
import pandas as pd
import yfinance as yf

def standarize_column_name(name):
    lcase = name.lower()
    if lcase == 'especie':
        return 'Symb'
    #if lcase == 'fecha':
    #    return 'Date'
    if lcase == 'apertura':
        return 'Open'
    if lcase == 'cierre':
        return 'Close'
    if lcase == 'maximo':
        return 'High'
    if lcase == 'minimo':
        return 'Low'
    if lcase == 'volumen':
        return 'Volume'
    if lcase == 'timestamp':
        return 'Date'
    else:
        return name


def assert_has_column(df, colname):
    assert colname in df.columns,\
        "df with no '"+ colname +"'. Names are: " + str(list(df.columns))

def df_standarize_header(*args):
    for df in args:
        df.rename(
            columns={
                k:standarize_column_name(k) for k in df.columns
                },
            inplace=True
        )

def df_map_time(df):
    assert_has_column(df, 'Date')
    try:
        df['Date'] = pd.to_datetime(df['Date'], unit='s').dt.date
    except ValueError as e:
        print("Could not map time column (" \
                + str(e) +"), ignoring. TODO: check column instead")

def df_set_index_to_time(df):
    assert_has_column(df, 'Date')
    df.set_index('Date', inplace=True)


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
    series = [ df[colname].rename(df['Symb'][0]) for df in dfs]
    return pd.concat(series, axis=1)



class DataFrameRaw():
    '''
    This is just a wrapper over pd.DataFrame
    '''

    @staticmethod
    def fromDataFrame(df):
        if isinstance(df, pd.DataFrame):
            return DataFrameRaw(df)
        if isinstance(df, DataFrameRaw):
            return df
        else:
            raise RuntimeError(
                "Expected df of type pd.DataFrame or " \
                + "timba.DataFrameRaw"
            )


    @classmethod
    def copyDataFrame(cls, other):
        return cls(other.df)


    def copy(self):
        return self.copyDataFrame(self)

    def __init__(self, df):
        assert isinstance(df, pd.DataFrame)
        self.df = df

    def __repr__(self):
        return repr(self.df)



class DataFrameStdHead(DataFrameRaw):
    '''
    This adds to the DataFrameRaw a standard naming for the columns.
    '''
    @staticmethod
    def fromDataFrame(df):
        if isinstance(df, DataFrameStdHead):
            return df
        elif isinstance(df, DataFrameRaw):
            df_standarize_header(df.df)
            return DataFrameStdHead(df.df)

        else:
            return DataFrameStdHead.fromDataFrame(
                DataFrameRaw.fromDataFrame(df)
            )

            
    @classmethod
    def fromFilename(cls, fname):
        return cls.fromDataFrame(pd.read_csv(fname))



class DataFrameDateIx(DataFrameStdHead):
    '''
    This type adds to the standarized header and index based on
    Date column (therefore the parameter must have a Date column).
    '''
    @staticmethod
    def fromDataFrame(df):
        if isinstance(df, DataFrameDateIx):
            return df
        elif isinstance(df, DataFrameStdHead):
            if df.df.index.name != 'Date':
                df_map_time(df.df)
                df_set_index_to_time(df.df)
            return DataFrameDateIx(df.df)
        else:
            return DataFrameDateIx.fromDataFrame(
                DataFrameStdHead.fromDataFrame(df)
            )

    @staticmethod
    def fromDateIndexed(df, symb=None):
        if not symb and not 'Symb' in df.columns:
            raise RuntimeError('Symb is missing!')
        if symb and 'Symb' in df.columns and symb != df['Symb'][0]:
            raise RuntimeError("Inconsistent Symb!")

        if type(df.index[0]) !=  dt.date:
            df.index = df.index.date
        res = DataFrameDateIx(df)
        if symb and not 'Symb' in df.columns:
            res.df['Symb'] = symb
        return res

    @staticmethod
    def fromYFinance(symb):
        df = yf.download(symb)
        return DataFrameDateIx.fromDateIndexed(df, symb)



class DataFrameSymbCmp(DataFrameRaw):
    '''
    This class is a wrapper of a df collection for the purpose of
    comparing them.
    '''

    @classmethod
    def fromDataFrameList(cls, dfs):
        dfs = [ DataFrameDateIx.fromDataFrame(df) for df in dfs]
        dfs = [ x.df for x in dfs]
        return cls(df_concat_cols('Close', dfs))

    @classmethod
    def fromDirectory(cls, dirname):
        fnames = [ dirname + f for f in os.listdir(dirname) if f.endswith(".csv") ]
        return cls.fromDataFrameList([pd.read_csv(f) for f in fnames]) 


    def getRatiosBetween(self, other):
        newcols = []
        newcolnames = []
        for c_i in self.df.columns:
            for c_j in other.df.columns:
                newcols.append(self.df[c_i] / other.df[c_j])
                newcolnames.append(c_i + "/" + c_j)
        return DataFrameSymbCmp(pd.concat(newcols, axis=1, keys=newcolnames))


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

        return DataFrameSymbCmp(pd.concat(newcols, axis=1, keys=newcolnames))


