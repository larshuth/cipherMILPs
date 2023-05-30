import unittest
from cipher.differential.gift import Gift64


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

        bits_before_round_2 = ['x128', 'x129', 'x74', 'x160', 'x130', 'x131', 'x90', 'x161', 'x132', 'x133', 'x106',
                               'x162', 'x134', 'x135', 'x122', 'x163', 'x136', 'x137', 'x70', 'x164', 'x138', 'x139',
                               'x86', 'x165', 'x140', 'x141', 'x102', 'x107', 'x142', 'x143', 'x118', 'x123', 'x144',
                               'x145', 'x66', 'x71', 'x146', 'x147', 'x82', 'x87', 'x148', 'x149', 'x98', 'x103',
                               'x150', 'x151', 'x114', 'x119', 'x152', 'x153', 'x78', 'x67', 'x154', 'x155', 'x94',
                               'x83', 'x156', 'x157', 'x110', 'x99', 'x158', 'x159', 'x126', 'x166']

        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x231', 'x232', 'x177', 'x263', 'x233', 'x234', 'x193', 'x264', 'x235', 'x236', 'x209',
                               'x265', 'x237', 'x238', 'x225', 'x266', 'x239', 'x240', 'x173', 'x267', 'x241', 'x242',
                               'x189', 'x268', 'x243', 'x244', 'x205', 'x210', 'x245', 'x246', 'x221', 'x226', 'x247',
                               'x248', 'x169', 'x174', 'x249', 'x250', 'x185', 'x190', 'x251', 'x252', 'x201', 'x206',
                               'x253', 'x254', 'x217', 'x222', 'x255', 'x256', 'x181', 'x170', 'x257', 'x258', 'x197',
                               'x186', 'x259', 'x260', 'x213', 'x202', 'x261', 'x262', 'x229', 'x269']

        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def round_testing_given_parameters(self, cipher_instance, expected_sbox_actions_round, expected_A_before_shift_rows,
                                       expected_A_after_shift_rows, expected_key_xor_actions,
                                       expected_xor_with_1_actions_round_1):

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

        expected_xor_with_1_actions_round_1 = [['lin trans', ['x79'], ['x160'], 'dl0'],
                                               ['lin trans', ['x95'], ['x161'], 'dl1'],
                                               ['lin trans', ['x111'], ['x162'], 'dl2'],
                                               ['lin trans', ['x127'], ['x163'], 'dl3'],
                                               ['lin trans', ['x75'], ['x164'], 'dl4'],
                                               ['lin trans', ['x91'], ['x165'], 'dl5'],
                                               ['lin trans', ['x115'], ['x166'], 'dl6']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_1, round_1_A_before_shift_rows,
                                            round_1_A_after_shift_rows, expected_key_xor_actions_round_1,
                                            expected_xor_with_1_actions_round_1)

        return

    def test_correct_actions_performed_round_2_bit_oriented(self):
        cipher_instance = Gift64(rounds=4, model_as_bit_oriented=True)

        cipher_instance.run_round()

        expected_sbox_actions_round_2 = [
            ['sbox', ['x128', 'x129', 'x74', 'x160'], ['x167', 'x168', 'x169', 'x170'], 'a16'],
            ['sbox', ['x130', 'x131', 'x90', 'x161'], ['x171', 'x172', 'x173', 'x174'], 'a17'],
            ['sbox', ['x132', 'x133', 'x106', 'x162'], ['x175', 'x176', 'x177', 'x178'], 'a18'],
            ['sbox', ['x134', 'x135', 'x122', 'x163'], ['x179', 'x180', 'x181', 'x182'], 'a19'],
            ['sbox', ['x136', 'x137', 'x70', 'x164'], ['x183', 'x184', 'x185', 'x186'], 'a20'],
            ['sbox', ['x138', 'x139', 'x86', 'x165'], ['x187', 'x188', 'x189', 'x190'], 'a21'],
            ['sbox', ['x140', 'x141', 'x102', 'x107'], ['x191', 'x192', 'x193', 'x194'], 'a22'],
            ['sbox', ['x142', 'x143', 'x118', 'x123'], ['x195', 'x196', 'x197', 'x198'], 'a23'],
            ['sbox', ['x144', 'x145', 'x66', 'x71'], ['x199', 'x200', 'x201', 'x202'], 'a24'],
            ['sbox', ['x146', 'x147', 'x82', 'x87'], ['x203', 'x204', 'x205', 'x206'], 'a25'],
            ['sbox', ['x148', 'x149', 'x98', 'x103'], ['x207', 'x208', 'x209', 'x210'], 'a26'],
            ['sbox', ['x150', 'x151', 'x114', 'x119'], ['x211', 'x212', 'x213', 'x214'], 'a27'],
            ['sbox', ['x152', 'x153', 'x78', 'x67'], ['x215', 'x216', 'x217', 'x218'], 'a28'],
            ['sbox', ['x154', 'x155', 'x94', 'x83'], ['x219', 'x220', 'x221', 'x222'], 'a29'],
            ['sbox', ['x156', 'x157', 'x110', 'x99'], ['x223', 'x224', 'x225', 'x226'], 'a30'],
            ['sbox', ['x158', 'x159', 'x126', 'x166'], ['x227', 'x228', 'x229', 'x230'], 'a31']]

        round_2_A_before_shift_rows = ['x167', 'x168', 'x169', 'x170', 'x171', 'x172', 'x173', 'x174', 'x175', 'x176',
                                       'x177', 'x178', 'x179', 'x180', 'x181', 'x182', 'x183', 'x184', 'x185', 'x186',
                                       'x187', 'x188', 'x189', 'x190', 'x191', 'x192', 'x193', 'x194', 'x195', 'x196',
                                       'x197', 'x198', 'x199', 'x200', 'x201', 'x202', 'x203', 'x204', 'x205', 'x206',
                                       'x207', 'x208', 'x209', 'x210', 'x211', 'x212', 'x213', 'x214', 'x215', 'x216',
                                       'x217', 'x218', 'x219', 'x220', 'x221', 'x222', 'x223', 'x224', 'x225', 'x226',
                                       'x227', 'x228', 'x229', 'x230']

        round_2_A_after_shift_rows = ['x167', 'x172', 'x177', 'x182', 'x183', 'x188', 'x193', 'x198', 'x199', 'x204',
                                      'x209', 'x214', 'x215', 'x220', 'x225', 'x230', 'x179', 'x168', 'x173', 'x178',
                                      'x195', 'x184', 'x189', 'x194', 'x211', 'x200', 'x205', 'x210', 'x227', 'x216',
                                      'x221', 'x226', 'x175', 'x180', 'x169', 'x174', 'x191', 'x196', 'x185', 'x190',
                                      'x207', 'x212', 'x201', 'x206', 'x223', 'x228', 'x217', 'x222', 'x171', 'x176',
                                      'x181', 'x170', 'x187', 'x192', 'x197', 'x186', 'x203', 'x208', 'x213', 'x202',
                                      'x219', 'x224', 'x229', 'x218']

        expected_key_xor_actions_round_2 = [['xor', 'x167', 'k32', 'x231', 'dx32'],
                                            ['xor', 'x172', 'k33', 'x232', 'dx33'],
                                            ['xor', 'x183', 'k34', 'x233', 'dx34'],
                                            ['xor', 'x188', 'k35', 'x234', 'dx35'],
                                            ['xor', 'x199', 'k36', 'x235', 'dx36'],
                                            ['xor', 'x204', 'k37', 'x236', 'dx37'],
                                            ['xor', 'x215', 'k38', 'x237', 'dx38'],
                                            ['xor', 'x220', 'k39', 'x238', 'dx39'],
                                            ['xor', 'x179', 'k40', 'x239', 'dx40'],
                                            ['xor', 'x168', 'k41', 'x240', 'dx41'],
                                            ['xor', 'x195', 'k42', 'x241', 'dx42'],
                                            ['xor', 'x184', 'k43', 'x242', 'dx43'],
                                            ['xor', 'x211', 'k44', 'x243', 'dx44'],
                                            ['xor', 'x200', 'k45', 'x244', 'dx45'],
                                            ['xor', 'x227', 'k46', 'x245', 'dx46'],
                                            ['xor', 'x216', 'k47', 'x246', 'dx47'],
                                            ['xor', 'x175', 'k48', 'x247', 'dx48'],
                                            ['xor', 'x180', 'k49', 'x248', 'dx49'],
                                            ['xor', 'x191', 'k50', 'x249', 'dx50'],
                                            ['xor', 'x196', 'k51', 'x250', 'dx51'],
                                            ['xor', 'x207', 'k52', 'x251', 'dx52'],
                                            ['xor', 'x212', 'k53', 'x252', 'dx53'],
                                            ['xor', 'x223', 'k54', 'x253', 'dx54'],
                                            ['xor', 'x228', 'k55', 'x254', 'dx55'],
                                            ['xor', 'x171', 'k56', 'x255', 'dx56'],
                                            ['xor', 'x176', 'k57', 'x256', 'dx57'],
                                            ['xor', 'x187', 'k58', 'x257', 'dx58'],
                                            ['xor', 'x192', 'k59', 'x258', 'dx59'],
                                            ['xor', 'x203', 'k60', 'x259', 'dx60'],
                                            ['xor', 'x208', 'k61', 'x260', 'dx61'],
                                            ['xor', 'x219', 'k62', 'x261', 'dx62'],
                                            ['xor', 'x224', 'k63', 'x262', 'dx63']]

        expected_xor_with_1_actions_round_2 = [['lin trans', ['x182'], ['x263'], 'dl7'],
                                               ['lin trans', ['x198'], ['x264'], 'dl8'],
                                               ['lin trans', ['x214'], ['x265'], 'dl9'],
                                               ['lin trans', ['x230'], ['x266'], 'dl10'],
                                               ['lin trans', ['x178'], ['x267'], 'dl11'],
                                               ['lin trans', ['x194'], ['x268'], 'dl12'],
                                               ['lin trans', ['x218'], ['x269'], 'dl13']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_2, round_2_A_before_shift_rows,
                                            round_2_A_after_shift_rows, expected_key_xor_actions_round_2,
                                            expected_xor_with_1_actions_round_2)

        return


if __name__ == '__main__':
    unittest.main()
