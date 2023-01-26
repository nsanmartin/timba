import pandas as pd

from src import pd_read as pdr

class DataFrameRaw():

    def __init__(self, fname):
        self.df = pd.read_csv(fname)

    def __repr__(self):
        return repr(self.df)


class DataFrameStdHead(DataFrameRaw):

    def __init__(self,fname):
        super().__init__(fname)
        pdr.df_map_header(self.df)



class DataFrameDateIx(DataFrameStdHead):

    def __init__(self, fname):
        super().__init__(fname)
        pdr.df_map_time(self.df)
        pdr.df_set_index_to_time(self.df)
