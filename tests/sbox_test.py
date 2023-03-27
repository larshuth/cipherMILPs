import unittest
from cipher.sbox import SBox


class SBoxTest(unittest.TestCase):
    def test_branch_number(self):
        # testing branch number using the PRESENT SBox which is 3 accoridng to
        # https://crypto.stackexchange.com/questions/61075/number-of-active-s-boxes
        present_substitutions = {index: value for index, value in
                        enumerate([12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2])}
        testbox = SBox(present_substitutions, 4, 4)
        self.assertEqual(3, testbox.branch_number)


if __name__ == '__main__':
    unittest.main()
