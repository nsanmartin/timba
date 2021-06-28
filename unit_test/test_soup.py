import unittest
from bs4 import BeautifulSoup
from src import soup

table0 = BeautifulSoup("""<table class="tablename">
        <thead>
            <tr> <th> Header </th> </tr>
            <tr>
                <th>Col1</th>
                <th>Col2</th>
                <th>Col3</th>
                <th>Col4</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>24/06/2020</td>
                <td>0,1</td>
                <td>-</td>
                <td>0,3</td>
            </tr>
            <tr>
                <td>06/04/2021</td>
                <td>1,100</td>
                <td>-</td>
                <td>1,300</td>
            </tr>
        <tfoot>
            <tr>
                <td colspan="4">Foot Value</td>
            </tr>
        </tfoot>
    </table>""", 'lxml').find("table", attrs={"class": "tablename"})



class TestSoup(unittest.TestCase):

    def test_get_table_head(self):
        head = soup.get_table_head(table0)
        rows = soup.head_rows_to_list(head)
        self.assertEqual(
            rows,
            [[' Header '], ['Col1', 'Col2', 'Col3', 'Col4']]
        )

    def test_get_table_body(self):
        body = soup.get_table_body(table0)
        rows = soup.data_rows_to_list(body)
        self.assertEqual(
            rows,
            [['24/06/2020', '0,1', '-', '0,3'], ['06/04/2021', '1,100', '-', '1,300']]
        )

