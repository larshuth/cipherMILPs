import unittest
import main


class MyTestCase(unittest.TestCase):
    def test_all_ciphers(self):
        viz = 0
        rounds = 4

        print('Start')
        running_cipher = main.main(rounds, main.AesDifferential, viz, bit_oriented=False, chosen_type='Logical condition modeling')
        print('1/10')
        self.assertEqual(True, running_cipher)
        # running_cipher &= main.main(rounds, main.AesDifferential, viz, bit_oriented=True, chosen_type='Logical condition modeling')
        print('2/10')
        self.assertEqual(True, running_cipher)
        running_cipher &= main.main(rounds, main.AesLinear, viz, bit_oriented=False, chosen_type='Boura 2020 Algo 2')
        print('3/10')
        self.assertEqual(True, running_cipher)
        running_cipher &= main.main(rounds, main.LBlockDifferential, viz, bit_oriented=False, chosen_type='SunEtAl 2013')
        print('4/10')
        self.assertEqual(True, running_cipher)
        running_cipher &= main.main(rounds, main.LBlockLinear, viz, bit_oriented=False, chosen_type='SunEtAl 2013 Greedy')
        print('5/10')
        self.assertEqual(True, running_cipher)
        # running_cipher &= main.main(rounds, main.AesLinear, viz, bit_oriented=True, chosen_type='Logical condition modeling')
        print('6/10')
        self.assertEqual(True, running_cipher)
        running_cipher &= main.main(rounds, main.LBlockDifferential, viz, bit_oriented=True, chosen_type='SunEtAl 2013 Greedy')
        print('7/10')
        self.assertEqual(True, running_cipher)
        running_cipher &= main.main(rounds, main.LBlockLinear, viz, bit_oriented=True, chosen_type='Baksi 2020')
        print('8/10')
        self.assertEqual(True, running_cipher)
        running_cipher &= main.main(rounds, main.Gift64Differential, viz, bit_oriented=True, chosen_type='SunEtAl 2013')
        print('9/10')
        self.assertEqual(True, running_cipher)
        running_cipher &= main.main(rounds, main.Gift64Linear, viz, bit_oriented=True, chosen_type='Exclusion of impossible transitions')
        print('10/10')

        self.assertEqual(True, running_cipher)
        return


if __name__ == '__main__':
    unittest.main()
