from cipher.cipher import Cipher
from cipher.sbox import SBox
from cipher.actions.permutationaction import PermutationAction
from cipher.actions.xoraction import XorAction
from cipher.actions.sboxaction import SBoxAction


class LBlock(Cipher):
    """
    Class in which all functions for LBlock cipher [Wu et al 2011] are defined.
    """

    def get_permutation(self, extra_shift=0):
        permutation = list()
        block_size = int(4 / self.orientation)
        for index, shift in enumerate([+1, +2, -2, -1, +1, +2, -2, -1]):
            permutation += [(index + shift) * block_size + i + extra_shift for i in range(block_size)]
        return permutation

    def generate_key_xor_actions_for_round(self):
        list_of_key_xor_actions = list()
        start_first_half = 0
        end_first_half = int((self.plaintextsize / 2) / self.orientation)

        for i in range(start_first_half, end_first_half):
            list_of_key_xor_actions.append(XorAction(inputs=(self.A[i], self.K[i]),
                                                     cipher_instance=self, a_position_to_overwrite=i))
        return list_of_key_xor_actions

    def generate_sbox_actions_for_round(self):
        list_of_sbox_actions = list()
        if self.orientation == 1:
            for i in range(8):
                sbox_input_vars = [self.A[4 * i + var] for var in range(self.sboxes[i].in_bits)]
                list_of_sbox_actions.append(SBoxAction(sbox=self.sboxes[i], input_vars=sbox_input_vars,
                                                       cipher_instance=self,
                                                       first_a_position_to_overwrite=4 * i))
        else:
            pass
        return list_of_sbox_actions

    def generate_permutation_after_sbox_actions_for_round(self):
        list_of_permutation_actions = list()
        permutation = self.get_permutation()
        # this shifts the elements in self.A such that [0,1,2,3,4,5,6,7,8,9 ...] becomes [4,5,6,7,12,13,14,15,0,1 ...]

        start_second_half = int((self.plaintextsize / 2) / self.orientation)
        end_second_half = int(self.plaintextsize / self.orientation)
        permutation += list(range(start_second_half, end_second_half))
        # permutation needs to span the whole A list, even if not all of them are changed
        list_of_permutation_actions.append(PermutationAction(permutation, self))
        return list_of_permutation_actions

    def generate_bitshift_actions_for_round(self):
        list_of_bitshift_actions = list()
        start_first_half = 0
        end_first_half = int((self.plaintextsize / 2) / self.orientation)
        permutation = list()
        permutation += list(range(start_first_half, end_first_half))
        # permutation needs to span the whole A list, even if not all of them are changed
        # using the previously written code if just due to laziness
        block_size = int(4 / self.orientation)
        for index, shift in enumerate([+2] * 8):
            permutation += [end_first_half + ((i + (2 * block_size)) % end_first_half) for i in range(end_first_half)]
        # this shifts the elements in self.A such that [0,1,2,3,4,5,6,7 ...] becomes [8,9,10,11,12,13,14,15 ...]
        list_of_bitshift_actions.append(PermutationAction(permutation, self))
        return list_of_bitshift_actions

    def generate_f_output_right_plaintext_xor_actions_for_round(self):
        f_output_right_plaintext_xor_actions_list = list()
        half_length = int(32 / self.orientation)
        f_output_right_plaintext_xor_actions_list += [XorAction(inputs=(self.A[i], self.A[i + half_length]),
                                                                cipher_instance=self,
                                                                a_position_to_overwrite=(i + half_length))
                                                      for i in range(half_length)]
        return f_output_right_plaintext_xor_actions_list

    def run_round(self):
        x1_size = int((self.plaintextsize / 2) / self.orientation)
        x1_backup = self.A[:x1_size].copy()

        for key_xor_action in self.generate_key_xor_actions_for_round():
            key_xor_action.run_action()
        print(self.A)
        for sbox_action in self.generate_sbox_actions_for_round():
            sbox_action.run_action()
        print(self.A)
        for permutation_action in self.generate_permutation_after_sbox_actions_for_round():
            permutation_action.run_action()
        print(self.A)

        for bitshift in self.generate_bitshift_actions_for_round():
            bitshift.run_action()
        print(self.A)
        for xor_action in self.generate_f_output_right_plaintext_xor_actions_for_round():
            xor_action.run_action()
        print(self.A)

        # renew the elements s.t. the first half of A, X_1 in the og paper,
        self.A[:x1_size] = x1_backup

        # and switch left and right
        self.A = self.A[x1_size:] + self.A[:x1_size]
        print(self.A)

        # this is actually not the size of the key but the array representing the subkey in each round
        self.K = ['k' + str(self.round_number * self.key_vars + i) for i in range(self.key_vars)]
        self.round_number += 1
        return True

    def __init__(self, rounds=32, model_as_bit_oriented=True, cryptanalysis_type="differential",
                 type_of_modeling='SunEtAl 2013', **kwargs):
        """
        Generates initialization and all needed structures for LBlock and specified number of rounds.

        Parameters:
        ---------
        rounds                  :   int
                                    Number of rounds for the cipher

        model_as_bit_oriented   :   bool
                                    Argument on whether LBlock should be modeled as a bit-oriented cipher instead
                                    of as a 4-bit word-oriented cipher.
        """
        plaintextsize = 64
        keysize = 32

        if model_as_bit_oriented:
            super().__init__(rounds, plaintextsize, keysize, orientation=1, type_of_modeling=type_of_modeling,
                             cryptanalysis_type=cryptanalysis_type)
        else:
            super().__init__(rounds, plaintextsize, keysize, orientation=4, type_of_modeling=type_of_modeling,
                             cryptanalysis_type=cryptanalysis_type)

        # Summary of what's happening in LBlock:
        #   1. Teile Input in vordere Hälfte X_1, hintere Hälfte X_0
        #   2. Get subkey K_1 von K, bitshift X_0 <<< 8
        #   3. Round function mit X_1 und K_1 = F_1
        #   4. X_0 xor F_1
        #   5. X_1 und X_0 tauschen
        #   6. That was 1 round, now repeat 32 times

        #   determine xor output vars, dummy vars, and constraints
        if self.cryptanalysis_type == 'differential':
            xors_per_round = int(64 / self.orientation)
        elif self.cryptanalysis_type == 'linear':
            xors_per_round = 0
        else:
            xors_per_round = 0

        #   determine 3 way fork output vars, dummy vars, and constraints
        if self.cryptanalysis_type == 'differential':
            twf_per_round = 0
        else:  # self.cryptanalysis_type == 'linear':
            twf_per_round = int(32 / self.orientation)

        #   determine self.linear transformation output vars, dummy vars, and constraints
        lt_per_round = list()

        #   determine sbox output vars, dummy vars, and constraints
        if self.orientation == 1:
            # instantiating all SBoxes
            s_0_subs = {index: value for index, value in
                        enumerate([14, 9, 15, 0, 13, 4, 10, 11, 1, 2, 8, 3, 7, 6, 12, 5])}
            sbox_0 = SBox(s_0_subs, 4, 4, self, extract_sun_inequalities=self.extract_sun_inequalities)

            s_1_subs = {index: value for index, value in
                        enumerate([4, 11, 14, 9, 15, 13, 0, 10, 7, 12, 5, 6, 2, 8, 1, 3])}
            sbox_1 = SBox(s_1_subs, 4, 4, self, extract_sun_inequalities=self.extract_sun_inequalities)

            s_2_subs = {index: value for index, value in
                        enumerate([1, 14, 7, 12, 15, 13, 0, 6, 11, 5, 9, 3, 2, 4, 8, 10])}
            sbox_2 = SBox(s_2_subs, 4, 4, self, extract_sun_inequalities=self.extract_sun_inequalities)

            s_3_subs = {index: value for index, value in
                        enumerate([7, 6, 8, 11, 0, 15, 3, 14, 9, 10, 12, 13, 5, 2, 4, 1])}
            sbox_3 = SBox(s_3_subs, 4, 4, self, extract_sun_inequalities=self.extract_sun_inequalities)

            s_4_subs = {index: value for index, value in
                        enumerate([14, 5, 15, 0, 7, 2, 12, 13, 1, 8, 4, 9, 11, 10, 6, 3])}
            sbox_4 = SBox(s_4_subs, 4, 4, self, extract_sun_inequalities=self.extract_sun_inequalities)

            s_5_subs = {index: value for index, value in
                        enumerate([2, 13, 11, 12, 15, 14, 0, 9, 7, 10, 6, 3, 1, 8, 4, 5])}
            sbox_5 = SBox(s_5_subs, 4, 4, self, extract_sun_inequalities=self.extract_sun_inequalities)

            s_6_subs = {index: value for index, value in
                        enumerate([11, 9, 4, 14, 0, 15, 10, 13, 6, 12, 5, 7, 3, 8, 1, 2])}
            sbox_6 = SBox(s_6_subs, 4, 4, self, extract_sun_inequalities=self.extract_sun_inequalities)

            s_7_subs = {index: value for index, value in
                        enumerate([13, 10, 15, 0, 14, 4, 9, 11, 2, 1, 8, 3, 7, 5, 12, 6])}
            sbox_7 = SBox(s_7_subs, 4, 4, self, extract_sun_inequalities=self.extract_sun_inequalities)

            self.sboxes = [sbox_0, sbox_1, sbox_2, sbox_3, sbox_4, sbox_5, sbox_6, sbox_7]

        extra_xors = 0
        overwrites = 0

        self.prepare_for_type_of_modeling()

        if self.cryptanalysis_type == 'differential':
            key_variable_usage = True
        elif self.cryptanalysis_type == 'linear':
            key_variable_usage = False
        else:
            key_variable_usage = True

        sbox_dummy_variables_per_round = self.calculate_vars_and_constraints(xors_per_round, twf_per_round,
                                                                             lt_per_round, extra_xors, overwrites,
                                                                             new_keys_every_round=True,
                                                                             keys_are_used=key_variable_usage)

        # making sure we have at least one active sbox (minimizing active sboxes to zero is possible)
        if model_as_bit_oriented:
            sbox_dummy_variables = ["a" + str(i) for i in range(self.number_a_vars)]
        else:
            sbox_dummy_variables = list()
            if self.cryptanalysis_type == 'differential':
                for round in range(1, self.rounds + 1):
                    sbox_dummy_variables += ["x" + str(i) for i in range(16 * round, 16 * round + 8)]
            elif self.cryptanalysis_type == 'linear':
                sbox_dummy_variables = ["x" + str(i) for i in range(8, 8 * self.rounds)]
            else:
                pass

        for sbox_dummy in sbox_dummy_variables:
            self.M[self.M.get_shape()[0] - 1, self.V[sbox_dummy]] = 1
        self.M[self.M.get_shape()[0] - 1, self.V['constant']] = -1

        # adding a set to include the matrices of possible convex hull
        self.sbox_inequality_matrices = list()

        super().prepare_for_type_of_modeling()

        self.line = 0
        self.round_number = 1
        print(self.next)
        return
