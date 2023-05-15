import unittest
from cipher.linear.lblock import LBlock


class LBlockTest(unittest.TestCase):
    def comparisons_and_run_round(self, cipher_instance, expected_tfb_actions, expected_sbox_actions):
        print(cipher_instance.A)
        # first we need to calculate the outputs of, depending on our orientation, 3-forked branched or sboxes
        for bitshift in cipher_instance.generate_bitshift_actions_for_round():
            bitshift.run_action()
        print(cipher_instance.A)
        output_vars = cipher_instance.calculate_output_vars_for_round()

        actual_twf_actions = cipher_instance.generate_threeforkedbranch_actions_for_round(output_vars)
        actual_twf_actions_test_readable = [
            [twf_action.type_of_action, twf_action.input_var, twf_action.output_var_1, twf_action.output_var_2,
             twf_action.dummy_var] for twf_action in actual_twf_actions]
        self.assertEqual(expected_tfb_actions, actual_twf_actions_test_readable)
        for twf_action in actual_twf_actions:
            twf_action.run_action()
        print(cipher_instance.A)

        actual_sbox_actions = cipher_instance.generate_sbox_actions_for_round(output_vars)
        actual_sbox_actions_test_readable = [
            [sboxaction.type_of_action, sboxaction.input_vars, sboxaction.output_vars,
             sboxaction.dummy_var] for sboxaction in actual_sbox_actions]
        self.assertEqual(expected_sbox_actions, actual_sbox_actions_test_readable)

        for sboxaction in actual_sbox_actions:
            sboxaction.run_action()
        print(cipher_instance.A)
        return

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

        bits_before_round_2 = ['x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50', 'x51',
                               'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x60', 'x61', 'x62', 'x63',
                               'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x65', 'x67', 'x69', 'x71',
                               'x73', 'x75', 'x77', 'x79', 'x81', 'x83', 'x85', 'x87', 'x89', 'x91', 'x93', 'x95',
                               'x97', 'x99', 'x101', 'x103', 'x105', 'x107', 'x109', 'x111', 'x113', 'x115', 'x117',
                               'x119', 'x121', 'x123', 'x125', 'x127']
        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x81', 'x83', 'x85', 'x87', 'x89', 'x91', 'x93', 'x95', 'x97', 'x99', 'x101', 'x103',
                               'x105', 'x107', 'x109', 'x111', 'x113', 'x115', 'x117', 'x119', 'x121', 'x123', 'x125',
                               'x127', 'x65', 'x67', 'x69', 'x71', 'x73', 'x75', 'x77', 'x79', 'x129', 'x131', 'x133',
                               'x135', 'x137', 'x139', 'x141', 'x143', 'x145', 'x147', 'x149', 'x151', 'x153', 'x155',
                               'x157', 'x159', 'x161', 'x163', 'x165', 'x167', 'x169', 'x171', 'x173', 'x175', 'x177',
                               'x179', 'x181', 'x183', 'x185', 'x187', 'x189', 'x191']
        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def test_correct_actions_performed_round_1_bit_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=True)

        expected_tfb_actions_round_1 = [['twf', 'x0', 'x64', 'x65', 'dt0'], ['twf', 'x1', 'x66', 'x67', 'dt1'],
                                        ['twf', 'x2', 'x68', 'x69', 'dt2'], ['twf', 'x3', 'x70', 'x71', 'dt3'],
                                        ['twf', 'x4', 'x72', 'x73', 'dt4'], ['twf', 'x5', 'x74', 'x75', 'dt5'],
                                        ['twf', 'x6', 'x76', 'x77', 'dt6'], ['twf', 'x7', 'x78', 'x79', 'dt7'],
                                        ['twf', 'x8', 'x80', 'x81', 'dt8'], ['twf', 'x9', 'x82', 'x83', 'dt9'],
                                        ['twf', 'x10', 'x84', 'x85', 'dt10'], ['twf', 'x11', 'x86', 'x87', 'dt11'],
                                        ['twf', 'x12', 'x88', 'x89', 'dt12'], ['twf', 'x13', 'x90', 'x91', 'dt13'],
                                        ['twf', 'x14', 'x92', 'x93', 'dt14'], ['twf', 'x15', 'x94', 'x95', 'dt15'],
                                        ['twf', 'x16', 'x96', 'x97', 'dt16'], ['twf', 'x17', 'x98', 'x99', 'dt17'],
                                        ['twf', 'x18', 'x100', 'x101', 'dt18'], ['twf', 'x19', 'x102', 'x103', 'dt19'],
                                        ['twf', 'x20', 'x104', 'x105', 'dt20'], ['twf', 'x21', 'x106', 'x107', 'dt21'],
                                        ['twf', 'x22', 'x108', 'x109', 'dt22'], ['twf', 'x23', 'x110', 'x111', 'dt23'],
                                        ['twf', 'x24', 'x112', 'x113', 'dt24'], ['twf', 'x25', 'x114', 'x115', 'dt25'],
                                        ['twf', 'x26', 'x116', 'x117', 'dt26'], ['twf', 'x27', 'x118', 'x119', 'dt27'],
                                        ['twf', 'x28', 'x120', 'x121', 'dt28'], ['twf', 'x29', 'x122', 'x123', 'dt29'],
                                        ['twf', 'x30', 'x124', 'x125', 'dt30'], ['twf', 'x31', 'x126', 'x127', 'dt31']]

        expected_sbox_actions_round_1 = [['sbox', ['x64', 'x66', 'x68', 'x70'], ['x44', 'x45', 'x46', 'x47'], 'a0'],
                                         ['sbox', ['x72', 'x74', 'x76', 'x78'], ['x52', 'x53', 'x54', 'x55'], 'a1'],
                                         ['sbox', ['x80', 'x82', 'x84', 'x86'], ['x40', 'x41', 'x42', 'x43'], 'a2'],
                                         ['sbox', ['x88', 'x90', 'x92', 'x94'], ['x48', 'x49', 'x50', 'x51'], 'a3'],
                                         ['sbox', ['x96', 'x98', 'x100', 'x102'], ['x60', 'x61', 'x62', 'x63'], 'a4'],
                                         ['sbox', ['x104', 'x106', 'x108', 'x110'], ['x36', 'x37', 'x38', 'x39'], 'a5'],
                                         ['sbox', ['x112', 'x114', 'x116', 'x118'], ['x56', 'x57', 'x58', 'x59'], 'a6'],
                                         ['sbox', ['x120', 'x122', 'x124', 'x126'], ['x32', 'x33', 'x34', 'x35'], 'a7']]

        self.comparisons_and_run_round(cipher_instance, expected_tfb_actions_round_1, expected_sbox_actions_round_1)
        return

    def test_correct_actions_performed_round_2_bit_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=True)

        cipher_instance.run_round()

        expected_tfb_actions_round_2 = [['twf', 'x40', 'x128', 'x129', 'dt32'], ['twf', 'x41', 'x130', 'x131', 'dt33'],
                                        ['twf', 'x42', 'x132', 'x133', 'dt34'], ['twf', 'x43', 'x134', 'x135', 'dt35'],
                                        ['twf', 'x44', 'x136', 'x137', 'dt36'], ['twf', 'x45', 'x138', 'x139', 'dt37'],
                                        ['twf', 'x46', 'x140', 'x141', 'dt38'], ['twf', 'x47', 'x142', 'x143', 'dt39'],
                                        ['twf', 'x48', 'x144', 'x145', 'dt40'], ['twf', 'x49', 'x146', 'x147', 'dt41'],
                                        ['twf', 'x50', 'x148', 'x149', 'dt42'], ['twf', 'x51', 'x150', 'x151', 'dt43'],
                                        ['twf', 'x52', 'x152', 'x153', 'dt44'], ['twf', 'x53', 'x154', 'x155', 'dt45'],
                                        ['twf', 'x54', 'x156', 'x157', 'dt46'], ['twf', 'x55', 'x158', 'x159', 'dt47'],
                                        ['twf', 'x56', 'x160', 'x161', 'dt48'], ['twf', 'x57', 'x162', 'x163', 'dt49'],
                                        ['twf', 'x58', 'x164', 'x165', 'dt50'], ['twf', 'x59', 'x166', 'x167', 'dt51'],
                                        ['twf', 'x60', 'x168', 'x169', 'dt52'], ['twf', 'x61', 'x170', 'x171', 'dt53'],
                                        ['twf', 'x62', 'x172', 'x173', 'dt54'], ['twf', 'x63', 'x174', 'x175', 'dt55'],
                                        ['twf', 'x32', 'x176', 'x177', 'dt56'], ['twf', 'x33', 'x178', 'x179', 'dt57'],
                                        ['twf', 'x34', 'x180', 'x181', 'dt58'], ['twf', 'x35', 'x182', 'x183', 'dt59'],
                                        ['twf', 'x36', 'x184', 'x185', 'dt60'], ['twf', 'x37', 'x186', 'x187', 'dt61'],
                                        ['twf', 'x38', 'x188', 'x189', 'dt62'], ['twf', 'x39', 'x190', 'x191', 'dt63']]
        expected_sbox_actions_round_2 = [['sbox', ['x128', 'x130', 'x132', 'x134'], ['x89', 'x91', 'x93', 'x95'], 'a8'],
                                         ['sbox', ['x136', 'x138', 'x140', 'x142'], ['x105', 'x107', 'x109', 'x111'],
                                          'a9'],
                                         ['sbox', ['x144', 'x146', 'x148', 'x150'], ['x81', 'x83', 'x85', 'x87'],
                                          'a10'],
                                         ['sbox', ['x152', 'x154', 'x156', 'x158'], ['x97', 'x99', 'x101', 'x103'],
                                          'a11'],
                                         ['sbox', ['x160', 'x162', 'x164', 'x166'], ['x121', 'x123', 'x125', 'x127'],
                                          'a12'],
                                         ['sbox', ['x168', 'x170', 'x172', 'x174'], ['x73', 'x75', 'x77', 'x79'],
                                          'a13'],
                                         ['sbox', ['x176', 'x178', 'x180', 'x182'], ['x113', 'x115', 'x117', 'x119'],
                                          'a14'],
                                         ['sbox', ['x184', 'x186', 'x188', 'x190'], ['x65', 'x67', 'x69', 'x71'],
                                          'a15']]

        self.comparisons_and_run_round(cipher_instance, expected_tfb_actions_round_2, expected_sbox_actions_round_2)
        return

    def test_round_progression_word_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=False)

        bits_before_round_1 = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
                               'x14', 'x15']
        self.assertEqual(cipher_instance.A, bits_before_round_1)

        cipher_instance.run_round()

        bits_before_round_2 = ['x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x8', 'x9', 'x16', 'x17', 'x18', 'x19', 'x20',
                               'x21', 'x22', 'x23']
        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x16', 'x17', 'x24', 'x25', 'x26', 'x27',
                               'x28', 'x29', 'x30', 'x31']
        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def test_correct_actions_performed_round_1_word_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=False)

        expected_tfb_actions_round_1 = [['twf', 'x0', 'x16', 'x11', 'dt0'], ['twf', 'x1', 'x17', 'x13', 'dt1'],
                                        ['twf', 'x2', 'x18', 'x10', 'dt2'], ['twf', 'x3', 'x19', 'x12', 'dt3'],
                                        ['twf', 'x4', 'x20', 'x15', 'dt4'], ['twf', 'x5', 'x21', 'x9', 'dt5'],
                                        ['twf', 'x6', 'x22', 'x14', 'dt6'], ['twf', 'x7', 'x23', 'x8', 'dt7']]
        expected_sbox_actions_round_1 = list()

        self.comparisons_and_run_round(cipher_instance, expected_tfb_actions_round_1, expected_sbox_actions_round_1)
        return

    def test_correct_actions_performed_round_2_word_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=False)

        cipher_instance.run_round()

        expected_tfb_actions_round_2 = [['twf', 'x10', 'x24', 'x19', 'dt8'], ['twf', 'x11', 'x25', 'x21', 'dt9'],
                                        ['twf', 'x12', 'x26', 'x18', 'dt10'], ['twf', 'x13', 'x27', 'x20', 'dt11'],
                                        ['twf', 'x14', 'x28', 'x23', 'dt12'], ['twf', 'x15', 'x29', 'x17', 'dt13'],
                                        ['twf', 'x8', 'x30', 'x22', 'dt14'], ['twf', 'x9', 'x31', 'x16', 'dt15']]
        expected_sbox_actions_round_2 = list()

        self.comparisons_and_run_round(cipher_instance, expected_tfb_actions_round_2, expected_sbox_actions_round_2)
        return


if __name__ == '__main__':
    unittest.main()
