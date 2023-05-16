import unittest
from timba.src import fetch

class TestFetch(unittest.TestCase):
    def test_build_qurl1(self):
        url = fetch.build_qurl1("a", ("b", "c"))
        self.assertEqual(
            url,
            "a?b=c"
        )

