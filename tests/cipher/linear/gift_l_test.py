import unittest
from cipher.linear.gift import Gift64


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

        bits_before_round_2 = ['x64', 'x69', 'x74', 'x128', 'x80', 'x85', 'x90', 'x129', 'x96', 'x101', 'x106', 'x130',
                               'x112', 'x117', 'x122', 'x131', 'x76', 'x65', 'x70', 'x132', 'x92', 'x81', 'x86', 'x133',
                               'x108', 'x97', 'x102', 'x107', 'x124', 'x113', 'x118', 'x123', 'x72', 'x77', 'x66',
                               'x71', 'x88', 'x93', 'x82', 'x87', 'x104', 'x109', 'x98', 'x103', 'x120', 'x125', 'x114',
                               'x119', 'x68', 'x73', 'x78', 'x67', 'x84', 'x89', 'x94', 'x83', 'x100', 'x105', 'x110',
                               'x99', 'x116', 'x121', 'x126', 'x134']

        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x135', 'x140', 'x145', 'x199', 'x151', 'x156', 'x161', 'x200', 'x167', 'x172', 'x177',
                               'x201', 'x183', 'x188', 'x193', 'x202', 'x147', 'x136', 'x141', 'x203', 'x163', 'x152',
                               'x157', 'x204', 'x179', 'x168', 'x173', 'x178', 'x195', 'x184', 'x189', 'x194', 'x143',
                               'x148', 'x137', 'x142', 'x159', 'x164', 'x153', 'x158', 'x175', 'x180', 'x169', 'x174',
                               'x191', 'x196', 'x185', 'x190', 'x139', 'x144', 'x149', 'x138', 'x155', 'x160', 'x165',
                               'x154', 'x171', 'x176', 'x181', 'x170', 'x187', 'x192', 'x197', 'x205']

        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def round_testing_given_parameters(self, cipher_instance, expected_sbox_actions_round, expected_A_before_shift_rows,
                                       expected_A_after_shift_rows, expected_xor_with_1_actions_round_1):

        actual_sbox_actions = cipher_instance.generate_sbox_actions_for_round()
        actual_sbox_actions_test_readable = [
            [sboxaction.type_of_action, sboxaction.input_vars, sboxaction.output_vars,
             sboxaction.dummy_var] for sboxaction in actual_sbox_actions]
        self.assertEqual(expected_sbox_actions_round, actual_sbox_actions_test_readable)

        for sboxaction in actual_sbox_actions:
            sboxaction.run_action()
        print(cipher_instance.A)

        self.assertEqual(expected_A_before_shift_rows, cipher_instance.A)

        for permutationsaction in cipher_instance.generate_permutation_actions_for_round():
            permutationsaction.run_action()

        self.assertEqual(expected_A_after_shift_rows, cipher_instance.A)

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

        expected_xor_with_1_actions_round_1 = [['lin trans', ['x79'], ['x128'], 'dl0'],
                                               ['lin trans', ['x95'], ['x129'], 'dl1'],
                                               ['lin trans', ['x111'], ['x130'], 'dl2'],
                                               ['lin trans', ['x127'], ['x131'], 'dl3'],
                                               ['lin trans', ['x75'], ['x132'], 'dl4'],
                                               ['lin trans', ['x91'], ['x133'], 'dl5'],
                                               ['lin trans', ['x115'], ['x134'], 'dl6']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_1, round_1_A_before_shift_rows,
                                            round_1_A_after_shift_rows, expected_xor_with_1_actions_round_1)

        return

    def test_correct_actions_performed_round_2_bit_oriented(self):
        cipher_instance = Gift64(rounds=4, model_as_bit_oriented=True)

        cipher_instance.run_round()

        expected_sbox_actions_round_2 = [
            ['sbox', ['x64', 'x69', 'x74', 'x128'], ['x135', 'x136', 'x137', 'x138'], 'a16'],
            ['sbox', ['x80', 'x85', 'x90', 'x129'], ['x139', 'x140', 'x141', 'x142'], 'a17'],
            ['sbox', ['x96', 'x101', 'x106', 'x130'], ['x143', 'x144', 'x145', 'x146'], 'a18'],
            ['sbox', ['x112', 'x117', 'x122', 'x131'], ['x147', 'x148', 'x149', 'x150'], 'a19'],
            ['sbox', ['x76', 'x65', 'x70', 'x132'], ['x151', 'x152', 'x153', 'x154'], 'a20'],
            ['sbox', ['x92', 'x81', 'x86', 'x133'], ['x155', 'x156', 'x157', 'x158'], 'a21'],
            ['sbox', ['x108', 'x97', 'x102', 'x107'], ['x159', 'x160', 'x161', 'x162'], 'a22'],
            ['sbox', ['x124', 'x113', 'x118', 'x123'], ['x163', 'x164', 'x165', 'x166'], 'a23'],
            ['sbox', ['x72', 'x77', 'x66', 'x71'], ['x167', 'x168', 'x169', 'x170'], 'a24'],
            ['sbox', ['x88', 'x93', 'x82', 'x87'], ['x171', 'x172', 'x173', 'x174'], 'a25'],
            ['sbox', ['x104', 'x109', 'x98', 'x103'], ['x175', 'x176', 'x177', 'x178'], 'a26'],
            ['sbox', ['x120', 'x125', 'x114', 'x119'], ['x179', 'x180', 'x181', 'x182'], 'a27'],
            ['sbox', ['x68', 'x73', 'x78', 'x67'], ['x183', 'x184', 'x185', 'x186'], 'a28'],
            ['sbox', ['x84', 'x89', 'x94', 'x83'], ['x187', 'x188', 'x189', 'x190'], 'a29'],
            ['sbox', ['x100', 'x105', 'x110', 'x99'], ['x191', 'x192', 'x193', 'x194'], 'a30'],
            ['sbox', ['x116', 'x121', 'x126', 'x134'], ['x195', 'x196', 'x197', 'x198'], 'a31']]

        round_2_A_before_shift_rows = ['x135', 'x136', 'x137', 'x138', 'x139', 'x140', 'x141', 'x142', 'x143', 'x144',
                                       'x145', 'x146', 'x147', 'x148', 'x149', 'x150', 'x151', 'x152', 'x153', 'x154',
                                       'x155', 'x156', 'x157', 'x158', 'x159', 'x160', 'x161', 'x162', 'x163', 'x164',
                                       'x165', 'x166', 'x167', 'x168', 'x169', 'x170', 'x171', 'x172', 'x173', 'x174',
                                       'x175', 'x176', 'x177', 'x178', 'x179', 'x180', 'x181', 'x182', 'x183', 'x184',
                                       'x185', 'x186', 'x187', 'x188', 'x189', 'x190', 'x191', 'x192', 'x193', 'x194',
                                       'x195', 'x196', 'x197', 'x198']

        round_2_A_after_shift_rows = ['x135', 'x140', 'x145', 'x150', 'x151', 'x156', 'x161', 'x166', 'x167', 'x172',
                                      'x177', 'x182', 'x183', 'x188', 'x193', 'x198', 'x147', 'x136', 'x141', 'x146',
                                      'x163', 'x152', 'x157', 'x162', 'x179', 'x168', 'x173', 'x178', 'x195', 'x184',
                                      'x189', 'x194', 'x143', 'x148', 'x137', 'x142', 'x159', 'x164', 'x153', 'x158',
                                      'x175', 'x180', 'x169', 'x174', 'x191', 'x196', 'x185', 'x190', 'x139', 'x144',
                                      'x149', 'x138', 'x155', 'x160', 'x165', 'x154', 'x171', 'x176', 'x181', 'x170',
                                      'x187', 'x192', 'x197', 'x186']

        expected_xor_with_1_actions_round_2 = [['lin trans', ['x150'], ['x199'], 'dl7'],
                                               ['lin trans', ['x166'], ['x200'], 'dl8'],
                                               ['lin trans', ['x182'], ['x201'], 'dl9'],
                                               ['lin trans', ['x198'], ['x202'], 'dl10'],
                                               ['lin trans', ['x146'], ['x203'], 'dl11'],
                                               ['lin trans', ['x162'], ['x204'], 'dl12'],
                                               ['lin trans', ['x186'], ['x205'], 'dl13']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_2, round_2_A_before_shift_rows,
                                            round_2_A_after_shift_rows, expected_xor_with_1_actions_round_2)
        return


if __name__ == '__main__':
    unittest.main()
