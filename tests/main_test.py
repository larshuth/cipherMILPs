import unittest
import main


class MyTestCase(unittest.TestCase):
    def test_all_ciphers(self):
        viz = 0
        rounds = 4

        running_cipher = main.main(rounds, main.AesDifferential, viz, bit_oriented=False, chosen_type='Baksi 2020')
        running_cipher &= main.main(rounds, main.AesDifferential, viz, bit_oriented=True, chosen_type='Baksi 2020')
        running_cipher &= main.main(rounds, main.AesLinear, viz, bit_oriented=False, chosen_type='Boura 2020')
        running_cipher &= main.main(rounds, main.LBlockDifferential, viz, bit_oriented=False, chosen_type='SunEtAt 2013')
        running_cipher &= main.main(rounds, main.LBlockLinear, viz, bit_oriented=False, chosen_type='SunEtAt 2013 Greedy')
        print('Linear done')

        running_cipher &= main.main(rounds, main.AesLinear, viz, bit_oriented=True, chosen_type='Boura 2020')
        running_cipher &= main.main(rounds, main.LBlockDifferential, viz, bit_oriented=True, chosen_type='SunEtAt 2013 Greedy')
        running_cipher &= main.main(rounds, main.LBlockLinear, viz, bit_oriented=True, chosen_type='SunEtAl 2013 with Baksi extension 2020 Greedy')
        running_cipher &= main.main(rounds, main.Gift64Differential, viz, bit_oriented=True, chosen_type='SunEtAt 2013')
        running_cipher &= main.main(rounds, main.Gift64Linear, viz, bit_oriented=True, chosen_type='SunEtAt 2013 with Baksi Extension')
        print('Differential done')

        self.assertEqual(True, running_cipher)
        return


if __name__ == '__main__':
    unittest.main()
