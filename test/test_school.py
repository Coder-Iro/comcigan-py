import unittest
import asyncio

from comcigan import School, AsyncSchool
from collections.abc import Iterable

school = School("운정고등학교")
asyncschool = asyncio.get_event_loop().run_until_complete(AsyncSchool.init("운정고등학교"))


class SchoolTestCase(unittest.TestCase):
    def test_getitem(self):
        self.assertIsInstance(school[0], list)

    def test_repr(self):
        self.assertIsInstance(repr(school), str)

    def test_str(self):
        self.assertIsInstance(str(school), str)

    def test_iter(self):
        self.assertIsInstance(iter(school), Iterable)


class AsyncSchoolTestCase(unittest.TestCase):
    def test_getitem(self):
        self.assertIsInstance(asyncschool[0], list)

    def test_repr(self):
        self.assertIsInstance(repr(asyncschool), str)

    def test_str(self):
        self.assertIsInstance(str(asyncschool), str)

    def test_iter(self):
        self.assertIsInstance(iter(asyncschool), Iterable)


if __name__ == "__main__":
    unittest.main()
