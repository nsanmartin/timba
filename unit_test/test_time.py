import unittest
import datetime as dt
from timba.src import time

class TestExpirationOpened(unittest.TestCase):
    def test_ctor(self):
        d = dt.datetime(1,1,1,1,1,1)
        eo = time.ExpirationOpened(d, d)
        self.assertEqual(eo.open_time, d)
        self.assertEqual(eo.close_time, d)

    def test_get_expiration(self):
        before = dt.datetime(2023,5,23,10,0,0)
        during = dt.datetime(2023,5,23,13,0,0)
        after = dt.datetime(2023, 5,23,19,0,0)
        eo = time.ExpirationOpened(11, 18)

        self.assertEqual(eo.get_expiration(before, 0), 86400*1000)
        self.assertEqual(eo.get_expiration(before, 86400*1001), 86400*1001)

        self.assertEqual(eo.get_expiration(during, 0), 0)
        self.assertEqual(eo.get_expiration(during, 10), 10)

        self.assertEqual(eo.get_expiration(after, 0), 3600 * 1000)
        self.assertEqual(eo.get_expiration(after, 3600 * 1001), 3600 * 1001)

        saturday = dt.datetime(2023,5,20,10,0,0)
        self.assertEqual( eo.get_expiration(saturday, 0), 57600 * 1000)
        self.assertEqual(
            eo.get_expiration(saturday, 57600 * 1001), 57600 * 1001
        )

        sunday = dt.datetime(2023,5,21,10,0,0)
        self.assertEqual(eo.get_expiration(sunday, 0), 144 * 1000**2)
        self.assertEqual(
            eo.get_expiration(sunday, 144 * 1000**2 + 1), 144 * 1000**2 + 1
        )

        monday_before = dt.datetime(2022, 5,23,9,0,0)
        self.assertEqual(eo.get_expiration(monday_before, 0), 259200 * 1000)
        self.assertEqual(
            eo.get_expiration(monday_before, 259200 * 1001), 259200 * 1001
        )
