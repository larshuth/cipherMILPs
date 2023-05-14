import unittest
from cipher.differential.aes import Aes
from cipher.actions import SBoxAction, XorAction, PermutationAction, OverwriteAction


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

        bits_before_round_2 = ['x512', 'x513', 'x514', 'x515', 'x516', 'x517', 'x518', 'x519', 'x520', 'x521', 'x522',
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

        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x896', 'x897', 'x898', 'x899', 'x900', 'x901', 'x902', 'x903', 'x904', 'x905', 'x906',
                               'x907', 'x908', 'x909', 'x910', 'x911', 'x912', 'x913', 'x914', 'x915', 'x916', 'x917',
                               'x918', 'x919', 'x920', 'x921', 'x922', 'x923', 'x924', 'x925', 'x926', 'x927', 'x928',
                               'x929', 'x930', 'x931', 'x932', 'x933', 'x934', 'x935', 'x936', 'x937', 'x938', 'x939',
                               'x940', 'x941', 'x942', 'x943', 'x944', 'x945', 'x946', 'x947', 'x948', 'x949', 'x950',
                               'x951', 'x952', 'x953', 'x954', 'x955', 'x956', 'x957', 'x958', 'x959', 'x960', 'x961',
                               'x962', 'x963', 'x964', 'x965', 'x966', 'x967', 'x968', 'x969', 'x970', 'x971', 'x972',
                               'x973', 'x974', 'x975', 'x976', 'x977', 'x978', 'x979', 'x980', 'x981', 'x982', 'x983',
                               'x984', 'x985', 'x986', 'x987', 'x988', 'x989', 'x990', 'x991', 'x992', 'x993', 'x994',
                               'x995', 'x996', 'x997', 'x998', 'x999', 'x1000', 'x1001', 'x1002', 'x1003', 'x1004',
                               'x1005', 'x1006', 'x1007', 'x1008', 'x1009', 'x1010', 'x1011', 'x1012', 'x1013', 'x1014',
                               'x1015', 'x1016', 'x1017', 'x1018', 'x1019', 'x1020', 'x1021', 'x1022', 'x1023']

        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def round_testing_given_parameters(self, cipher_instance, expected_sbox_actions_round, expected_A_before_shift_rows,
                                       expected_A_after_shift_rows, expected_mixcolumns_actions,
                                       expected_key_xor_actions, expected_key_xor_actions_pre_round=None):
        if expected_key_xor_actions_pre_round:
            actual_key_xor_actions = cipher_instance.generate_key_xor_actions_for_round()
            actual_key_xor_actions_test_readable = [
                [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
                 xoraction.dummy_var] for xoraction in actual_key_xor_actions]
            self.assertEqual(expected_key_xor_actions_pre_round, actual_key_xor_actions_test_readable)

            for keyaction in actual_key_xor_actions:
                keyaction.run_action()
            cipher_instance.K = ['k' + str(cipher_instance.round_number * cipher_instance.key_vars + i) for i in
                                 range(cipher_instance.key_vars)]

        actual_sbox_actions = cipher_instance.generate_sbox_actions_for_round()
        actual_sbox_actions_test_readable = [
            [sboxaction.type_of_action, int(sboxaction.input_vars[0][1:]), int(sboxaction.output_vars[0][1:]),
             sboxaction.dummy_var] for sboxaction in actual_sbox_actions]
        self.assertEqual(expected_sbox_actions_round, actual_sbox_actions_test_readable)

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

        actual_key_xor_actions = cipher_instance.generate_key_xor_actions_for_round()
        actual_key_xor_actions_test_readable = [
            [xoraction.type_of_action, xoraction.input_var_1, xoraction.input_var_2, xoraction.output_var,
             xoraction.dummy_var] for xoraction in actual_key_xor_actions]
        self.assertEqual(expected_key_xor_actions, actual_key_xor_actions_test_readable)
        return

    def test_correct_actions_performed_round_1_bit_oriented(self):
        cipher_instance = Aes(rounds=4, model_as_bit_oriented=True)

        expected_key_xor_actions_pre_round_1 = [['xor', 'x0', 'k0', 'x128', 'dx0'], ['xor', 'x1', 'k1', 'x129', 'dx1'],
                                                ['xor', 'x2', 'k2', 'x130', 'dx2'], ['xor', 'x3', 'k3', 'x131', 'dx3'],
                                                ['xor', 'x4', 'k4', 'x132', 'dx4'], ['xor', 'x5', 'k5', 'x133', 'dx5'],
                                                ['xor', 'x6', 'k6', 'x134', 'dx6'], ['xor', 'x7', 'k7', 'x135', 'dx7'],
                                                ['xor', 'x8', 'k8', 'x136', 'dx8'], ['xor', 'x9', 'k9', 'x137', 'dx9'],
                                                ['xor', 'x10', 'k10', 'x138', 'dx10'],
                                                ['xor', 'x11', 'k11', 'x139', 'dx11'],
                                                ['xor', 'x12', 'k12', 'x140', 'dx12'],
                                                ['xor', 'x13', 'k13', 'x141', 'dx13'],
                                                ['xor', 'x14', 'k14', 'x142', 'dx14'],
                                                ['xor', 'x15', 'k15', 'x143', 'dx15'],
                                                ['xor', 'x16', 'k16', 'x144', 'dx16'],
                                                ['xor', 'x17', 'k17', 'x145', 'dx17'],
                                                ['xor', 'x18', 'k18', 'x146', 'dx18'],
                                                ['xor', 'x19', 'k19', 'x147', 'dx19'],
                                                ['xor', 'x20', 'k20', 'x148', 'dx20'],
                                                ['xor', 'x21', 'k21', 'x149', 'dx21'],
                                                ['xor', 'x22', 'k22', 'x150', 'dx22'],
                                                ['xor', 'x23', 'k23', 'x151', 'dx23'],
                                                ['xor', 'x24', 'k24', 'x152', 'dx24'],
                                                ['xor', 'x25', 'k25', 'x153', 'dx25'],
                                                ['xor', 'x26', 'k26', 'x154', 'dx26'],
                                                ['xor', 'x27', 'k27', 'x155', 'dx27'],
                                                ['xor', 'x28', 'k28', 'x156', 'dx28'],
                                                ['xor', 'x29', 'k29', 'x157', 'dx29'],
                                                ['xor', 'x30', 'k30', 'x158', 'dx30'],
                                                ['xor', 'x31', 'k31', 'x159', 'dx31'],
                                                ['xor', 'x32', 'k32', 'x160', 'dx32'],
                                                ['xor', 'x33', 'k33', 'x161', 'dx33'],
                                                ['xor', 'x34', 'k34', 'x162', 'dx34'],
                                                ['xor', 'x35', 'k35', 'x163', 'dx35'],
                                                ['xor', 'x36', 'k36', 'x164', 'dx36'],
                                                ['xor', 'x37', 'k37', 'x165', 'dx37'],
                                                ['xor', 'x38', 'k38', 'x166', 'dx38'],
                                                ['xor', 'x39', 'k39', 'x167', 'dx39'],
                                                ['xor', 'x40', 'k40', 'x168', 'dx40'],
                                                ['xor', 'x41', 'k41', 'x169', 'dx41'],
                                                ['xor', 'x42', 'k42', 'x170', 'dx42'],
                                                ['xor', 'x43', 'k43', 'x171', 'dx43'],
                                                ['xor', 'x44', 'k44', 'x172', 'dx44'],
                                                ['xor', 'x45', 'k45', 'x173', 'dx45'],
                                                ['xor', 'x46', 'k46', 'x174', 'dx46'],
                                                ['xor', 'x47', 'k47', 'x175', 'dx47'],
                                                ['xor', 'x48', 'k48', 'x176', 'dx48'],
                                                ['xor', 'x49', 'k49', 'x177', 'dx49'],
                                                ['xor', 'x50', 'k50', 'x178', 'dx50'],
                                                ['xor', 'x51', 'k51', 'x179', 'dx51'],
                                                ['xor', 'x52', 'k52', 'x180', 'dx52'],
                                                ['xor', 'x53', 'k53', 'x181', 'dx53'],
                                                ['xor', 'x54', 'k54', 'x182', 'dx54'],
                                                ['xor', 'x55', 'k55', 'x183', 'dx55'],
                                                ['xor', 'x56', 'k56', 'x184', 'dx56'],
                                                ['xor', 'x57', 'k57', 'x185', 'dx57'],
                                                ['xor', 'x58', 'k58', 'x186', 'dx58'],
                                                ['xor', 'x59', 'k59', 'x187', 'dx59'],
                                                ['xor', 'x60', 'k60', 'x188', 'dx60'],
                                                ['xor', 'x61', 'k61', 'x189', 'dx61'],
                                                ['xor', 'x62', 'k62', 'x190', 'dx62'],
                                                ['xor', 'x63', 'k63', 'x191', 'dx63'],
                                                ['xor', 'x64', 'k64', 'x192', 'dx64'],
                                                ['xor', 'x65', 'k65', 'x193', 'dx65'],
                                                ['xor', 'x66', 'k66', 'x194', 'dx66'],
                                                ['xor', 'x67', 'k67', 'x195', 'dx67'],
                                                ['xor', 'x68', 'k68', 'x196', 'dx68'],
                                                ['xor', 'x69', 'k69', 'x197', 'dx69'],
                                                ['xor', 'x70', 'k70', 'x198', 'dx70'],
                                                ['xor', 'x71', 'k71', 'x199', 'dx71'],
                                                ['xor', 'x72', 'k72', 'x200', 'dx72'],
                                                ['xor', 'x73', 'k73', 'x201', 'dx73'],
                                                ['xor', 'x74', 'k74', 'x202', 'dx74'],
                                                ['xor', 'x75', 'k75', 'x203', 'dx75'],
                                                ['xor', 'x76', 'k76', 'x204', 'dx76'],
                                                ['xor', 'x77', 'k77', 'x205', 'dx77'],
                                                ['xor', 'x78', 'k78', 'x206', 'dx78'],
                                                ['xor', 'x79', 'k79', 'x207', 'dx79'],
                                                ['xor', 'x80', 'k80', 'x208', 'dx80'],
                                                ['xor', 'x81', 'k81', 'x209', 'dx81'],
                                                ['xor', 'x82', 'k82', 'x210', 'dx82'],
                                                ['xor', 'x83', 'k83', 'x211', 'dx83'],
                                                ['xor', 'x84', 'k84', 'x212', 'dx84'],
                                                ['xor', 'x85', 'k85', 'x213', 'dx85'],
                                                ['xor', 'x86', 'k86', 'x214', 'dx86'],
                                                ['xor', 'x87', 'k87', 'x215', 'dx87'],
                                                ['xor', 'x88', 'k88', 'x216', 'dx88'],
                                                ['xor', 'x89', 'k89', 'x217', 'dx89'],
                                                ['xor', 'x90', 'k90', 'x218', 'dx90'],
                                                ['xor', 'x91', 'k91', 'x219', 'dx91'],
                                                ['xor', 'x92', 'k92', 'x220', 'dx92'],
                                                ['xor', 'x93', 'k93', 'x221', 'dx93'],
                                                ['xor', 'x94', 'k94', 'x222', 'dx94'],
                                                ['xor', 'x95', 'k95', 'x223', 'dx95'],
                                                ['xor', 'x96', 'k96', 'x224', 'dx96'],
                                                ['xor', 'x97', 'k97', 'x225', 'dx97'],
                                                ['xor', 'x98', 'k98', 'x226', 'dx98'],
                                                ['xor', 'x99', 'k99', 'x227', 'dx99'],
                                                ['xor', 'x100', 'k100', 'x228', 'dx100'],
                                                ['xor', 'x101', 'k101', 'x229', 'dx101'],
                                                ['xor', 'x102', 'k102', 'x230', 'dx102'],
                                                ['xor', 'x103', 'k103', 'x231', 'dx103'],
                                                ['xor', 'x104', 'k104', 'x232', 'dx104'],
                                                ['xor', 'x105', 'k105', 'x233', 'dx105'],
                                                ['xor', 'x106', 'k106', 'x234', 'dx106'],
                                                ['xor', 'x107', 'k107', 'x235', 'dx107'],
                                                ['xor', 'x108', 'k108', 'x236', 'dx108'],
                                                ['xor', 'x109', 'k109', 'x237', 'dx109'],
                                                ['xor', 'x110', 'k110', 'x238', 'dx110'],
                                                ['xor', 'x111', 'k111', 'x239', 'dx111'],
                                                ['xor', 'x112', 'k112', 'x240', 'dx112'],
                                                ['xor', 'x113', 'k113', 'x241', 'dx113'],
                                                ['xor', 'x114', 'k114', 'x242', 'dx114'],
                                                ['xor', 'x115', 'k115', 'x243', 'dx115'],
                                                ['xor', 'x116', 'k116', 'x244', 'dx116'],
                                                ['xor', 'x117', 'k117', 'x245', 'dx117'],
                                                ['xor', 'x118', 'k118', 'x246', 'dx118'],
                                                ['xor', 'x119', 'k119', 'x247', 'dx119'],
                                                ['xor', 'x120', 'k120', 'x248', 'dx120'],
                                                ['xor', 'x121', 'k121', 'x249', 'dx121'],
                                                ['xor', 'x122', 'k122', 'x250', 'dx122'],
                                                ['xor', 'x123', 'k123', 'x251', 'dx123'],
                                                ['xor', 'x124', 'k124', 'x252', 'dx124'],
                                                ['xor', 'x125', 'k125', 'x253', 'dx125'],
                                                ['xor', 'x126', 'k126', 'x254', 'dx126'],
                                                ['xor', 'x127', 'k127', 'x255', 'dx127']]

        expected_sbox_actions_round_1 = [['sbox', 128, 256, 'a0'], ['sbox', 136, 264, 'a1'], ['sbox', 144, 272, 'a2'],
                                         ['sbox', 152, 280, 'a3'], ['sbox', 160, 288, 'a4'], ['sbox', 168, 296, 'a5'],
                                         ['sbox', 176, 304, 'a6'], ['sbox', 184, 312, 'a7'], ['sbox', 192, 320, 'a8'],
                                         ['sbox', 200, 328, 'a9'], ['sbox', 208, 336, 'a10'], ['sbox', 216, 344, 'a11'],
                                         ['sbox', 224, 352, 'a12'], ['sbox', 232, 360, 'a13'],
                                         ['sbox', 240, 368, 'a14'], ['sbox', 248, 376, 'a15']]

        round_1_A_before_shift_rows = ['x256', 'x257', 'x258', 'x259', 'x260', 'x261', 'x262', 'x263', 'x264', 'x265',
                                       'x266', 'x267', 'x268', 'x269', 'x270', 'x271', 'x272', 'x273', 'x274', 'x275',
                                       'x276', 'x277', 'x278', 'x279', 'x280', 'x281', 'x282', 'x283', 'x284', 'x285',
                                       'x286', 'x287', 'x288', 'x289', 'x290', 'x291', 'x292', 'x293', 'x294', 'x295',
                                       'x296', 'x297', 'x298', 'x299', 'x300', 'x301', 'x302', 'x303', 'x304', 'x305',
                                       'x306', 'x307', 'x308', 'x309', 'x310', 'x311', 'x312', 'x313', 'x314', 'x315',
                                       'x316', 'x317', 'x318', 'x319', 'x320', 'x321', 'x322', 'x323', 'x324', 'x325',
                                       'x326', 'x327', 'x328', 'x329', 'x330', 'x331', 'x332', 'x333', 'x334', 'x335',
                                       'x336', 'x337', 'x338', 'x339', 'x340', 'x341', 'x342', 'x343', 'x344', 'x345',
                                       'x346', 'x347', 'x348', 'x349', 'x350', 'x351', 'x352', 'x353', 'x354', 'x355',
                                       'x356', 'x357', 'x358', 'x359', 'x360', 'x361', 'x362', 'x363', 'x364', 'x365',
                                       'x366', 'x367', 'x368', 'x369', 'x370', 'x371', 'x372', 'x373', 'x374', 'x375',
                                       'x376', 'x377', 'x378', 'x379', 'x380', 'x381', 'x382', 'x383']

        round_1_A_after_shift_rows = ['x256', 'x257', 'x258', 'x259', 'x260', 'x261', 'x262', 'x263', 'x296', 'x297',
                                      'x298', 'x299', 'x300', 'x301', 'x302', 'x303', 'x336', 'x337', 'x338', 'x339',
                                      'x340', 'x341', 'x342', 'x343', 'x376', 'x377', 'x378', 'x379', 'x380', 'x381',
                                      'x382', 'x383', 'x288', 'x289', 'x290', 'x291', 'x292', 'x293', 'x294', 'x295',
                                      'x328', 'x329', 'x330', 'x331', 'x332', 'x333', 'x334', 'x335', 'x368', 'x369',
                                      'x370', 'x371', 'x372', 'x373', 'x374', 'x375', 'x280', 'x281', 'x282', 'x283',
                                      'x284', 'x285', 'x286', 'x287', 'x320', 'x321', 'x322', 'x323', 'x324', 'x325',
                                      'x326', 'x327', 'x360', 'x361', 'x362', 'x363', 'x364', 'x365', 'x366', 'x367',
                                      'x272', 'x273', 'x274', 'x275', 'x276', 'x277', 'x278', 'x279', 'x312', 'x313',
                                      'x314', 'x315', 'x316', 'x317', 'x318', 'x319', 'x352', 'x353', 'x354', 'x355',
                                      'x356', 'x357', 'x358', 'x359', 'x264', 'x265', 'x266', 'x267', 'x268', 'x269',
                                      'x270', 'x271', 'x304', 'x305', 'x306', 'x307', 'x308', 'x309', 'x310', 'x311',
                                      'x344', 'x345', 'x346', 'x347', 'x348', 'x349', 'x350', 'x351']
        expected_mixcolumns_actions_round_1 = [['lin trans',
                                                ['x256', 'x257', 'x258', 'x259', 'x260', 'x261', 'x262', 'x263', 'x296',
                                                 'x297', 'x298', 'x299', 'x300', 'x301', 'x302', 'x303', 'x336', 'x337',
                                                 'x338', 'x339', 'x340', 'x341', 'x342', 'x343', 'x376', 'x377', 'x378',
                                                 'x379', 'x380', 'x381', 'x382', 'x383'],
                                                ['x384', 'x385', 'x386', 'x387', 'x388', 'x389', 'x390', 'x391', 'x392',
                                                 'x393', 'x394', 'x395', 'x396', 'x397', 'x398', 'x399', 'x400', 'x401',
                                                 'x402', 'x403', 'x404', 'x405', 'x406', 'x407', 'x408', 'x409', 'x410',
                                                 'x411', 'x412', 'x413', 'x414', 'x415'],
                                                'dl0'],
                                               ['lin trans',
                                                ['x288', 'x289', 'x290', 'x291', 'x292', 'x293', 'x294', 'x295', 'x328',
                                                 'x329', 'x330', 'x331', 'x332', 'x333', 'x334', 'x335', 'x368', 'x369',
                                                 'x370', 'x371', 'x372', 'x373', 'x374', 'x375', 'x280', 'x281', 'x282',
                                                 'x283', 'x284', 'x285', 'x286', 'x287'],
                                                ['x416', 'x417', 'x418', 'x419', 'x420', 'x421', 'x422', 'x423', 'x424',
                                                 'x425', 'x426', 'x427', 'x428', 'x429', 'x430', 'x431', 'x432', 'x433',
                                                 'x434', 'x435', 'x436', 'x437', 'x438', 'x439', 'x440', 'x441', 'x442',
                                                 'x443', 'x444', 'x445', 'x446', 'x447'],
                                                'dl1'],
                                               ['lin trans',
                                                ['x320', 'x321', 'x322', 'x323', 'x324', 'x325', 'x326', 'x327', 'x360',
                                                 'x361', 'x362', 'x363', 'x364', 'x365', 'x366', 'x367', 'x272', 'x273',
                                                 'x274', 'x275', 'x276', 'x277', 'x278', 'x279', 'x312', 'x313', 'x314',
                                                 'x315', 'x316', 'x317', 'x318', 'x319'],
                                                ['x448', 'x449', 'x450', 'x451', 'x452', 'x453', 'x454', 'x455', 'x456',
                                                 'x457', 'x458', 'x459', 'x460', 'x461', 'x462', 'x463', 'x464', 'x465',
                                                 'x466', 'x467', 'x468', 'x469', 'x470', 'x471', 'x472', 'x473', 'x474',
                                                 'x475', 'x476', 'x477', 'x478', 'x479'],
                                                'dl2'],
                                               ['lin trans',
                                                ['x352', 'x353', 'x354', 'x355', 'x356', 'x357', 'x358', 'x359', 'x264',
                                                 'x265', 'x266', 'x267', 'x268', 'x269', 'x270', 'x271', 'x304', 'x305',
                                                 'x306', 'x307', 'x308', 'x309', 'x310', 'x311', 'x344', 'x345', 'x346',
                                                 'x347', 'x348', 'x349', 'x350', 'x351'],
                                                ['x480', 'x481', 'x482', 'x483', 'x484', 'x485', 'x486', 'x487', 'x488',
                                                 'x489', 'x490', 'x491', 'x492', 'x493', 'x494', 'x495', 'x496', 'x497',
                                                 'x498', 'x499', 'x500', 'x501', 'x502', 'x503', 'x504', 'x505', 'x506',
                                                 'x507', 'x508', 'x509', 'x510', 'x511'],
                                                'dl3']
                                               ]

        expected_key_xor_actions_round_1 = [['xor', 'x384', 'k128', 'x512', 'dx128'],
                                            ['xor', 'x385', 'k129', 'x513', 'dx129'],
                                            ['xor', 'x386', 'k130', 'x514', 'dx130'],
                                            ['xor', 'x387', 'k131', 'x515', 'dx131'],
                                            ['xor', 'x388', 'k132', 'x516', 'dx132'],
                                            ['xor', 'x389', 'k133', 'x517', 'dx133'],
                                            ['xor', 'x390', 'k134', 'x518', 'dx134'],
                                            ['xor', 'x391', 'k135', 'x519', 'dx135'],
                                            ['xor', 'x392', 'k136', 'x520', 'dx136'],
                                            ['xor', 'x393', 'k137', 'x521', 'dx137'],
                                            ['xor', 'x394', 'k138', 'x522', 'dx138'],
                                            ['xor', 'x395', 'k139', 'x523', 'dx139'],
                                            ['xor', 'x396', 'k140', 'x524', 'dx140'],
                                            ['xor', 'x397', 'k141', 'x525', 'dx141'],
                                            ['xor', 'x398', 'k142', 'x526', 'dx142'],
                                            ['xor', 'x399', 'k143', 'x527', 'dx143'],
                                            ['xor', 'x400', 'k144', 'x528', 'dx144'],
                                            ['xor', 'x401', 'k145', 'x529', 'dx145'],
                                            ['xor', 'x402', 'k146', 'x530', 'dx146'],
                                            ['xor', 'x403', 'k147', 'x531', 'dx147'],
                                            ['xor', 'x404', 'k148', 'x532', 'dx148'],
                                            ['xor', 'x405', 'k149', 'x533', 'dx149'],
                                            ['xor', 'x406', 'k150', 'x534', 'dx150'],
                                            ['xor', 'x407', 'k151', 'x535', 'dx151'],
                                            ['xor', 'x408', 'k152', 'x536', 'dx152'],
                                            ['xor', 'x409', 'k153', 'x537', 'dx153'],
                                            ['xor', 'x410', 'k154', 'x538', 'dx154'],
                                            ['xor', 'x411', 'k155', 'x539', 'dx155'],
                                            ['xor', 'x412', 'k156', 'x540', 'dx156'],
                                            ['xor', 'x413', 'k157', 'x541', 'dx157'],
                                            ['xor', 'x414', 'k158', 'x542', 'dx158'],
                                            ['xor', 'x415', 'k159', 'x543', 'dx159'],
                                            ['xor', 'x416', 'k160', 'x544', 'dx160'],
                                            ['xor', 'x417', 'k161', 'x545', 'dx161'],
                                            ['xor', 'x418', 'k162', 'x546', 'dx162'],
                                            ['xor', 'x419', 'k163', 'x547', 'dx163'],
                                            ['xor', 'x420', 'k164', 'x548', 'dx164'],
                                            ['xor', 'x421', 'k165', 'x549', 'dx165'],
                                            ['xor', 'x422', 'k166', 'x550', 'dx166'],
                                            ['xor', 'x423', 'k167', 'x551', 'dx167'],
                                            ['xor', 'x424', 'k168', 'x552', 'dx168'],
                                            ['xor', 'x425', 'k169', 'x553', 'dx169'],
                                            ['xor', 'x426', 'k170', 'x554', 'dx170'],
                                            ['xor', 'x427', 'k171', 'x555', 'dx171'],
                                            ['xor', 'x428', 'k172', 'x556', 'dx172'],
                                            ['xor', 'x429', 'k173', 'x557', 'dx173'],
                                            ['xor', 'x430', 'k174', 'x558', 'dx174'],
                                            ['xor', 'x431', 'k175', 'x559', 'dx175'],
                                            ['xor', 'x432', 'k176', 'x560', 'dx176'],
                                            ['xor', 'x433', 'k177', 'x561', 'dx177'],
                                            ['xor', 'x434', 'k178', 'x562', 'dx178'],
                                            ['xor', 'x435', 'k179', 'x563', 'dx179'],
                                            ['xor', 'x436', 'k180', 'x564', 'dx180'],
                                            ['xor', 'x437', 'k181', 'x565', 'dx181'],
                                            ['xor', 'x438', 'k182', 'x566', 'dx182'],
                                            ['xor', 'x439', 'k183', 'x567', 'dx183'],
                                            ['xor', 'x440', 'k184', 'x568', 'dx184'],
                                            ['xor', 'x441', 'k185', 'x569', 'dx185'],
                                            ['xor', 'x442', 'k186', 'x570', 'dx186'],
                                            ['xor', 'x443', 'k187', 'x571', 'dx187'],
                                            ['xor', 'x444', 'k188', 'x572', 'dx188'],
                                            ['xor', 'x445', 'k189', 'x573', 'dx189'],
                                            ['xor', 'x446', 'k190', 'x574', 'dx190'],
                                            ['xor', 'x447', 'k191', 'x575', 'dx191'],
                                            ['xor', 'x448', 'k192', 'x576', 'dx192'],
                                            ['xor', 'x449', 'k193', 'x577', 'dx193'],
                                            ['xor', 'x450', 'k194', 'x578', 'dx194'],
                                            ['xor', 'x451', 'k195', 'x579', 'dx195'],
                                            ['xor', 'x452', 'k196', 'x580', 'dx196'],
                                            ['xor', 'x453', 'k197', 'x581', 'dx197'],
                                            ['xor', 'x454', 'k198', 'x582', 'dx198'],
                                            ['xor', 'x455', 'k199', 'x583', 'dx199'],
                                            ['xor', 'x456', 'k200', 'x584', 'dx200'],
                                            ['xor', 'x457', 'k201', 'x585', 'dx201'],
                                            ['xor', 'x458', 'k202', 'x586', 'dx202'],
                                            ['xor', 'x459', 'k203', 'x587', 'dx203'],
                                            ['xor', 'x460', 'k204', 'x588', 'dx204'],
                                            ['xor', 'x461', 'k205', 'x589', 'dx205'],
                                            ['xor', 'x462', 'k206', 'x590', 'dx206'],
                                            ['xor', 'x463', 'k207', 'x591', 'dx207'],
                                            ['xor', 'x464', 'k208', 'x592', 'dx208'],
                                            ['xor', 'x465', 'k209', 'x593', 'dx209'],
                                            ['xor', 'x466', 'k210', 'x594', 'dx210'],
                                            ['xor', 'x467', 'k211', 'x595', 'dx211'],
                                            ['xor', 'x468', 'k212', 'x596', 'dx212'],
                                            ['xor', 'x469', 'k213', 'x597', 'dx213'],
                                            ['xor', 'x470', 'k214', 'x598', 'dx214'],
                                            ['xor', 'x471', 'k215', 'x599', 'dx215'],
                                            ['xor', 'x472', 'k216', 'x600', 'dx216'],
                                            ['xor', 'x473', 'k217', 'x601', 'dx217'],
                                            ['xor', 'x474', 'k218', 'x602', 'dx218'],
                                            ['xor', 'x475', 'k219', 'x603', 'dx219'],
                                            ['xor', 'x476', 'k220', 'x604', 'dx220'],
                                            ['xor', 'x477', 'k221', 'x605', 'dx221'],
                                            ['xor', 'x478', 'k222', 'x606', 'dx222'],
                                            ['xor', 'x479', 'k223', 'x607', 'dx223'],
                                            ['xor', 'x480', 'k224', 'x608', 'dx224'],
                                            ['xor', 'x481', 'k225', 'x609', 'dx225'],
                                            ['xor', 'x482', 'k226', 'x610', 'dx226'],
                                            ['xor', 'x483', 'k227', 'x611', 'dx227'],
                                            ['xor', 'x484', 'k228', 'x612', 'dx228'],
                                            ['xor', 'x485', 'k229', 'x613', 'dx229'],
                                            ['xor', 'x486', 'k230', 'x614', 'dx230'],
                                            ['xor', 'x487', 'k231', 'x615', 'dx231'],
                                            ['xor', 'x488', 'k232', 'x616', 'dx232'],
                                            ['xor', 'x489', 'k233', 'x617', 'dx233'],
                                            ['xor', 'x490', 'k234', 'x618', 'dx234'],
                                            ['xor', 'x491', 'k235', 'x619', 'dx235'],
                                            ['xor', 'x492', 'k236', 'x620', 'dx236'],
                                            ['xor', 'x493', 'k237', 'x621', 'dx237'],
                                            ['xor', 'x494', 'k238', 'x622', 'dx238'],
                                            ['xor', 'x495', 'k239', 'x623', 'dx239'],
                                            ['xor', 'x496', 'k240', 'x624', 'dx240'],
                                            ['xor', 'x497', 'k241', 'x625', 'dx241'],
                                            ['xor', 'x498', 'k242', 'x626', 'dx242'],
                                            ['xor', 'x499', 'k243', 'x627', 'dx243'],
                                            ['xor', 'x500', 'k244', 'x628', 'dx244'],
                                            ['xor', 'x501', 'k245', 'x629', 'dx245'],
                                            ['xor', 'x502', 'k246', 'x630', 'dx246'],
                                            ['xor', 'x503', 'k247', 'x631', 'dx247'],
                                            ['xor', 'x504', 'k248', 'x632', 'dx248'],
                                            ['xor', 'x505', 'k249', 'x633', 'dx249'],
                                            ['xor', 'x506', 'k250', 'x634', 'dx250'],
                                            ['xor', 'x507', 'k251', 'x635', 'dx251'],
                                            ['xor', 'x508', 'k252', 'x636', 'dx252'],
                                            ['xor', 'x509', 'k253', 'x637', 'dx253'],
                                            ['xor', 'x510', 'k254', 'x638', 'dx254'],
                                            ['xor', 'x511', 'k255', 'x639', 'dx255']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_1, round_1_A_before_shift_rows,
                                            round_1_A_after_shift_rows, expected_mixcolumns_actions_round_1,
                                            expected_key_xor_actions_round_1, expected_key_xor_actions_pre_round_1)
        return

    def test_round_progression_word_oriented(self):
        cipher_instance = Aes(rounds=4, model_as_bit_oriented=False)

        bits_before_round_1 = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
                               'x14', 'x15']
        self.assertEqual(cipher_instance.A, bits_before_round_1)

        cipher_instance.run_round()

        bits_before_round_2 = ['x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59',
                               'x60', 'x61', 'x62', 'x63']

        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.run_round()

        bits_before_round_3 = ['x80', 'x81', 'x82', 'x83', 'x84', 'x85', 'x86', 'x87', 'x88', 'x89', 'x90', 'x91',
                               'x92', 'x93', 'x94', 'x95']

        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return

    def test_correct_actions_performed_round_1_word_oriented(self):
        cipher_instance = Aes(rounds=4, model_as_bit_oriented=False)

        expected_key_xor_actions_pre_round_1 = [['xor', 'x0', 'k0', 'x16', 'dx0'], ['xor', 'x1', 'k1', 'x17', 'dx1'],
                                                ['xor', 'x2', 'k2', 'x18', 'dx2'], ['xor', 'x3', 'k3', 'x19', 'dx3'],
                                                ['xor', 'x4', 'k4', 'x20', 'dx4'], ['xor', 'x5', 'k5', 'x21', 'dx5'],
                                                ['xor', 'x6', 'k6', 'x22', 'dx6'], ['xor', 'x7', 'k7', 'x23', 'dx7'],
                                                ['xor', 'x8', 'k8', 'x24', 'dx8'], ['xor', 'x9', 'k9', 'x25', 'dx9'],
                                                ['xor', 'x10', 'k10', 'x26', 'dx10'],
                                                ['xor', 'x11', 'k11', 'x27', 'dx11'],
                                                ['xor', 'x12', 'k12', 'x28', 'dx12'],
                                                ['xor', 'x13', 'k13', 'x29', 'dx13'],
                                                ['xor', 'x14', 'k14', 'x30', 'dx14'],
                                                ['xor', 'x15', 'k15', 'x31', 'dx15']]

        expected_sbox_actions_round_1 = list()

        round_1_A_before_shift_rows = ['x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26',
                                       'x27', 'x28', 'x29', 'x30', 'x31']

        round_1_A_after_shift_rows = ['x16', 'x21', 'x26', 'x31', 'x20', 'x25', 'x30', 'x19', 'x24', 'x29', 'x18',
                                      'x23', 'x28', 'x17', 'x22', 'x27']
        expected_mixcolumns_actions_round_1 = [
            ['lin trans', ['x16', 'x21', 'x26', 'x31'], ['x32', 'x33', 'x34', 'x35'], 'dl0'],
            ['lin trans', ['x20', 'x25', 'x30', 'x19'], ['x36', 'x37', 'x38', 'x39'], 'dl1'],
            ['lin trans', ['x24', 'x29', 'x18', 'x23'], ['x40', 'x41', 'x42', 'x43'], 'dl2'],
            ['lin trans', ['x28', 'x17', 'x22', 'x27'], ['x44', 'x45', 'x46', 'x47'], 'dl3']]

        expected_key_xor_actions_round_1 = [['xor', 'x32', 'k16', 'x48', 'dx16'], ['xor', 'x33', 'k17', 'x49', 'dx17'],
                                            ['xor', 'x34', 'k18', 'x50', 'dx18'], ['xor', 'x35', 'k19', 'x51', 'dx19'],
                                            ['xor', 'x36', 'k20', 'x52', 'dx20'], ['xor', 'x37', 'k21', 'x53', 'dx21'],
                                            ['xor', 'x38', 'k22', 'x54', 'dx22'], ['xor', 'x39', 'k23', 'x55', 'dx23'],
                                            ['xor', 'x40', 'k24', 'x56', 'dx24'], ['xor', 'x41', 'k25', 'x57', 'dx25'],
                                            ['xor', 'x42', 'k26', 'x58', 'dx26'], ['xor', 'x43', 'k27', 'x59', 'dx27'],
                                            ['xor', 'x44', 'k28', 'x60', 'dx28'], ['xor', 'x45', 'k29', 'x61', 'dx29'],
                                            ['xor', 'x46', 'k30', 'x62', 'dx30'], ['xor', 'x47', 'k31', 'x63', 'dx31']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_1, round_1_A_before_shift_rows,
                                            round_1_A_after_shift_rows, expected_mixcolumns_actions_round_1,
                                            expected_key_xor_actions_round_1, expected_key_xor_actions_pre_round_1)
        return

    def test_correct_actions_performed_round_2_word_oriented(self):
        cipher_instance = Aes(rounds=4, model_as_bit_oriented=False)

        cipher_instance.run_round()

        expected_key_xor_actions_pre_round_2 = None

        expected_sbox_actions_round_2 = list()

        round_2_A_before_shift_rows = ['x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58',
                                       'x59', 'x60', 'x61', 'x62', 'x63']

        round_2_A_after_shift_rows = ['x48', 'x53', 'x58', 'x63', 'x52', 'x57', 'x62', 'x51', 'x56', 'x61', 'x50',
                                      'x55', 'x60', 'x49', 'x54', 'x59']

        expected_mixcolumns_actions_round_2 = [
            ['lin trans', ['x48', 'x53', 'x58', 'x63'], ['x64', 'x65', 'x66', 'x67'], 'dl4'],
            ['lin trans', ['x52', 'x57', 'x62', 'x51'], ['x68', 'x69', 'x70', 'x71'], 'dl5'],
            ['lin trans', ['x56', 'x61', 'x50', 'x55'], ['x72', 'x73', 'x74', 'x75'], 'dl6'],
            ['lin trans', ['x60', 'x49', 'x54', 'x59'], ['x76', 'x77', 'x78', 'x79'], 'dl7']]

        expected_key_xor_actions_round_2 = [['xor', 'x64', 'k32', 'x80', 'dx32'], ['xor', 'x65', 'k33', 'x81', 'dx33'],
                                            ['xor', 'x66', 'k34', 'x82', 'dx34'], ['xor', 'x67', 'k35', 'x83', 'dx35'],
                                            ['xor', 'x68', 'k36', 'x84', 'dx36'], ['xor', 'x69', 'k37', 'x85', 'dx37'],
                                            ['xor', 'x70', 'k38', 'x86', 'dx38'], ['xor', 'x71', 'k39', 'x87', 'dx39'],
                                            ['xor', 'x72', 'k40', 'x88', 'dx40'], ['xor', 'x73', 'k41', 'x89', 'dx41'],
                                            ['xor', 'x74', 'k42', 'x90', 'dx42'], ['xor', 'x75', 'k43', 'x91', 'dx43'],
                                            ['xor', 'x76', 'k44', 'x92', 'dx44'], ['xor', 'x77', 'k45', 'x93', 'dx45'],
                                            ['xor', 'x78', 'k46', 'x94', 'dx46'], ['xor', 'x79', 'k47', 'x95', 'dx47']]

        self.round_testing_given_parameters(cipher_instance, expected_sbox_actions_round_2, round_2_A_before_shift_rows,
                                            round_2_A_after_shift_rows, expected_mixcolumns_actions_round_2,
                                            expected_key_xor_actions_round_2, expected_key_xor_actions_pre_round_2)
        return


if __name__ == '__main__':
    unittest.main()
