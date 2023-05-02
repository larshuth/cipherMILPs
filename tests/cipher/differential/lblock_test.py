import unittest
from cipher.differential.lblock import LBlock
from cipher.actions import SBoxAction, XorAction, PermutationAction, OverwriteAction


class LBlockTest(unittest.TestCase):
    def test_init_bit_oriented(self):
        cipher_instance = LBlock(model_as_bit_oriented=True)
        bits_before_round_1 = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13',
                               'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25',
                               'x26', 'x27', 'x28', 'x29', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37',
                               'x38', 'x39', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49',
                               'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x60', 'x61',
                               'x62', 'x63']
        self.assertEqual(cipher_instance.A, bits_before_round_1)
        return

    def test_round_progression_bit_oriented(self):
        cipher_instance = LBlock(rounds=4, model_as_bit_oriented=True)

        actions = list()
        # copy pasted from the lblock.py file
        actions += cipher_instance.generate_key_xor_actions_for_round()
        for key_xor_action in cipher_instance.generate_key_xor_actions_for_round():
            key_xor_action.run_action()

        actions += cipher_instance.generate_sbox_actions_for_round()
        for sbox_action in cipher_instance.generate_sbox_actions_for_round():
            sbox_action.run_action()

        actions += cipher_instance.generate_permutation_after_sbox_actions_for_round()
        for permutation_action in cipher_instance.generate_permutation_after_sbox_actions_for_round():
            permutation_action.run_action()

        actions += cipher_instance.generate_bitshift_actions_for_round()
        for bitshift in cipher_instance.generate_bitshift_actions_for_round():
            bitshift.run_action()

        actions += cipher_instance.generate_f_output_right_plaintext_xor_actions_for_round()
        for xor_action in cipher_instance.generate_f_output_right_plaintext_xor_actions_for_round():
            xor_action.run_action()


        events_round_1 = [['xor', 'x0', 'k0', 'x64', 'd0'], ['xor', 'x1', 'k1', 'x65', 'd1'],
                          ['xor', 'x2', 'k2', 'x66', 'd2'], ['xor', 'x3', 'k3', 'x67', 'd3'],
                          ['xor', 'x4', 'k4', 'x68', 'd4'], ['xor', 'x5', 'k5', 'x69', 'd5'],
                          ['xor', 'x6', 'k6', 'x70', 'd6'], ['xor', 'x7', 'k7', 'x71', 'd7'],
                          ['xor', 'x8', 'k8', 'x72', 'd8'], ['xor', 'x9', 'k9', 'x73', 'd9'],
                          ['xor', 'x10', 'k10', 'x74', 'd10'], ['xor', 'x11', 'k11', 'x75', 'd11'],
                          ['xor', 'x12', 'k12', 'x76', 'd12'], ['xor', 'x13', 'k13', 'x77', 'd13'],
                          ['xor', 'x14', 'k14', 'x78', 'd14'], ['xor', 'x15', 'k15', 'x79', 'd15'],
                          ['xor', 'x16', 'k16', 'x80', 'd16'], ['xor', 'x17', 'k17', 'x81', 'd17'],
                          ['xor', 'x18', 'k18', 'x82', 'd18'], ['xor', 'x19', 'k19', 'x83', 'd19'],
                          ['xor', 'x20', 'k20', 'x84', 'd20'], ['xor', 'x21', 'k21', 'x85', 'd21'],
                          ['xor', 'x22', 'k22', 'x86', 'd22'], ['xor', 'x23', 'k23', 'x87', 'd23'],
                          ['xor', 'x24', 'k24', 'x88', 'd24'], ['xor', 'x25', 'k25', 'x89', 'd25'],
                          ['xor', 'x26', 'k26', 'x90', 'd26'], ['xor', 'x27', 'k27', 'x91', 'd27'],
                          ['xor', 'x28', 'k28', 'x92', 'd28'], ['xor', 'x29', 'k29', 'x93', 'd29'],
                          ['xor', 'x30', 'k30', 'x94', 'd30'], ['xor', 'x31', 'k31', 'x95', 'd31'],
                          ['sbox', 64, 96, 'a0'], ['sbox', 68, 100, 'a1'], ['sbox', 72, 104, 'a2'],
                          ['sbox', 76, 108, 'a3'], ['sbox', 80, 112, 'a4'], ['sbox', 84, 116, 'a5'],
                          ['sbox', 88, 120, 'a6'], ['sbox', 92, 124, 'a7'],
                          ['xor', 'x100', 'x32', 'x128', 'd32'], ['xor', 'x101', 'x33', 'x129', 'd33'],
                          ['xor', 'x102', 'x34', 'x130', 'd34'], ['xor', 'x103', 'x35', 'x131', 'd35'],
                          ['xor', 'x108', 'x36', 'x132', 'd36'], ['xor', 'x109', 'x37', 'x133', 'd37'],
                          ['xor', 'x110', 'x38', 'x134', 'd38'], ['xor', 'x111', 'x39', 'x135', 'd39'],
                          ['xor', 'x96', 'x40', 'x136', 'd40'], ['xor', 'x97', 'x41', 'x137', 'd41'],
                          ['xor', 'x98', 'x42', 'x138', 'd42'], ['xor', 'x99', 'x43', 'x139', 'd43'],
                          ['xor', 'x104', 'x44', 'x140', 'd44'], ['xor', 'x105', 'x45', 'x141', 'd45'],
                          ['xor', 'x106', 'x46', 'x142', 'd46'], ['xor', 'x107', 'x47', 'x143', 'd47'],
                          ['xor', 'x116', 'x48', 'x144', 'd48'], ['xor', 'x117', 'x49', 'x145', 'd49'],
                          ['xor', 'x118', 'x50', 'x146', 'd50'], ['xor', 'x119', 'x51', 'x147', 'd51'],
                          ['xor', 'x124', 'x52', 'x148', 'd52'], ['xor', 'x125', 'x53', 'x149', 'd53'],
                          ['xor', 'x126', 'x54', 'x150', 'd54'], ['xor', 'x127', 'x55', 'x151', 'd55'],
                          ['xor', 'x112', 'x56', 'x152', 'd56'], ['xor', 'x113', 'x57', 'x153', 'd57'],
                          ['xor', 'x114', 'x58', 'x154', 'd58'], ['xor', 'x115', 'x59', 'x155', 'd59'],
                          ['xor', 'x120', 'x60', 'x156', 'd60'], ['xor', 'x121', 'x61', 'x157', 'd61'],
                          ['xor', 'x122', 'x62', 'x158', 'd62'], ['xor', 'x123', 'x63', 'x159', 'd63']]

        expected_actions = list()
        for action in events_round_1:
            if action[0] == "xor":
                if int(action[1][1:])
                expected_actions.append(XorAction((action[1], action[2]), cipher_instance))

        filtered_actions = [[a[0]] + a[2:] if a[0] == 'sbox' else a for a in actions]    # filtering out sbox instances
        self.assertEqual(events_round_1, filtered_actions)

        line = 0
        for action in actions:
            line = cipher_instance.gen_long_constraint(line, action)
        cipher_instance.shift_after()

        bits_before_round_2 = ['x128', 'x129', 'x130', 'x131', 'x132', 'x133', 'x134', 'x135', 'x136', 'x137', 'x138',
                               'x139', 'x140', 'x141', 'x142', 'x143', 'x144', 'x145', 'x146', 'x147', 'x148', 'x149',
                               'x150', 'x151', 'x152', 'x153', 'x154', 'x155', 'x156', 'x157', 'x158', 'x159', 'x0',
                               'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14',
                               'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26',
                               'x27', 'x28', 'x29', 'x30', 'x31']
        self.assertEqual(bits_before_round_2, cipher_instance.A)

        cipher_instance.shift_before()
        actions = cipher_instance.rangenumber()
        events_round_2 = [['xor', 'x128', 'k32', 'x160', 'd64'], ['xor', 'x129', 'k33', 'x161', 'd65'],
                          ['xor', 'x130', 'k34', 'x162', 'd66'], ['xor', 'x131', 'k35', 'x163', 'd67'],
                          ['xor', 'x132', 'k36', 'x164', 'd68'], ['xor', 'x133', 'k37', 'x165', 'd69'],
                          ['xor', 'x134', 'k38', 'x166', 'd70'], ['xor', 'x135', 'k39', 'x167', 'd71'],
                          ['xor', 'x136', 'k40', 'x168', 'd72'], ['xor', 'x137', 'k41', 'x169', 'd73'],
                          ['xor', 'x138', 'k42', 'x170', 'd74'], ['xor', 'x139', 'k43', 'x171', 'd75'],
                          ['xor', 'x140', 'k44', 'x172', 'd76'], ['xor', 'x141', 'k45', 'x173', 'd77'],
                          ['xor', 'x142', 'k46', 'x174', 'd78'], ['xor', 'x143', 'k47', 'x175', 'd79'],
                          ['xor', 'x144', 'k48', 'x176', 'd80'], ['xor', 'x145', 'k49', 'x177', 'd81'],
                          ['xor', 'x146', 'k50', 'x178', 'd82'], ['xor', 'x147', 'k51', 'x179', 'd83'],
                          ['xor', 'x148', 'k52', 'x180', 'd84'], ['xor', 'x149', 'k53', 'x181', 'd85'],
                          ['xor', 'x150', 'k54', 'x182', 'd86'], ['xor', 'x151', 'k55', 'x183', 'd87'],
                          ['xor', 'x152', 'k56', 'x184', 'd88'], ['xor', 'x153', 'k57', 'x185', 'd89'],
                          ['xor', 'x154', 'k58', 'x186', 'd90'], ['xor', 'x155', 'k59', 'x187', 'd91'],
                          ['xor', 'x156', 'k60', 'x188', 'd92'], ['xor', 'x157', 'k61', 'x189', 'd93'],
                          ['xor', 'x158', 'k62', 'x190', 'd94'], ['xor', 'x159', 'k63', 'x191', 'd95'],
                          ['sbox', 160, 192, 'a8'], ['sbox', 164, 196, 'a9'], ['sbox', 168, 200, 'a10'],
                          ['sbox', 172, 204, 'a11'], ['sbox', 176, 208, 'a12'], ['sbox', 180, 212, 'a13'],
                          ['sbox', 184, 216, 'a14'], ['sbox', 188, 220, 'a15'],
                          ['xor', 'x196', 'x32', 'x128', 'd96'], ['xor', 'x197', 'x33', 'x129', 'd97'],
                          ['xor', 'x198', 'x34', 'x130', 'd98'], ['xor', 'x199', 'x35', 'x131', 'd99'],
                          ['xor', 'x204', 'x36', 'x132', 'd100'], ['xor', 'x205', 'x37', 'x133', 'd101'],
                          ['xor', 'x206', 'x38', 'x134', 'd102'], ['xor', 'x207', 'x39', 'x135', 'd103'],
                          ['xor', 'x192', 'x40', 'x136', 'd104'], ['xor', 'x193', 'x41', 'x137', 'd105'],
                          ['xor', 'x194', 'x42', 'x138', 'd106'], ['xor', 'x195', 'x43', 'x139', 'd107'],
                          ['xor', 'x200', 'x44', 'x140', 'd108'], ['xor', 'x201', 'x45', 'x141', 'd109'],
                          ['xor', 'x202', 'x46', 'x142', 'd110'], ['xor', 'x203', 'x47', 'x143', 'd111'],
                          ['xor', 'x212', 'x48', 'x144', 'd112'], ['xor', 'x213', 'x49', 'x145', 'd113'],
                          ['xor', 'x214', 'x50', 'x146', 'd114'], ['xor', 'x215', 'x51', 'x147', 'd115'],
                          ['xor', 'x220', 'x52', 'x148', 'd116'], ['xor', 'x221', 'x53', 'x149', 'd117'],
                          ['xor', 'x222', 'x54', 'x150', 'd118'], ['xor', 'x223', 'x55', 'x151', 'd119'],
                          ['xor', 'x208', 'x56', 'x152', 'd120'], ['xor', 'x209', 'x57', 'x153', 'd121'],
                          ['xor', 'x210', 'x58', 'x154', 'd122'], ['xor', 'x211', 'x59', 'x155', 'd123'],
                          ['xor', 'x216', 'x60', 'x156', 'd124'], ['xor', 'x217', 'x61', 'x157', 'd125'],
                          ['xor', 'x218', 'x62', 'x158', 'd126'], ['xor', 'x219', 'x63', 'x159', 'd127']]

        filtered_actions = [[a[0]] + a[2:] if a[0] == 'sbox' else a for a in actions]  # filtering out sbox instances
        self.assertEqual(events_round_2, filtered_actions)

        line = 0
        for action in actions:
            line = cipher_instance.gen_long_constraint(line, action)
        cipher_instance.shift_after()

        bits_before_round_3 = ['x224', 'x225', 'x226', 'x227', 'x228', 'x229', 'x230', 'x231', 'x232', 'x233', 'x234',
                               'x235', 'x236', 'x237', 'x238', 'x239', 'x240', 'x241', 'x242', 'x243', 'x244', 'x245',
                               'x246', 'x247', 'x248', 'x249', 'x250', 'x251', 'x252', 'x253', 'x254', 'x255',
                               'x128', 'x129', 'x130', 'x131', 'x132', 'x133', 'x134', 'x135', 'x136', 'x137', 'x138',
                               'x139', 'x140', 'x141', 'x142', 'x143', 'x144', 'x145', 'x146', 'x147', 'x148', 'x149',
                               'x150', 'x151', 'x152', 'x153', 'x154', 'x155', 'x156', 'x157', 'x158', 'x159']
        self.assertEqual(bits_before_round_3, cipher_instance.A)
        return


if __name__ == '__main__':
    unittest.main()
