import unittest

# TODO: Die ganze File


class ConvexHullTestCases(unittest.TestCase):
    def test_string_to_inequality_conversion(self):
        inequality = "-x0 + x1 >= 0\n-x3 + x4 - x5 >= -1\n-x6 + x7 >= 0\n-x7 >= -1x4 >= 0"

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
