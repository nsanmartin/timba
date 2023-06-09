import unittest
import pandas as pd
from timba.src import DataFrame as tdf

standard_header = [ 'Symb', 'Open', 'High', 'Low', 'Close', 'Volume', 'DateTime' ]

class TestDataFrame(unittest.TestCase):
    def test_ctors_headers(self):
        data = [{
            'especie': 'YPFD',
            'apertura': 17,
            'maximo': 17, 
            'minimo': 17,
            'cierre': 17,
            'volumen': 100,
            'timestamp': 1008720000
        }]
        df = pd.DataFrame(data)

        raw = tdf.DataFrameRaw.fromDataFrame(df.copy())
        self.assertTrue((raw.df.columns == df.columns).all())

        stdhead = tdf.DataFrameStdHead.fromDataFrame(df.copy())
        self.assertTrue((stdhead.df.columns == standard_header).all())

        dateix = tdf.DataFrameDateIx.fromDataFrame(df.copy()) 
        date = pd.to_datetime(1008720000, unit='s').date()
        self.assertEqual(date, dateix.df.index[0])


    def test_ctos_symb_cmp(self):
        x = pd.DataFrame([{
            'especie': 'YPFD', 'apertura': 17, 'maximo': 17, 'minimo': 17,
            'cierre': 51, 'volumen': 100, 'timestamp': 1008720000
        }])

        y = pd.DataFrame([{
            'especie': 'GD30', 'apertura': 17, 'maximo': 17, 'minimo': 17,
            'cierre': 17, 'volumen': 100, 'timestamp': 1008720000
        }])

        cmp = tdf.DataFrameSymbCmp.fromDataFrameList([x, y])
        self.assertTrue((cmp.df.columns == ['YPFD', 'GD30']).all())

        ratios = cmp.getRatiosBetween(cmp)
        ratios_cols = [ 'YPFD/YPFD', 'YPFD/GD30', 'GD30/YPFD', 'GD30/GD30' ]
        self.assertTrue((ratios.df.columns == ratios_cols).all())

        ratios = cmp.getRatios()
        self.assertTrue((ratios.df.columns == ['YPFD/GD30']).all())
