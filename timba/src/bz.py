from timba.src import DataFrame
import pandas as pd

class DataFrameBz(DataFrame.DataFrameDateIx):
    def __init__(self, dfix):
        assert isinstance(dfix, DataFrame.DataFrameDateIx)
        self.df = dfix.df

    @staticmethod
    def fromDataFrame(df):
        return DataFrameBz(DataFrame.DataFrameDateIx.fromDataFrame(df))

    def ticker(self, ticker):
        return self.df[self.df['ticker'] == ticker.upper()]

def movs_as_date_indexed(fname):
    assert isinstance(fname, str), "fname must be a string"
    df = pd.read_csv(fname)
    boletos = DataFrame.DataFrameDateIx.fromDataFrame(df)
    #boletos.drop('descripcion', axis=1)
    return boletos

def boletos_as_date_indexed(fname):
    df = pd.read_csv(fname)
    boletos = DataFrame.DataFrameDateIx.fromDataFrame(df)
    boletos.drop('Symb', axis=1)
    return boletos

def movimientos(tdf, ticker):
    df = tdf.df[tdf.df['ticker'] == ticker]
    df = df[(df['precio'] > 0)
            | (df['descripcion'].str.startswith('Recibo de Títulos'))
            | (df['descripcion'].str.contains('Canje Titulos'))
            | (df['descripcion'].str.startswith('Acreditación cambio de ratio'))
            | (df['descripcion'].str.startswith('Movimiento Manual'))
            | (df['descripcion'].str.startswith('Dividendo en acciones'))
            | (df['descripcion'].str.startswith('Dividendo en espe'))
            | (df['descripcion'].str.startswith('Canje '))
            | (df['descripcion'].str.startswith('Transferencia '))
            | (df['descripcion'].str.startswith('Conversión '))
            | (df['descripcion'].str.startswith('Renta y Amortizaci'))]
    return df


def movimientos_to_tenencia(tdf):
    df = pd.DataFrame([
        (tk, movimientos(tdf, tk)['cantidad'].sum())
        for tk in tdf.df['ticker'].unique()
    ])
    df.dropna(inplace=True)
    df.set_index(0, inplace=True)
    df.index.name = None
    df.columns= ['tenencia']
    return df

