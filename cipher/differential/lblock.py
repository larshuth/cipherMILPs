from cipher.cipher import Cipher
from cipher.sbox import SBox
from cipher.actions import SBoxAction, XorAction, PermutationAction, OverwriteAction
import convexHull

from scipy.sparse import lil_matrix


class LBlock(Cipher):
    """
    Class in which all functions for LBlock cipher [Wu et al 2011] are defined.
    """

    def generate_f_function_actions(self):
        list_of_f_function_actions = list()
        list_of_f_function_actions += self.generate_key_xor_actions_for_round()
        list_of_f_function_actions += self.generate_sbox_actions_for_round()
        list_of_f_function_actions += self.generate_permutation_after_sbox_actions_for_round()
        return list_of_f_function_actions

    def generate_key_xor_actions_for_round(self):
        list_of_key_xor_actions = list()
        for i in range(int(len(self.A)/2)):
            list_of_key_xor_actions.append(XorAction(inputs=(self.A[i], self.K[i]),
                                                     cipher_instance=self, a_position_to_overwrite=i))
        return list_of_key_xor_actions

    def generate_sbox_actions_for_round(self):
        list_of_sbox_actions = list()
        if self.orientation == 1:
            extract_int_from_x_var = lambda x_var_name: int(x_var_name[1:])
            for i in range(8):
                first_input_element_position_in_A = sum(self.sboxes[prior].in_bits for prior in range(i))
                input_start = extract_int_from_x_var(self.A[first_input_element_position_in_A])
                list_of_sbox_actions.append(SBoxAction(sbox=self.sboxes[i], input_start=input_start,
                                                       cipher_instance=self,
                                                       first_a_position_to_overwrite=first_input_element_position_in_A))
        else:
            pass
        return list_of_sbox_actions

    def generate_permutation_after_sbox_actions_for_round(self):
        list_of_permutation_actions = list()
        permutation = list()
        block_size = int(4/self.orientation)
        for index, shift in enumerate([+1, +2, -2, -1, +1, +2, -2, -1]):
            permutation += [(index + shift) * block_size * i for i in range(int(4/self.orientation))]
        # this shifts the elements in self.A such that [0,1,2,3,4,5,6,7,8,9 ...] becomes [4,5,6,7,12,13,14,15,0,1 ...]
        permutation += list(range(self.plaintextsize/2, self.plaintextsize))
        # permutation needs to span the whole A list, even if not all of them are changed
        list_of_permutation_actions.append(PermutationAction(permutation, self))
        return list_of_permutation_actions

    def generate_bitshift_actions_for_round(self):
        list_of_bitshift_actions = list()
        permutation = list()
        permutation += list(range(self.plaintextsize / 2))
        # permutation needs to span the whole A list, even if not all of them are changed
        # using the previously written code if just due to laziness
        block_size = int(4 / self.orientation)
        for index, shift in enumerate([+2] * 8):
            permutation += [((index + shift) * block_size * i) % (8*block_size) for i in range(int(4 / self.orientation))]
        # this shifts the elements in self.A such that [0,1,2,3,4,5,6,7 ...] becomes [8,9,10,11,12,13,14,15 ...]
        list_of_bitshift_actions.append(PermutationAction(permutation, self))
        return list_of_bitshift_actions

    def generate_f_output_right_plaintext_xor_actions_for_round(self):
        f_output_right_plaintext_xor_actions_list = list()
        half_length = int(self.plaintextsize/2)
        f_output_right_plaintext_xor_actions_list += [XorAction(inputs=(self.A[i], self.A[i + half_length]), cipher_instance=self, a_position_to_overwrite= (i + half_length)) for i in range(half_length)]
        return f_output_right_plaintext_xor_actions_list

    def generate_actions_for_round(self):
        list_of_actions = list()
        # Feistel f-function, includes key xor-ing, sboxes and permutation
        list_of_actions += self.generate_f_function_actions()
        list_of_actions += self.generate_bitshift_actions_for_round()
        list_of_actions += self.generate_f_output_right_plaintext_xor_actions_for_round()
        return list_of_actions

    def run_round(self):
        x1_size = int(self.plaintextsize / 2)
        x1_backup = self.A[:x1_size].copy()

        for action in self.generate_actions_for_round():
            self.gen_long_constraint(action)

        # renew the elements s.t. the first half of A, X_1 in the og paper,
        self.A[:x1_size] = x1_backup

        # and switch left and right
        self.A = self.A[x1_size:] + self.A[:x1_size]

        # this is actually not the size of the key but the array representing the subkey in each round
        self.K = ['k' + str(self.round_number * self.keysize + i) for i in range(keysize)]
        self.round_number += 1
        return True

    def __init__(self, rounds=32, model_as_bit_oriented=True, convex_hull_applied=True):
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
        if model_as_bit_oriented:
            super().__init__(rounds, orientation=1)
        else:
            super().__init__(rounds, orientation=4)

        inputsize = 64

        self.cryptanalysis_type = 'differential'

        # note that convex hull application (as shown in Sun et al. 2013 and Baksi 2020 is only used for sboxes which
        # are only modeled in bit-oriented ciphers)
        self.convex_hull_applied = convex_hull_applied

        # Summary of what's happening in LBlock:
        #   1. Teile Input in vordere Hälfte X_1, hintere Hälfte X_0
        #   2. Get subkey K_1 von K, bitshift X_0 <<< 8
        #   3. Round function mit X_1 und K_1 = F_1
        #   4. X_0 xor F_1
        #   5. X_1 und X_0 tauschen
        #   6. That was 1 round, now repeat 32 times

        # self.next = number of currently used (x) variable
        self.next = 0
        # self.M = matrix representing the self.linear inequalities

        # with mouha, every round, there are
        #   1 dummy + 1 output per XOR, 1 dummy per self.linear transformation, dummy + 2 output per 3-way fork,
        #   and 1 dummy + v output per w*v sbox
        #   4 inequalities per XOR
        #   2*l + 1 inequalities per self.linear transformation L: F_2^l -> F_2^l
        #   4 per 3-fork branch
        # Das Nicky Paper war byte-oriented (e.g. 32 byte input in Enocoro) während das
        # Sun Paper bit-oriented ist (e.g. 64 bit input in LBlock)
        # with sun, every round there are:
        #   1 + w constraints are necessary for all (w*v)-sboxes
        #   2 more are needed if the sbox is symmetric
        #   w + v + 1 more, redundant if the sbox invertible with branch number 2

        #   determine plaintext vars
        plaintext_vars = inputsize / self.orientation

        #   determine xor output vars, dummy vars, and constraints
        if self.cryptanalysis_type == 'differential':
            xors_per_round = int(64 / self.orientation)
        elif self.cryptanalysis_type == 'linear':
            xors_per_round = 0
        else:
            xors_per_round = 0

        xor_dummy_variables_per_round = xors_per_round
        xor_constraints_per_round = 4 * xors_per_round
        xor_new_x_vars_per_round = xors_per_round

        #   determine 3 way fork output vars, dummy vars, and constraints
        if self.cryptanalysis_type == 'differential':
            twf_per_round = 0
        else:  # self.cryptanalysis_type == 'linear':
            twf_per_round = int(32 / self.orientation)

        twf_dummy_variables_per_round = twf_per_round
        twf_constraints_per_round = 4 * twf_per_round
        twf_new_x_vars_per_round = 2 * twf_per_round

        #   determine self.linear transformation output vars, dummy vars, and constraints
        lt_per_round = 0
        lt_dummy_variables_per_round = lt_per_round
        lt_constraints_per_round = 4 * lt_per_round
        lt_new_x_vars_per_round = 2 * lt_per_round

        #   determine sbox output vars, dummy vars, and constraints
        if self.orientation == 1:
            # instantiating all SBoxes
            s_0_subs = {index: value for index, value in
                        enumerate([14, 9, 15, 0, 13, 4, 10, 11, 1, 2, 8, 3, 7, 6, 12, 5])}
            sbox_0 = SBox(s_0_subs, 4, 4)

            s_1_subs = {index: value for index, value in
                        enumerate([4, 11, 14, 9, 15, 13, 0, 10, 7, 12, 5, 6, 2, 8, 1, 3])}
            sbox_1 = SBox(s_1_subs, 4, 4)

            s_2_subs = {index: value for index, value in
                        enumerate([1, 14, 7, 12, 15, 13, 0, 6, 11, 5, 9, 3, 2, 4, 8, 10])}
            sbox_2 = SBox(s_2_subs, 4, 4)

            s_3_subs = {index: value for index, value in
                        enumerate([7, 6, 8, 11, 0, 15, 3, 14, 9, 10, 12, 13, 5, 2, 4, 1])}
            sbox_3 = SBox(s_3_subs, 4, 4)

            s_4_subs = {index: value for index, value in
                        enumerate([14, 5, 15, 0, 7, 2, 12, 13, 1, 8, 4, 9, 11, 10, 6, 3])}
            sbox_4 = SBox(s_4_subs, 4, 4)

            s_5_subs = {index: value for index, value in
                        enumerate([2, 13, 11, 12, 15, 14, 0, 9, 7, 10, 6, 3, 1, 8, 4, 5])}
            sbox_5 = SBox(s_5_subs, 4, 4)

            s_6_subs = {index: value for index, value in
                        enumerate([11, 9, 4, 14, 0, 15, 10, 13, 6, 12, 5, 7, 3, 8, 1, 2])}
            sbox_6 = SBox(s_6_subs, 4, 4)

            s_7_subs = {index: value for index, value in
                        enumerate([13, 10, 15, 0, 14, 4, 9, 11, 2, 1, 8, 3, 7, 5, 12, 6])}
            sbox_7 = SBox(s_7_subs, 4, 4)

            self.sboxes = [sbox_0, sbox_1, sbox_2, sbox_3, sbox_4, sbox_5, sbox_6, sbox_7]

            sboxes_per_round = 8

            bijective_sboxes_per_round = sum([int(sbox.is_bijective) for sbox in self.sboxes])
            # the entry for a sbox is 1 iff the sbox is not invertible or its branch number is larger than 2
            extra_constraint_sboxes_per_round = sum(
                [1 ^ int(sbox.is_invertible and sbox.branch_number <= 2) for sbox in self.sboxes])
        else:
            sboxes_per_round = 0
            bijective_sboxes_per_round = 0
            extra_constraint_sboxes_per_round = 0

        sbox_new_x_variables_per_round = self.orientation * sboxes_per_round
        sbox_dummy_variables_per_round = sboxes_per_round
        sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large = extra_constraint_sboxes_per_round
        sbox_constraints_per_round_following_sun = sboxes_per_round * (
                1 + 4) + bijective_sboxes_per_round * 2 + extra_constraint_sboxes_per_round * (1 + 4 + 4)

        encryption_key_vars = int((32 * self.rounds) / self.orientation)

        # self.M is lil_matrix((#constraints, #variables), dtype=int) with lil_matrix coming from the SciPy package

        number_constraints = ((xor_constraints_per_round +
                               twf_constraints_per_round +
                               sbox_constraints_per_round_following_sun +
                               lt_constraints_per_round) * self.rounds) + 1
        number_constraints = int(number_constraints)

        self.number_variables = (plaintext_vars +
                                 encryption_key_vars +
                                 (
                                         xor_new_x_vars_per_round + xor_dummy_variables_per_round +
                                         twf_new_x_vars_per_round + twf_dummy_variables_per_round +
                                         lt_new_x_vars_per_round + lt_dummy_variables_per_round +
                                         sbox_new_x_variables_per_round + sbox_dummy_variables_per_round +
                                         sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large
                                 ) * self.rounds) + 1
        self.number_variables = int(self.number_variables)

        self.M = lil_matrix((number_constraints, self.number_variables), dtype=int)

        # we order M by: x variables (cipher bits), d dummy variables (xor), a dummy variables (bit oriented sboxes),
        # this ordering is self.V = dict of all variables mapping names to entry in self.M
        self.number_x_vars = int(plaintext_vars + ((
                                                           xor_new_x_vars_per_round + twf_new_x_vars_per_round + lt_new_x_vars_per_round + sbox_new_x_variables_per_round) * self.rounds))
        self.number_d_vars = (xor_dummy_variables_per_round + twf_dummy_variables_per_round) * self.rounds
        self.number_a_vars = int(sbox_dummy_variables_per_round * self.rounds)
        self.number_ds_vars = int(sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large * self.rounds)

        self.V = {'x' + str(i): i for i in range(self.number_x_vars)}
        self.V |= {i: 'x' + str(i) for i in range(self.number_x_vars)}

        self.V |= {'d' + str(i): i + self.number_x_vars for i in range(self.number_d_vars)}
        self.V |= {i + self.number_x_vars: 'd' + str(i) for i in range(self.number_d_vars)}

        self.V |= {'a' + str(i): i + self.number_x_vars + self.number_d_vars for i in range(self.number_a_vars)}
        self.V |= {i + self.number_x_vars + self.number_d_vars: 'a' + str(i) for i in range(self.number_a_vars)}

        list_of_ds_vars = ['ds' + str(i)
                           for i in range(sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large * self.rounds)]
        self.V |= {var_name: index + self.number_x_vars + self.number_d_vars + self.number_a_vars
                   for index, var_name in enumerate(list_of_ds_vars)}
        self.V |= {index + self.number_x_vars + self.number_d_vars + self.number_a_vars: var_name
                   for index, var_name in enumerate(list_of_ds_vars)}

        self.V |= {'k' + str(i): i + self.number_x_vars + self.number_d_vars + self.number_a_vars + self.number_ds_vars
                   for i in range(encryption_key_vars)}
        self.V |= {i + self.number_x_vars + self.number_d_vars + self.number_a_vars + self.number_ds_vars: 'k' + str(i)
                   for i in range(encryption_key_vars)}

        self.V['constant'] = self.M.get_shape()[1] - 1
        self.V[self.M.get_shape()[1] - 1] = 'constant'

        # list mit den Bits die momentan in der Cipher sind
        self.A = ['x' + str(i) for i in range(int(inputsize / self.orientation))]
        self.K = ['k' + str(i) for i in range(int((inputsize / 2) / self.orientation))]

        # making sure we have at least one active sbox (minimizing active sboxes to zero is possible)
        if model_as_bit_oriented:
            sbox_dummy_variables = ["a" + str(i) for i in range(sbox_dummy_variables_per_round)]
        else:
            sbox_dummy_variables = list()
            for round in range(1, self.rounds + 1):
                sbox_dummy_variables += ["x" + str(i) for i in range(16 * round, 16 * (round + 1))]

        for sbox_dummy in sbox_dummy_variables:
            self.M[self.M.get_shape()[0] - 1, self.V[sbox_dummy]] = 1
        self.M[self.M.get_shape()[0] - 1, self.V['constant']] = -1

        # adding a set to include the matrices of possible convex hull
        self.sbox_inequality_matrices = list()

        self.line = 0
        self.round_number = 1
        return
