import unittest
from cipher.linear.aes import Aes


class AESTest(unittest.TestCase):
    def test_round_progression_bit_oriented(self):
        cipher_instance = Aes(rounds=4, model_as_bit_oriented=True)

        bits_before_round_1 = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
                               'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25',
                               'x26', 'x27', 'x28', 'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37',
                               'x38', 'x39', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49',
                               'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x60', 'x61',
                               'x62', 'x63', 'x64', 'x65', 'x66', 'x67', 'x68', 'x69', 'x70', 'x71', 'x72', 'x73',
                               'x74', 'x75', 'x76', 'x77', 'x78', 'x79', 'x80', 'x81', 'x82', 'x83', 'x84', 'x85',
                               'x86', 'x87', 'x88', 'x89', 'x90', 'x91', 'x92', 'x93', 'x94', 'x95', 'x96', 'x97',
                               'x98', 'x99', 'x100', 'x101', 'x102', 'x103', 'x104', 'x105', 'x106', 'x107', 'x108',
                               'x109', 'x110', 'x111', 'x112', 'x113', 'x114', 'x115', 'x116', 'x117', 'x118', 'x119',
                               'x120', 'x121', 'x122', 'x123', 'x124', 'x125', 'x126', 'x127']

        self.assertEqual(cipher_instance.A, bits_before_round_1)

        cipher_instance.run_round()

        bits_before_round_2 = ['x256', 'x257', 'x258', 'x259', 'x260', 'x261', 'x262', 'x263', 'x264', 'x265', 'x266',
                               'x267', 'x268', 'x269', 'x270', 'x271', 'x272', 'x273', 'x274', 'x275', 'x276', 'x277',
                               'x278', 'x279', 'x280', 'x281', 'x282', 'x283', 'x284', 'x285', 'x286', 'x287', 'x288',
                               'x289', 'x290', 'x291', 'x292', 'x293', 'x294', 'x295', 'x296', 'x297', 'x298', 'x299',
                               'x300', 'x301', 'x302', 'x303', 'x304', 'x305', 'x306', 'x307', 'x308', 'x309', 'x310',
                               'x311', 'x312', 'x313', 'x314', 'x315', 'x316', 'x317', 'x318', 'x319', 'x320', 'x321',
                               'x322', 'x323', 'x324', 'x325', 'x326', 'x327', 'x328', 'x329', 'x330', 'x331', 'x332',
                               'x333', 'x334', 'x335', 'x336', 'x337', 'x338', 'x339', 'x340', 'x341', 'x342', 'x343',
                               'x344', 'x345', 'x346', 'x347', 'x348', 'x349', 'x350', 'x351', 'x352', 'x353', 'x354',
                               'x355', 'x356', 'x357', 'x358', 'x359', 'x360', 'x361', 'x362', 'x363', 'x364', 'x365',
                               'x366', 'x367', 'x368', 'x369', 'x370', 'x371', 'x372', 'x373', 'x374', 'x375', 'x376',
                               'x377', 'x378', 'x379', 'x380', 'x381', 'x382', 'x383']

        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x512', 'x513', 'x514', 'x515', 'x516', 'x517', 'x518', 'x519', 'x520', 'x521', 'x522',
                               'x523', 'x524', 'x525', 'x526', 'x527', 'x528', 'x529', 'x530', 'x531', 'x532', 'x533',
                               'x534', 'x535', 'x536', 'x537', 'x538', 'x539', 'x540', 'x541', 'x542', 'x543', 'x544',
                               'x545', 'x546', 'x547', 'x548', 'x549', 'x550', 'x551', 'x552', 'x553', 'x554', 'x555',
                               'x556', 'x557', 'x558', 'x559', 'x560', 'x561', 'x562', 'x563', 'x564', 'x565', 'x566',
                               'x567', 'x568', 'x569', 'x570', 'x571', 'x572', 'x573', 'x574', 'x575', 'x576', 'x577',
                               'x578', 'x579', 'x580', 'x581', 'x582', 'x583', 'x584', 'x585', 'x586', 'x587', 'x588',
                               'x589', 'x590', 'x591', 'x592', 'x593', 'x594', 'x595', 'x596', 'x597', 'x598', 'x599',
                               'x600', 'x601', 'x602', 'x603', 'x604', 'x605', 'x606', 'x607', 'x608', 'x609', 'x610',
                               'x611', 'x612', 'x613', 'x614', 'x615', 'x616', 'x617', 'x618', 'x619', 'x620', 'x621',
                               'x622', 'x623', 'x624', 'x625', 'x626', 'x627', 'x628', 'x629', 'x630', 'x631', 'x632',
                               'x633', 'x634', 'x635', 'x636', 'x637', 'x638', 'x639']

        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def round_testing_given_parameters(self, cipher_instance, expected_sbox_actions_round, expected_A_before_shift_rows,
                                       expected_A_after_shift_rows, expected_mixcolumns_actions):

        actual_sbox_actions = cipher_instance.generate_sbox_actions_for_round()
        actual_sbox_actions_test_readable = [
            [sboxaction.type_of_action, sboxaction.input_vars, sboxaction.output_vars,
             sboxaction.dummy_var] for sboxaction in actual_sbox_actions]
        self.assertEqual(expected_sbox_actions_round, actual_sbox_actions_test_readable)
        print(expected_sbox_actions_round)
        print(actual_sbox_actions_test_readable)

        for sboxaction in actual_sbox_actions:
            sboxaction.run_action()
        print(cipher_instance.A)

        self.assertEqual(expected_A_before_shift_rows, cipher_instance.A)

        for shiftrowsaction in cipher_instance.generate_shift_rows_actions_for_round():
            shiftrowsaction.run_action()

        self.assertEqual(expected_A_after_shift_rows, cipher_instance.A)

        actual_mixcolumns_actions = cipher_instance.generate_mix_columns_actions_for_round()
        actual_mixcolumns_actions_text_readable = [
            [action.type_of_action, action.input_list, action.output_list, action.dummy_var] for action in
            actual_mixcolumns_actions]
        for mixcolumnsaction in actual_mixcolumns_actions:
            mixcolumnsaction.run_action()
        self.assertEqual(expected_mixcolumns_actions, actual_mixcolumns_actions_text_readable)

        return

    def test_correct_actions_performed_round_1_bit_oriented(self):
        cipher_instance = Aes(rounds=4, model_as_bit_oriented=True)

        expected_sbox_actions_round_1 = [['sbox', ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'],
                                          ['x128', 'x129', 'x130', 'x131', 'x132', 'x133', 'x134', 'x135'], 'a0'],
                                         ['sbox', ['x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15'],
                                          ['x136', 'x137', 'x138', 'x139', 'x140', 'x141', 'x142', 'x143'], 'a1'],
                                         ['sbox', ['x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23'],
                                          ['x144', 'x145', 'x146', 'x147', 'x148', 'x149', 'x150', 'x151'], 'a2'],
                                         ['sbox', ['x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x30', 'x31'],
                                          ['x152', 'x153', 'x154', 'x155', 'x156', 'x157', 'x158', 'x159'], 'a3'],
                                         ['sbox', ['x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39'],
                                          ['x160', 'x161', 'x162', 'x163', 'x164', 'x165', 'x166', 'x167'], 'a4'],
                                         ['sbox', ['x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47'],
                                          ['x168', 'x169', 'x170', 'x171', 'x172', 'x173', 'x174', 'x175'], 'a5'],
                                         ['sbox', ['x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55'],
                                          ['x176', 'x177', 'x178', 'x179', 'x180', 'x181', 'x182', 'x183'], 'a6'],
                                         ['sbox', ['x56', 'x57', 'x58', 'x59', 'x60', 'x61', 'x62', 'x63'],
                                          ['x184', 'x185', 'x186', 'x187', 'x188', 'x189', 'x190', 'x191'], 'a7'],
                                         ['sbox', ['x64', 'x65', 'x66', 'x67', 'x68', 'x69', 'x70', 'x71'],
                                          ['x192', 'x193', 'x194', 'x195', 'x196', 'x197', 'x198', 'x199'], 'a8'],
                                         ['sbox', ['x72', 'x73', 'x74', 'x75', 'x76', 'x77', 'x78', 'x79'],
                                          ['x200', 'x201', 'x202', 'x203', 'x204', 'x205', 'x206', 'x207'], 'a9'],
                                         ['sbox', ['x80', 'x81', 'x82', 'x83', 'x84', 'x85', 'x86', 'x87'],
                                          ['x208', 'x209', 'x210', 'x211', 'x212', 'x213', 'x214', 'x215'], 'a10'],
                                         ['sbox', ['x88', 'x89', 'x90', 'x91', 'x92', 'x93', 'x94', 'x95'],
                                          ['x216', 'x217', 'x218', 'x219', 'x220', 'x221', 'x222', 'x223'], 'a11'],
                                         ['sbox', ['x96', 'x97', 'x98', 'x99', 'x100', 'x101', 'x102', 'x103'],
                                          ['x224', 'x225', 'x226', 'x227', 'x228', 'x229', 'x230', 'x231'], 'a12'],
                                         ['sbox', ['x104', 'x105', 'x106', 'x107', 'x108', 'x109', 'x110', 'x111'],
                                          ['x232', 'x233', 'x234', 'x235', 'x236', 'x237', 'x238', 'x239'], 'a13'],
                                         ['sbox', ['x112', 'x113', 'x114', 'x115', 'x116', 'x117', 'x118', 'x119'],
                                          ['x240', 'x241', 'x242', 'x243', 'x244', 'x245', 'x246', 'x247'], 'a14'],
                                         ['sbox', ['x120', 'x121', 'x122', 'x123', 'x124', 'x125', 'x126', 'x127'],
                                          ['x248', 'x249', 'x250', 'x251', 'x252', 'x253', 'x254', 'x255'], 'a15']]

        round_1_A_before_shift_rows = ['x128', 'x129', 'x130', 'x131', 'x132', 'x133', 'x134', 'x135', 'x136', 'x137',
                                       'x138', 'x139', 'x140', 'x141', 'x142', 'x143', 'x144', 'x145', 'x146', 'x147',
                                       'x148', 'x149', 'x150', 'x151', 'x152', 'x153', 'x154', 'x155', 'x156', 'x157',
                                       'x158', 'x159', 'x160', 'x161', 'x162', 'x163', 'x164', 'x165', 'x166', 'x167',
                                       'x168', 'x169', 'x170', 'x171', 'x172', 'x173', 'x174', 'x175', 'x176', 'x177',
                                       'x178', 'x179', 'x180', 'x181', 'x182', 'x183', 'x184', 'x185', 'x186', 'x187',
                                       'x188', 'x189', 'x190', 'x191', 'x192', 'x193', 'x194', 'x195', 'x196', 'x197',
                                       'x198', 'x199', 'x200', 'x201', 'x202', 'x203', 'x204', 'x205', 'x206', 'x207',
                                       'x208', 'x209', 'x210', 'x211', 'x212', 'x213', 'x214', 'x215', 'x216', 'x217',
                                       'x218', 'x219', 'x220', 'x221', 'x222', 'x223', 'x224', 'x225', 'x226', 'x227',
                                       'x228', 'x229', 'x230', 'x231', 'x232', 'x233', 'x234', 'x235', 'x236', 'x237',
                                       'x238', 'x239', 'x240', 'x241', 'x242', 'x243', 'x244', 'x245', 'x246', 'x247',
                                       'x248', 'x249', 'x250', 'x251', 'x252', 'x253', 'x254', 'x255']

        round_1_A_after_shift_rows = ['x128', 'x129', 'x130', 'x131', 'x132', 'x133', 'x134', 'x135', 'x168', 'x169',
                                      'x170', 'x171', 'x172', 'x173', 'x174', 'x175', 'x208', 'x209', 'x210', 'x211',
                                      'x212', 'x213', 'x214', 'x215', 'x248', 'x249', 'x250', 'x251', 'x252', 'x253',
                                      'x254', 'x255', 'x160', 'x161', 'x162', 'x163', 'x164', 'x165', 'x166', 'x167',
                                      'x200', 'x201', 'x202', 'x203', 'x204', 'x205', 'x206', 'x207', 'x240', 'x241',
                                      'x242', 'x243', 'x244', 'x245', 'x246', 'x247', 'x152', 'x153', 'x154', 'x155',
                                      'x156', 'x157', 'x158', 'x159', 'x192', 'x193', 'x194', 'x195', 'x196', 'x197',
                                      'x198', 'x199', 'x232', 'x233', 'x234', 'x235', 'x236', 'x237', 'x238', 'x239',
                                      'x144', 'x145', 'x146', 'x147', 'x148', 'x149', 'x150', 'x151', 'x184', 'x185',
                                      'x186', 'x187', 'x188', 'x189', 'x190', 'x191', 'x224', 'x225', 'x226', 'x227',
                                      'x228', 'x229', 'x230', 'x231', 'x136', 'x137', 'x138', 'x139', 'x140', 'x141',
                                      'x142', 'x143', 'x176', 'x177', 'x178', 'x179', 'x180', 'x181', 'x182', 'x183',
                                      'x216', 'x217', 'x218', 'x219', 'x220', 'x221', 'x222', 'x223']

        expected_mixcolumns_actions_round_1 = [['lin trans',
                                                ['x128', 'x129', 'x130', 'x131', 'x132', 'x133', 'x134', 'x135', 'x168',
                                                 'x169', 'x170', 'x171', 'x172', 'x173', 'x174', 'x175', 'x208', 'x209',
                                                 'x210', 'x211', 'x212', 'x213', 'x214', 'x215', 'x248', 'x249', 'x250',
                                                 'x251', 'x252', 'x253', 'x254', 'x255'],
                                                ['x256', 'x257', 'x258', 'x259', 'x260', 'x261', 'x262', 'x263', 'x264',
                                                 'x265', 'x266', 'x267', 'x268', 'x269', 'x270', 'x271', 'x272', 'x273',
                                                 'x274', 'x275', 'x276', 'x277', 'x278', 'x279', 'x280', 'x281', 'x282',
                                                 'x283', 'x284', 'x285', 'x286', 'x287'], 'dl0'],
                                               ['lin trans',
                                                ['x160', 'x161', 'x162', 'x163', 'x164', 'x165', 'x166', 'x167', 'x200',
                                                 'x201', 'x202', 'x203', 'x204', 'x205', 'x206', 'x207', 'x240', 'x241',
                                                 'x242', 'x243', 'x244', 'x245', 'x246', 'x247', 'x152', 'x153', 'x154',
                                                 'x155', 'x156', 'x157', 'x158', 'x159'],
                                                ['x288', 'x289', 'x290', 'x291', 'x292', 'x293', 'x294', 'x295', 'x296',
                                                 'x297', 'x298', 'x299', 'x300', 'x301', 'x302', 'x303', 'x304', 'x305',
                                                 'x306', 'x307', 'x308', 'x309', 'x310', 'x311', 'x312', 'x313', 'x314',
                                                 'x315', 'x316', 'x317', 'x318', 'x319'], 'dl1'],
                                               ['lin trans',
                                                ['x192', 'x193', 'x194', 'x195', 'x196', 'x197', 'x198', 'x199', 'x232',
                                                 'x233', 'x234', 'x235', 'x236', 'x237', 'x238', 'x239', 'x144', 'x145',
                                                 'x146', 'x147', 'x148', 'x149', 'x150', 'x151', 'x184', 'x185', 'x186',
                                                 'x187', 'x188', 'x189', 'x190', 'x191'],
                                                ['x320', 'x321', 'x322', 'x323', 'x324', 'x325', 'x326', 'x327', 'x328',
                                                 'x329', 'x330', 'x331', 'x332', 'x333', 'x334', 'x335', 'x336', 'x337',
                                                 'x338', 'x339', 'x340', 'x341', 'x342', 'x343', 'x344', 'x345', 'x346',
                                                 'x347', 'x348', 'x349', 'x350', 'x351'], 'dl2'],
                                               ['lin trans',
                                                ['x224', 'x225', 'x226', 'x227', 'x228', 'x229', 'x230', 'x231', 'x136',
                                                 'x137', 'x138', 'x139', 'x140', 'x141', 'x142', 'x143', 'x176', 'x177',
                                                 'x178', 'x179', 'x180', 'x181', 'x182', 'x183', 'x216', 'x217', 'x218',
                                                 'x219', 'x220', 'x221', 'x222', 'x223'],
                                                ['x352', 'x353', 'x354', 'x355', 'x356', 'x357', 'x358', 'x359', 'x360',
                                                 'x361', 'x362', 'x363', 'x364', 'x365', 'x366', 'x367', 'x368', 'x369',
                                                 'x370', 'x371', 'x372', 'x373', 'x374', 'x375', 'x376', 'x377', 'x378',
                                                 'x379', 'x380', 'x381', 'x382', 'x383'], 'dl3']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_1, round_1_A_before_shift_rows,
                                            round_1_A_after_shift_rows, expected_mixcolumns_actions_round_1)
        return

    def test_round_progression_word_oriented(self):
        cipher_instance = Aes(rounds=4, model_as_bit_oriented=False)

        bits_before_round_1 = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
                               'x14', 'x15']
        self.assertEqual(cipher_instance.A, bits_before_round_1)

        cipher_instance.run_round()

        bits_before_round_2 = ['x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27',
                               'x28', 'x29', 'x30', 'x31']

        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42', 'x43',
                               'x44', 'x45', 'x46', 'x47']

        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def test_correct_actions_performed_round_1_word_oriented(self):
        cipher_instance = Aes(rounds=4, model_as_bit_oriented=False)

        expected_sbox_actions_round_1 = list()

        round_1_A_before_shift_rows = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12',
                                       'x13', 'x14', 'x15']

        round_1_A_after_shift_rows = ['x0', 'x5', 'x10', 'x15', 'x4', 'x9', 'x14', 'x3', 'x8', 'x13', 'x2', 'x7', 'x12',
                                      'x1', 'x6', 'x11']

        expected_mixcolumns_actions_round_1 = [
            ['lin trans', ['x0', 'x5', 'x10', 'x15'], ['x16', 'x17', 'x18', 'x19'], 'dl0'],
            ['lin trans', ['x4', 'x9', 'x14', 'x3'], ['x20', 'x21', 'x22', 'x23'], 'dl1'],
            ['lin trans', ['x8', 'x13', 'x2', 'x7'], ['x24', 'x25', 'x26', 'x27'], 'dl2'],
            ['lin trans', ['x12', 'x1', 'x6', 'x11'], ['x28', 'x29', 'x30', 'x31'], 'dl3']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_1, round_1_A_before_shift_rows,
                                            round_1_A_after_shift_rows, expected_mixcolumns_actions_round_1)
        return

    def test_correct_actions_performed_round_2_word_oriented(self):
        cipher_instance = Aes(rounds=4, model_as_bit_oriented=False)

        cipher_instance.run_round()

        expected_sbox_actions_round_2 = list()

        round_2_A_before_shift_rows = ['x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26',
                                       'x27', 'x28', 'x29', 'x30', 'x31']

        round_2_A_after_shift_rows = ['x16', 'x21', 'x26', 'x31', 'x20', 'x25', 'x30', 'x19', 'x24', 'x29', 'x18',
                                      'x23', 'x28', 'x17', 'x22', 'x27']

        expected_mixcolumns_actions_round_2 = [
            ['lin trans', ['x16', 'x21', 'x26', 'x31'], ['x32', 'x33', 'x34', 'x35'], 'dl4'],
            ['lin trans', ['x20', 'x25', 'x30', 'x19'], ['x36', 'x37', 'x38', 'x39'], 'dl5'],
            ['lin trans', ['x24', 'x29', 'x18', 'x23'], ['x40', 'x41', 'x42', 'x43'], 'dl6'],
            ['lin trans', ['x28', 'x17', 'x22', 'x27'], ['x44', 'x45', 'x46', 'x47'], 'dl7']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_2, round_2_A_before_shift_rows,
                                            round_2_A_after_shift_rows, expected_mixcolumns_actions_round_2)
        return


if __name__ == '__main__':
    unittest.main()
