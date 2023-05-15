import unittest
from cipher.differential.lblock import LBlock
from cipher.actions.overwriteaction import OverwriteAction
from cipher.actions.permutationaction import PermutationAction
from cipher.actions.xoraction import XorAction
from cipher.actions.sboxaction import SBoxAction


class LBlockTest(unittest.TestCase):
    def test_round_progression_bit_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=True)

        bits_before_round_1 = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
                               'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25',
                               'x26', 'x27', 'x28', 'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37',
                               'x38', 'x39', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49',
                               'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x60', 'x61',
                               'x62', 'x63']
        self.assertEqual(cipher_instance.A, bits_before_round_1)

        cipher_instance.run_round()

        bits_before_round_2 = ['x128', 'x129', 'x130', 'x131', 'x132', 'x133', 'x134', 'x135', 'x136', 'x137', 'x138',
                               'x139', 'x140', 'x141', 'x142', 'x143', 'x144', 'x145', 'x146', 'x147', 'x148', 'x149',
                               'x150', 'x151', 'x152', 'x153', 'x154', 'x155', 'x156', 'x157', 'x158', 'x159', 'x0',
                               'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14',
                               'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26',
                               'x27', 'x28', 'x29', 'x30', 'x31']
        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x224', 'x225', 'x226', 'x227', 'x228', 'x229', 'x230', 'x231', 'x232', 'x233', 'x234',
                               'x235', 'x236', 'x237', 'x238', 'x239', 'x240', 'x241', 'x242', 'x243', 'x244', 'x245',
                               'x246', 'x247', 'x248', 'x249', 'x250', 'x251', 'x252', 'x253', 'x254', 'x255',
                               'x128', 'x129', 'x130', 'x131', 'x132', 'x133', 'x134', 'x135', 'x136', 'x137', 'x138',
                               'x139', 'x140', 'x141', 'x142', 'x143', 'x144', 'x145', 'x146', 'x147', 'x148', 'x149',
                               'x150', 'x151', 'x152', 'x153', 'x154', 'x155', 'x156', 'x157', 'x158', 'x159']
        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def test_correct_actions_performed_round_1_bit_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=True)

        expected_key_xor_actions_round_1 = [['xor', 'x0', 'k0', 'x64', 'dx0'], ['xor', 'x1', 'k1', 'x65', 'dx1'],
                                            ['xor', 'x2', 'k2', 'x66', 'dx2'], ['xor', 'x3', 'k3', 'x67', 'dx3'],
                                            ['xor', 'x4', 'k4', 'x68', 'dx4'], ['xor', 'x5', 'k5', 'x69', 'dx5'],
                                            ['xor', 'x6', 'k6', 'x70', 'dx6'], ['xor', 'x7', 'k7', 'x71', 'dx7'],
                                            ['xor', 'x8', 'k8', 'x72', 'dx8'], ['xor', 'x9', 'k9', 'x73', 'dx9'],
                                            ['xor', 'x10', 'k10', 'x74', 'dx10'], ['xor', 'x11', 'k11', 'x75', 'dx11'],
                                            ['xor', 'x12', 'k12', 'x76', 'dx12'], ['xor', 'x13', 'k13', 'x77', 'dx13'],
                                            ['xor', 'x14', 'k14', 'x78', 'dx14'], ['xor', 'x15', 'k15', 'x79', 'dx15'],
                                            ['xor', 'x16', 'k16', 'x80', 'dx16'], ['xor', 'x17', 'k17', 'x81', 'dx17'],
                                            ['xor', 'x18', 'k18', 'x82', 'dx18'], ['xor', 'x19', 'k19', 'x83', 'dx19'],
                                            ['xor', 'x20', 'k20', 'x84', 'dx20'], ['xor', 'x21', 'k21', 'x85', 'dx21'],
                                            ['xor', 'x22', 'k22', 'x86', 'dx22'], ['xor', 'x23', 'k23', 'x87', 'dx23'],
                                            ['xor', 'x24', 'k24', 'x88', 'dx24'], ['xor', 'x25', 'k25', 'x89', 'dx25'],
                                            ['xor', 'x26', 'k26', 'x90', 'dx26'], ['xor', 'x27', 'k27', 'x91', 'dx27'],
                                            ['xor', 'x28', 'k28', 'x92', 'dx28'], ['xor', 'x29', 'k29', 'x93', 'dx29'],
                                            ['xor', 'x30', 'k30', 'x94', 'dx30'], ['xor', 'x31', 'k31', 'x95', 'dx31']]
        expected_sbox_actions_round_1 = [['sbox', 64, 96, 'a0'], ['sbox', 68, 100, 'a1'], ['sbox', 72, 104, 'a2'],
                                         ['sbox', 76, 108, 'a3'], ['sbox', 80, 112, 'a4'], ['sbox', 84, 116, 'a5'],
                                         ['sbox', 88, 120, 'a6'], ['sbox', 92, 124, 'a7']]
        expected_xor_actions_round_1 = [['xor', 'x100', 'x40', 'x128', 'dx32'], ['xor', 'x101', 'x41', 'x129', 'dx33'],
                                        ['xor', 'x102', 'x42', 'x130', 'dx34'], ['xor', 'x103', 'x43', 'x131', 'dx35'],
                                        ['xor', 'x108', 'x44', 'x132', 'dx36'], ['xor', 'x109', 'x45', 'x133', 'dx37'],
                                        ['xor', 'x110', 'x46', 'x134', 'dx38'], ['xor', 'x111', 'x47', 'x135', 'dx39'],
                                        ['xor', 'x96', 'x48', 'x136', 'dx40'], ['xor', 'x97', 'x49', 'x137', 'dx41'],
                                        ['xor', 'x98', 'x50', 'x138', 'dx42'], ['xor', 'x99', 'x51', 'x139', 'dx43'],
                                        ['xor', 'x104', 'x52', 'x140', 'dx44'], ['xor', 'x105', 'x53', 'x141', 'dx45'],
                                        ['xor', 'x106', 'x54', 'x142', 'dx46'], ['xor', 'x107', 'x55', 'x143', 'dx47'],
                                        ['xor', 'x116', 'x56', 'x144', 'dx48'], ['xor', 'x117', 'x57', 'x145', 'dx49'],
                                        ['xor', 'x118', 'x58', 'x146', 'dx50'], ['xor', 'x119', 'x59', 'x147', 'dx51'],
                                        ['xor', 'x124', 'x60', 'x148', 'dx52'], ['xor', 'x125', 'x61', 'x149', 'dx53'],
                                        ['xor', 'x126', 'x62', 'x150', 'dx54'], ['xor', 'x127', 'x63', 'x151', 'dx55'],
                                        ['xor', 'x112', 'x32', 'x152', 'dx56'], ['xor', 'x113', 'x33', 'x153', 'dx57'],
                                        ['xor', 'x114', 'x34', 'x154', 'dx58'], ['xor', 'x115', 'x35', 'x155', 'dx59'],
                                        ['xor', 'x120', 'x36', 'x156', 'dx60'], ['xor', 'x121', 'x37', 'x157', 'dx61'],
                                        ['xor', 'x122', 'x38', 'x158', 'dx62'], ['xor', 'x123', 'x39', 'x159', 'dx63']]

        print(cipher_instance.A)
        actual_key_xor_actions = cipher_instance.generate_key_xor_actions_for_round()
        actual_key_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_key_xor_actions]
        self.assertEqual(expected_key_xor_actions_round_1, actual_key_xor_actions_test_readable)

        for key_xor_action in actual_key_xor_actions:
            key_xor_action.run_action()

        print(cipher_instance.A)
        actual_sbox_actions = cipher_instance.generate_sbox_actions_for_round()
        actual_sbox_actions_test_readable = [
            [sboxaction.type_of_action, int(sboxaction.input_vars[0][1:]), int(sboxaction.output_vars[0][1:]),
             sboxaction.dummy_var] for sboxaction in actual_sbox_actions]
        self.assertEqual(expected_sbox_actions_round_1, actual_sbox_actions_test_readable)

        for sboxaction in actual_sbox_actions:
            sboxaction.run_action()
        print(cipher_instance.A)

        for permutation_action in cipher_instance.generate_permutation_after_sbox_actions_for_round():
            permutation_action.run_action()
        print(cipher_instance.A)
        for bitshift in cipher_instance.generate_bitshift_actions_for_round():
            bitshift.run_action()
        print(cipher_instance.A)

        actual_xor_actions = cipher_instance.generate_f_output_right_plaintext_xor_actions_for_round()
        actual_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_xor_actions]
        self.assertEqual(expected_xor_actions_round_1, actual_xor_actions_test_readable)
        for xor_action in actual_xor_actions:
            xor_action.run_action()
        print(cipher_instance.A)
        return

    def test_correct_actions_performed_round_2_bit_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=True)

        cipher_instance.run_round()

        expected_key_xor_actions_round_2 = [['xor', 'x128', 'k32', 'x160', 'dx64'],
                                            ['xor', 'x129', 'k33', 'x161', 'dx65'],
                                            ['xor', 'x130', 'k34', 'x162', 'dx66'],
                                            ['xor', 'x131', 'k35', 'x163', 'dx67'],
                                            ['xor', 'x132', 'k36', 'x164', 'dx68'],
                                            ['xor', 'x133', 'k37', 'x165', 'dx69'],
                                            ['xor', 'x134', 'k38', 'x166', 'dx70'],
                                            ['xor', 'x135', 'k39', 'x167', 'dx71'],
                                            ['xor', 'x136', 'k40', 'x168', 'dx72'],
                                            ['xor', 'x137', 'k41', 'x169', 'dx73'],
                                            ['xor', 'x138', 'k42', 'x170', 'dx74'],
                                            ['xor', 'x139', 'k43', 'x171', 'dx75'],
                                            ['xor', 'x140', 'k44', 'x172', 'dx76'],
                                            ['xor', 'x141', 'k45', 'x173', 'dx77'],
                                            ['xor', 'x142', 'k46', 'x174', 'dx78'],
                                            ['xor', 'x143', 'k47', 'x175', 'dx79'],
                                            ['xor', 'x144', 'k48', 'x176', 'dx80'],
                                            ['xor', 'x145', 'k49', 'x177', 'dx81'],
                                            ['xor', 'x146', 'k50', 'x178', 'dx82'],
                                            ['xor', 'x147', 'k51', 'x179', 'dx83'],
                                            ['xor', 'x148', 'k52', 'x180', 'dx84'],
                                            ['xor', 'x149', 'k53', 'x181', 'dx85'],
                                            ['xor', 'x150', 'k54', 'x182', 'dx86'],
                                            ['xor', 'x151', 'k55', 'x183', 'dx87'],
                                            ['xor', 'x152', 'k56', 'x184', 'dx88'],
                                            ['xor', 'x153', 'k57', 'x185', 'dx89'],
                                            ['xor', 'x154', 'k58', 'x186', 'dx90'],
                                            ['xor', 'x155', 'k59', 'x187', 'dx91'],
                                            ['xor', 'x156', 'k60', 'x188', 'dx92'],
                                            ['xor', 'x157', 'k61', 'x189', 'dx93'],
                                            ['xor', 'x158', 'k62', 'x190', 'dx94'],
                                            ['xor', 'x159', 'k63', 'x191', 'dx95']]

        expected_sbox_actions_round_2 = [['sbox', 160, 192, 'a8'], ['sbox', 164, 196, 'a9'], ['sbox', 168, 200, 'a10'],
                                         ['sbox', 172, 204, 'a11'], ['sbox', 176, 208, 'a12'],
                                         ['sbox', 180, 212, 'a13'],
                                         ['sbox', 184, 216, 'a14'], ['sbox', 188, 220, 'a15']]

        expected_xor_actions_round_2 = [['xor', 'x196', 'x8', 'x224', 'dx96'],
                                        ['xor', 'x197', 'x9', 'x225', 'dx97'],
                                        ['xor', 'x198', 'x10', 'x226', 'dx98'],
                                        ['xor', 'x199', 'x11', 'x227', 'dx99'],
                                        ['xor', 'x204', 'x12', 'x228', 'dx100'],
                                        ['xor', 'x205', 'x13', 'x229', 'dx101'],
                                        ['xor', 'x206', 'x14', 'x230', 'dx102'],
                                        ['xor', 'x207', 'x15', 'x231', 'dx103'],
                                        ['xor', 'x192', 'x16', 'x232', 'dx104'],
                                        ['xor', 'x193', 'x17', 'x233', 'dx105'],
                                        ['xor', 'x194', 'x18', 'x234', 'dx106'],
                                        ['xor', 'x195', 'x19', 'x235', 'dx107'],
                                        ['xor', 'x200', 'x20', 'x236', 'dx108'],
                                        ['xor', 'x201', 'x21', 'x237', 'dx109'],
                                        ['xor', 'x202', 'x22', 'x238', 'dx110'],
                                        ['xor', 'x203', 'x23', 'x239', 'dx111'],
                                        ['xor', 'x212', 'x24', 'x240', 'dx112'],
                                        ['xor', 'x213', 'x25', 'x241', 'dx113'],
                                        ['xor', 'x214', 'x26', 'x242', 'dx114'],
                                        ['xor', 'x215', 'x27', 'x243', 'dx115'],
                                        ['xor', 'x220', 'x28', 'x244', 'dx116'],
                                        ['xor', 'x221', 'x29', 'x245', 'dx117'],
                                        ['xor', 'x222', 'x30', 'x246', 'dx118'],
                                        ['xor', 'x223', 'x31', 'x247', 'dx119'],
                                        ['xor', 'x208', 'x0', 'x248', 'dx120'],
                                        ['xor', 'x209', 'x1', 'x249', 'dx121'],
                                        ['xor', 'x210', 'x2', 'x250', 'dx122'],
                                        ['xor', 'x211', 'x3', 'x251', 'dx123'],
                                        ['xor', 'x216', 'x4', 'x252', 'dx124'],
                                        ['xor', 'x217', 'x5', 'x253', 'dx125'],
                                        ['xor', 'x218', 'x6', 'x254', 'dx126'],
                                        ['xor', 'x219', 'x7', 'x255', 'dx127']]

        print(cipher_instance.A)
        actual_key_xor_actions = cipher_instance.generate_key_xor_actions_for_round()
        actual_key_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_key_xor_actions]
        self.assertEqual(expected_key_xor_actions_round_2, actual_key_xor_actions_test_readable)

        for key_xor_action in actual_key_xor_actions:
            key_xor_action.run_action()

        print(cipher_instance.A)
        actual_sbox_actions = cipher_instance.generate_sbox_actions_for_round()
        actual_sbox_actions_test_readable = [
            [sboxaction.type_of_action, int(sboxaction.input_vars[0][1:]), int(sboxaction.output_vars[0][1:]),
             sboxaction.dummy_var] for sboxaction in actual_sbox_actions]
        self.assertEqual(expected_sbox_actions_round_2, actual_sbox_actions_test_readable)

        for sboxaction in actual_sbox_actions:
            sboxaction.run_action()
        print(cipher_instance.A)

        for permutation_action in cipher_instance.generate_permutation_after_sbox_actions_for_round():
            permutation_action.run_action()
        print(cipher_instance.A)
        for bitshift in cipher_instance.generate_bitshift_actions_for_round():
            bitshift.run_action()
        print(cipher_instance.A)

        actual_xor_actions = cipher_instance.generate_f_output_right_plaintext_xor_actions_for_round()
        actual_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_xor_actions]
        self.assertEqual(expected_xor_actions_round_2, actual_xor_actions_test_readable)
        for xor_action in actual_xor_actions:
            xor_action.run_action()
        print(cipher_instance.A)
        return

    def test_round_progression_word_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=False)

        bits_before_round_1 = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
                               'x14', 'x15']
        self.assertEqual(cipher_instance.A, bits_before_round_1)

        cipher_instance.run_round()

        bits_before_round_2 = ['x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30', 'x31', 'x0', 'x1', 'x2', 'x3', 'x4',
                               'x5', 'x6', 'x7']
        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x24', 'x25', 'x26', 'x27',
                               'x28', 'x29', 'x30', 'x31']
        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def test_correct_actions_performed_round_1_word_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=False)

        expected_key_xor_actions_round_1 = [['xor', 'x0', 'k0', 'x16', 'dx0'], ['xor', 'x1', 'k1', 'x17', 'dx1'],
                                            ['xor', 'x2', 'k2', 'x18', 'dx2'], ['xor', 'x3', 'k3', 'x19', 'dx3'],
                                            ['xor', 'x4', 'k4', 'x20', 'dx4'], ['xor', 'x5', 'k5', 'x21', 'dx5'],
                                            ['xor', 'x6', 'k6', 'x22', 'dx6'], ['xor', 'x7', 'k7', 'x23', 'dx7']]
        expected_sbox_actions_round_1 = list()
        expected_xor_actions_round_1 = [['xor', 'x17', 'x10', 'x24', 'dx8'], ['xor', 'x19', 'x11', 'x25', 'dx9'],
                                        ['xor', 'x16', 'x12', 'x26', 'dx10'], ['xor', 'x18', 'x13', 'x27', 'dx11'],
                                        ['xor', 'x21', 'x14', 'x28', 'dx12'], ['xor', 'x23', 'x15', 'x29', 'dx13'],
                                        ['xor', 'x20', 'x8', 'x30', 'dx14'], ['xor', 'x22', 'x9', 'x31', 'dx15']]

        print(cipher_instance.A)
        actual_key_xor_actions = cipher_instance.generate_key_xor_actions_for_round()
        actual_key_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_key_xor_actions]
        self.assertEqual(expected_key_xor_actions_round_1, actual_key_xor_actions_test_readable)

        for key_xor_action in actual_key_xor_actions:
            key_xor_action.run_action()

        print(cipher_instance.A)
        actual_sbox_actions = cipher_instance.generate_sbox_actions_for_round()
        actual_sbox_actions_test_readable = [
            [sboxaction.type_of_action, int(sboxaction.input_vars[0][1:]), int(sboxaction.output_vars[0][1:]),
             sboxaction.dummy_var] for sboxaction in actual_sbox_actions]
        self.assertEqual(expected_sbox_actions_round_1, actual_sbox_actions_test_readable)

        for sboxaction in actual_sbox_actions:
            sboxaction.run_action()
        print(cipher_instance.A)

        for permutation_action in cipher_instance.generate_permutation_after_sbox_actions_for_round():
            permutation_action.run_action()
        print(cipher_instance.A)
        for bitshift in cipher_instance.generate_bitshift_actions_for_round():
            bitshift.run_action()
        print(cipher_instance.A)

        actual_xor_actions = cipher_instance.generate_f_output_right_plaintext_xor_actions_for_round()
        actual_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_xor_actions]
        self.assertEqual(expected_xor_actions_round_1, actual_xor_actions_test_readable)
        for xor_action in actual_xor_actions:
            xor_action.run_action()
        print(cipher_instance.A)
        return

    def test_correct_actions_performed_round_2_word_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=False)

        cipher_instance.run_round()

        expected_key_xor_actions_round_2 = [['xor', 'x24', 'k8', 'x32', 'dx16'], ['xor', 'x25', 'k9', 'x33', 'dx17'],
                                            ['xor', 'x26', 'k10', 'x34', 'dx18'], ['xor', 'x27', 'k11', 'x35', 'dx19'],
                                            ['xor', 'x28', 'k12', 'x36', 'dx20'], ['xor', 'x29', 'k13', 'x37', 'dx21'],
                                            ['xor', 'x30', 'k14', 'x38', 'dx22'], ['xor', 'x31', 'k15', 'x39', 'dx23']]
        expected_sbox_actions_round_2 = list()
        expected_xor_actions_round_2 = [['xor', 'x33', 'x2', 'x40', 'dx24'], ['xor', 'x35', 'x3', 'x41', 'dx25'],
                                        ['xor', 'x32', 'x4', 'x42', 'dx26'], ['xor', 'x34', 'x5', 'x43', 'dx27'],
                                        ['xor', 'x37', 'x6', 'x44', 'dx28'], ['xor', 'x39', 'x7', 'x45', 'dx29'],
                                        ['xor', 'x36', 'x0', 'x46', 'dx30'], ['xor', 'x38', 'x1', 'x47', 'dx31']]

        print(cipher_instance.A)
        actual_key_xor_actions = cipher_instance.generate_key_xor_actions_for_round()
        actual_key_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_key_xor_actions]
        self.assertEqual(expected_key_xor_actions_round_2, actual_key_xor_actions_test_readable)

        for key_xor_action in actual_key_xor_actions:
            key_xor_action.run_action()

        print(cipher_instance.A)
        actual_sbox_actions = cipher_instance.generate_sbox_actions_for_round()
        actual_sbox_actions_test_readable = [
            [sboxaction.type_of_action, int(sboxaction.input_vars[0][1:]), int(sboxaction.output_vars[0][1:]),
             sboxaction.dummy_var] for sboxaction in actual_sbox_actions]
        self.assertEqual(expected_sbox_actions_round_2, actual_sbox_actions_test_readable)

        for sboxaction in actual_sbox_actions:
            sboxaction.run_action()
        print(cipher_instance.A)

        for permutation_action in cipher_instance.generate_permutation_after_sbox_actions_for_round():
            permutation_action.run_action()
        print(cipher_instance.A)
        for bitshift in cipher_instance.generate_bitshift_actions_for_round():
            bitshift.run_action()
        print(cipher_instance.A)

        actual_xor_actions = cipher_instance.generate_f_output_right_plaintext_xor_actions_for_round()
        actual_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_xor_actions]
        self.assertEqual(expected_xor_actions_round_2, actual_xor_actions_test_readable)
        for xor_action in actual_xor_actions:
            xor_action.run_action()
        print(cipher_instance.A)
        return


if __name__ == '__main__':
    unittest.main()
