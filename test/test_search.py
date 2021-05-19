import unittest
import asyncio

from comcigan import School, AsyncSchool


class SearchTestCase(unittest.TestCase):
    def test_correct(self):
        self.assertIsInstance(School("운정고등학교"), School)

    def test_toomany(self):
        with self.assertRaises(ValueError):
            School("금촌")

    def test_noschool(self):
        with self.assertRaises(NameError):
            School("그런거 없다.")


class AsyncSearchTestCase(unittest.TestCase):
    def test_correct(self):
        sc = AsyncSchool()
        asyncio.get_event_loop().run_until_complete(sc.init("운정고등학교"))
        self.assertIsInstance(sc, AsyncSchool)

    def test_toomany(self):
        sc = AsyncSchool()
        with self.assertRaises(ValueError):
            asyncio.get_event_loop().run_until_complete(sc.init("금촌"))

    def test_noschool(self):
        sc = AsyncSchool()
        with self.assertRaises(NameError):
            asyncio.get_event_loop().run_until_complete(sc.init("그런거 없다."))


if __name__ == "__main__":
    unittest.main()
