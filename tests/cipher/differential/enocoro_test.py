import unittest
from cipher.differential.enocoro import Enocoro


class EnocoroTestCase(unittest.TestCase):
    def test_active_bit_transition_byte_oriented(self):
        enocoro_instance = Enocoro(model_as_bit_oriented=False)

        A_before_round_1 = ["x" + str(i) for i in range(34)]
        self.assertEqual(A_before_round_1, enocoro_instance.A)

        enocoro_instance.shift_before()
        for action in enocoro_instance.generate_actions_for_round():
            enocoro_instance.gen_long_constraint(action)
        enocoro_instance.shift_after()

        A_before_round_2 = ["x" + str(i-1) for i in range(34)]
        A_before_round_2[0] = "x34"
        A_before_round_2[3] = "X41"
        A_before_round_2[8] = "X42"
        A_before_round_2[17] = "X43"
        A_before_round_2[32] = "X39"
        A_before_round_2[33] = "X40"

        self.assertEqual(A_before_round_2, enocoro_instance.A)
        return


if __name__ == '__main__':
    unittest.main()
