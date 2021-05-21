import unittest

from comcigan import School
from collections.abc import Iterable

school = School("운정고등학교")

class SchoolTestCase(unittest.TestCase):
    def test_getitem(self):
        self.assertIsInstance(school[0], list)

    def test_repr(self):
        self.assertIsInstance(repr(school), str)
    
    def test_str(self):
        self.assertIsInstance(str(school), str)
    
    def test_iter(self):
        self.assertIsInstance(iter(school), Iterable)

if __name__ == "__main__":
    unittest.main()
