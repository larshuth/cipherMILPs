import unittest
import main


class MyTestCase(unittest.TestCase):
    def test_all_ciphers(self):
        for cipher in main.AVAILABLE:
            viz = 0
            rounds = 4
            running_cipher_normal = main.main(rounds, cipher, viz, bit_oriented=False)
            self.assertEqual(True, running_cipher_normal)
            if cipher in main.BIT_ORIENTED:
                running_cipher_bit_oriented = main.main(rounds, cipher, viz, bit_oriented=True)
                self.assertEqual(True, running_cipher_bit_oriented)
            return


if __name__ == '__main__':
    unittest.main()
