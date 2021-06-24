import unittest
from src import table

class TestTable(unittest.TestCase):
    def test_read_number(self):
        self.assertEqual(table.esp_text_to_num_text('-'), '0')
        self.assertEqual(table.esp_text_to_num_text('1'), '1')
        self.assertEqual(table.esp_text_to_num_text('1.000'), '1000')
        self.assertEqual(table.esp_text_to_num_text('1,003'), '1.003')
        self.assertEqual(table.esp_text_to_num_text('1.003,4'), '1003.4')
