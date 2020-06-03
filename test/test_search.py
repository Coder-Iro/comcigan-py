import unittest

from comcigan import School


class SearchTestCase(unittest.TestCase):
    def test_correct(self):
        self.assertIsInstance(School("운정고등학교"), School)

    def test_toomany(self):
        with self.assertRaises(ValueError):
            School("금촌")

    def test_noschool(self):
        with self.assertRaises(NameError):
            School("그런거 없다.")


if __name__ == '__main__':
    unittest.main()
