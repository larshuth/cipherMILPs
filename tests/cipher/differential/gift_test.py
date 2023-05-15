import unittest
from cipher.differential.gift import Gift64
from cipher.actions.overwriteaction import OverwriteAction
from cipher.actions.permutationaction import PermutationAction
from cipher.actions.xoraction import XorAction
from cipher.actions.sboxaction import SBoxAction


class GIFT64Test(unittest.TestCase):
    def test_round_progression_bit_oriented(self):
        cipher_instance = Gift64(rounds=4, model_as_bit_oriented=True)

        bits_before_round_1 = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
                               'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25',
                               'x26', 'x27', 'x28', 'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37',
                               'x38', 'x39', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49',
                               'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x60', 'x61',
                               'x62', 'x63']

        self.assertEqual(cipher_instance.A, bits_before_round_1)

        cipher_instance.run_round()

        bits_before_round_2 = ['x128', 'x129', 'x74', 'x166', 'x130', 'x131', 'x90', 'x165', 'x132', 'x133', 'x106',
                               'x164', 'x134', 'x135', 'x122', 'x163', 'x136', 'x137', 'x70', 'x162', 'x138', 'x139',
                               'x86', 'x161', 'x140', 'x141', 'x102', 'x107', 'x142', 'x143', 'x118', 'x123', 'x144',
                               'x145', 'x66', 'x71', 'x146', 'x147', 'x82', 'x87', 'x148', 'x149', 'x98', 'x103',
                               'x150', 'x151', 'x114', 'x119', 'x152', 'x153', 'x78', 'x67', 'x154', 'x155', 'x94',
                               'x83', 'x156', 'x157', 'x110', 'x99', 'x158', 'x159', 'x126', 'x160']

        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x']

        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def round_testing_given_parameters(self, cipher_instance, expected_sbox_actions_round, expected_A_before_shift_rows,
                                       expected_A_after_shift_rows, expected_key_xor_actions,
                                       expected_xor_with_1_actions_round_1):

        actual_sbox_actions = cipher_instance.generate_sbox_actions_for_round()
        actual_sbox_actions_test_readable = [
            [sboxaction.type_of_action, int(sboxaction.input_vars[0][1:]), int(sboxaction.output_vars[0][1:]),
             sboxaction.dummy_var] for sboxaction in actual_sbox_actions]
        self.assertEqual(expected_sbox_actions_round, actual_sbox_actions_test_readable)

        for sboxaction in actual_sbox_actions:
            sboxaction.run_action()
        print(cipher_instance.A)

        self.assertEqual(expected_A_before_shift_rows, cipher_instance.A)

        for permutationsaction in cipher_instance.generate_permutation_actions_for_round():
            permutationsaction.run_action()

        self.assertEqual(expected_A_after_shift_rows, cipher_instance.A)

        actual_key_xor_actions = cipher_instance.generate_key_xor_actions_for_round()
        actual_key_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_key_xor_actions]
        self.assertEqual(expected_key_xor_actions, actual_key_xor_actions_test_readable)

        actual_single_bit_xor_actions = cipher_instance.generate_single_bit_xor_actions()
        actual_single_bit_xor_actions_text_readable = [
            [action.type_of_action, action.input_list, action.output_list, action.dummy_var] for action in
            actual_single_bit_xor_actions]
        for single_bit_xor_action in actual_single_bit_xor_actions:
            single_bit_xor_action.run_action()
        self.assertEqual(expected_xor_with_1_actions_round_1, actual_single_bit_xor_actions_text_readable)
        return

    def test_correct_actions_performed_round_1_bit_oriented(self):
        cipher_instance = Gift64(rounds=4, model_as_bit_oriented=True)

        expected_sbox_actions_round_1 = [['sbox', ['x0', 'x1', 'x2', 'x3'], ['x64', 'x65', 'x66', 'x67'], 'a0'],
                                         ['sbox', ['x4', 'x5', 'x6', 'x7'], ['x68', 'x69', 'x70', 'x71'], 'a1'],
                                         ['sbox', ['x8', 'x9', 'x10', 'x11'], ['x72', 'x73', 'x74', 'x75'], 'a2'],
                                         ['sbox', ['x12', 'x13', 'x14', 'x15'], ['x76', 'x77', 'x78', 'x79'], 'a3'],
                                         ['sbox', ['x16', 'x17', 'x18', 'x19'], ['x80', 'x81', 'x82', 'x83'], 'a4'],
                                         ['sbox', ['x20', 'x21', 'x22', 'x23'], ['x84', 'x85', 'x86', 'x87'], 'a5'],
                                         ['sbox', ['x24', 'x25', 'x26', 'x27'], ['x88', 'x89', 'x90', 'x91'], 'a6'],
                                         ['sbox', ['x28', 'x29', 'x30', 'x31'], ['x92', 'x93', 'x94', 'x95'], 'a7'],
                                         ['sbox', ['x32', 'x33', 'x34', 'x35'], ['x96', 'x97', 'x98', 'x99'], 'a8'],
                                         ['sbox', ['x36', 'x37', 'x38', 'x39'], ['x100', 'x101', 'x102', 'x103'], 'a9'],
                                         ['sbox', ['x40', 'x41', 'x42', 'x43'], ['x104', 'x105', 'x106', 'x107'],
                                          'a10'],
                                         ['sbox', ['x44', 'x45', 'x46', 'x47'], ['x108', 'x109', 'x110', 'x111'],
                                          'a11'],
                                         ['sbox', ['x48', 'x49', 'x50', 'x51'], ['x112', 'x113', 'x114', 'x115'],
                                          'a12'],
                                         ['sbox', ['x52', 'x53', 'x54', 'x55'], ['x116', 'x117', 'x118', 'x119'],
                                          'a13'],
                                         ['sbox', ['x56', 'x57', 'x58', 'x59'], ['x120', 'x121', 'x122', 'x123'],
                                          'a14'],
                                         ['sbox', ['x60', 'x61', 'x62', 'x63'], ['x124', 'x125', 'x126', 'x127'],
                                          'a15']]

        round_1_A_before_shift_rows = ['x64', 'x65', 'x66', 'x67', 'x68', 'x69', 'x70', 'x71', 'x72', 'x73', 'x74',
                                       'x75', 'x76', 'x77', 'x78', 'x79', 'x80', 'x81', 'x82', 'x83', 'x84', 'x85',
                                       'x86', 'x87', 'x88', 'x89', 'x90', 'x91', 'x92', 'x93', 'x94', 'x95', 'x96',
                                       'x97', 'x98', 'x99', 'x100', 'x101', 'x102', 'x103', 'x104', 'x105', 'x106',
                                       'x107', 'x108', 'x109', 'x110', 'x111', 'x112', 'x113', 'x114', 'x115', 'x116',
                                       'x117', 'x118', 'x119', 'x120', 'x121', 'x122', 'x123', 'x124', 'x125', 'x126',
                                       'x127']

        round_1_A_after_shift_rows = ['x64', 'x69', 'x74', 'x79', 'x80', 'x85', 'x90', 'x95', 'x96', 'x101', 'x106',
                                      'x111', 'x112', 'x117', 'x122', 'x127', 'x76', 'x65', 'x70', 'x75', 'x92', 'x81',
                                      'x86', 'x91', 'x108', 'x97', 'x102', 'x107', 'x124', 'x113', 'x118', 'x123',
                                      'x72', 'x77', 'x66', 'x71', 'x88', 'x93', 'x82', 'x87', 'x104', 'x109', 'x98',
                                      'x103', 'x120', 'x125', 'x114', 'x119', 'x68', 'x73', 'x78', 'x67', 'x84', 'x89',
                                      'x94', 'x83', 'x100', 'x105', 'x110', 'x99', 'x116', 'x121', 'x126', 'x115']

        expected_key_xor_actions_round_1 = [['xor', 'x64', 'k0', 'x128', 'dx0'], ['xor', 'x69', 'k1', 'x129', 'dx1'],
                                            ['xor', 'x80', 'k2', 'x130', 'dx2'], ['xor', 'x85', 'k3', 'x131', 'dx3'],
                                            ['xor', 'x96', 'k4', 'x132', 'dx4'], ['xor', 'x101', 'k5', 'x133', 'dx5'],
                                            ['xor', 'x112', 'k6', 'x134', 'dx6'], ['xor', 'x117', 'k7', 'x135', 'dx7'],
                                            ['xor', 'x76', 'k8', 'x136', 'dx8'], ['xor', 'x65', 'k9', 'x137', 'dx9'],
                                            ['xor', 'x92', 'k10', 'x138', 'dx10'],
                                            ['xor', 'x81', 'k11', 'x139', 'dx11'],
                                            ['xor', 'x108', 'k12', 'x140', 'dx12'],
                                            ['xor', 'x97', 'k13', 'x141', 'dx13'],
                                            ['xor', 'x124', 'k14', 'x142', 'dx14'],
                                            ['xor', 'x113', 'k15', 'x143', 'dx15'],
                                            ['xor', 'x72', 'k16', 'x144', 'dx16'],
                                            ['xor', 'x77', 'k17', 'x145', 'dx17'],
                                            ['xor', 'x88', 'k18', 'x146', 'dx18'],
                                            ['xor', 'x93', 'k19', 'x147', 'dx19'],
                                            ['xor', 'x104', 'k20', 'x148', 'dx20'],
                                            ['xor', 'x109', 'k21', 'x149', 'dx21'],
                                            ['xor', 'x120', 'k22', 'x150', 'dx22'],
                                            ['xor', 'x125', 'k23', 'x151', 'dx23'],
                                            ['xor', 'x68', 'k24', 'x152', 'dx24'],
                                            ['xor', 'x73', 'k25', 'x153', 'dx25'],
                                            ['xor', 'x84', 'k26', 'x154', 'dx26'],
                                            ['xor', 'x89', 'k27', 'x155', 'dx27'],
                                            ['xor', 'x100', 'k28', 'x156', 'dx28'],
                                            ['xor', 'x105', 'k29', 'x157', 'dx29'],
                                            ['xor', 'x116', 'k30', 'x158', 'dx30'],
                                            ['xor', 'x121', 'k31', 'x159', 'dx31']]

        expected_xor_with_1_actions_round_1 = [['lin trans', 'x79', 'x160', 'dl0'], ['lin trans', 'x95', 'x161', 'dl1'],
                                               ['lin trans', 'x111', 'x162', 'dl2'],
                                               ['lin trans', 'x127', 'x163', 'dl3'],
                                               ['lin trans', 'x75', 'x164', 'dl4'], ['lin trans', 'x91', 'x165', 'dl5'],
                                               ['lin trans', 'x115', 'x166', 'dl6']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_1, round_1_A_before_shift_rows,
                                            round_1_A_after_shift_rows, expected_key_xor_actions_round_1,
                                            expected_xor_with_1_actions_round_1)

        return

    def test_correct_actions_performed_round_2_bit_oriented(self):
        pass
        return


if __name__ == '__main__':
    unittest.main()
