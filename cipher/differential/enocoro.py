from cipher.cipher import Cipher
from scipy.sparse import lil_matrix
from cipher.actions.lineartransformationaction import LinTransformationAction
from cipher.actions.xoraction import XorAction
from cipher.actions.sboxaction import SBoxAction
from cipher.sbox import SBox


class Enocoro(Cipher):
    """
    Class in which all functions for Enocoro are defined.
    """

    def generate_actions_for_round(self):
        """
        Defines what to go through in the for loop for gen_long_constraint.

        Parameters:
        ----------
        A   :   list
                Names of all variables in this current round

        Returns:
        ----------
            :   list of lists
                Specifies which variables belong in the constraint
        """
        list_of_actions = list()
        rounds_til_now = self.rounds - 1
        xors = 8
        sboxes = 4
        linear_transformations = 1

        if self.orientation == 1:
            # sboxes are now required
            bits_per_word = 8
            new_x_variables_per_round = (xors + sboxes + 2 * linear_transformations) * bits_per_word
            x_vars_so_far = 34 + (rounds_til_now * new_x_variables_per_round)

            new_dummies_per_round = (xors * bits_per_word) + linear_transformations + (
                        sboxes * self.sbox.dummy_vars_for_bit_oriented_modeling)
            dummies_so_far_prior_rounds = new_dummies_per_round * rounds_til_now

            # the actions are handled in the order of the numbering of their output variable in Fig.3 of Mouha et al
            def new_variable(i):
                return "x" + str(x_vars_so_far + i)
            dummies_so_far_this_round = 0
            new_x_variables_this_round = 0

            list_of_xor_inputs_positions = [(31 * bits_per_word + i, 32 * bits_per_word + i) for i in range(8)]
            list_of_xor_inputs = [(self.V[in_var_1], self.V[in_var_2]) for in_var_1, in_var_2 in
                                  list_of_xor_inputs_positions]
            for index, xor_input in enumerate(list_of_xor_inputs):  # total of 3 xors
                list_of_actions.append(XorAction(inputs=xor_input, output=new_variable(index),
                                                 dummy="d" + str(dummies_so_far_prior_rounds + index),
                                                 cipher_instance=self))

            dummies_so_far_this_round += len(list_of_xor_inputs)
            new_x_variables_this_round += len(list_of_xor_inputs)

            # sboxes are now required
            list_of_sbox_inputs_positions = [2, 7]
            list_of_sbox_inputs = [self.A[pos * 8] for pos in list_of_sbox_inputs_positions]
            for index, sbox_input in enumerate(list_of_sbox_inputs):
                list_of_actions.append(SBoxAction(sbox=self.sbox, input_start=sbox_input,
                                                  output_start=new_variable(new_x_variables_this_round + index),
                                                  dummy="d" + str(
                                                      dummies_so_far_prior_rounds + dummies_so_far_this_round + index),
                                                  cipher_instance=self))
                dummies_so_far_this_round += self.sbox.dummy_vars_for_bit_oriented_modeling

            list_of_xor_inputs = [(self.A[31], self.A[32]), (self.A[2], self.A[32]), (self.A[7], self.A[33])]
            for index, xor_input in enumerate(list_of_xor_inputs):  # total of 3 xors
                list_of_actions.append(XorAction(inputs=xor_input, output=new_variable(index),
                                                 dummy="d" + str(dummies_so_far_prior_rounds + index),
                                                 cipher_instance=self))

            xor_outputs_above_lin_trans = (new_variable(4), new_variable(5))

            lin_trans_outputs = (new_variable(6), new_variable(7))
            list_of_actions += [LinTransformationAction(inputs=xor_outputs_above_lin_trans, outputs=lin_trans_outputs,
                                                        dummy="d" + str(dummies_so_far_prior_rounds + 3),
                                                        cipher_instance=self)]

            list_of_xor_inputs = [(self.A[16], new_variable(6)), (self.A[29], new_variable(7)), (self.A[2], self.A[6]),
                                  (self.A[7], self.A[15]), (self.A[16], self.A[28])]
            for index, xor_input in enumerate(list_of_xor_inputs):  # additional 2 xors after the linear transformation
                list_of_actions.append(XorAction(inputs=xor_input, output=new_variable(index),
                                                 dummy="d" + str(dummies_so_far_prior_rounds + 4 + index),
                                                 cipher_instance=self))

                # sboxes are now required
                list_of_sbox_inputs = [16, 29]
                list_of_sbox_inputs = [self.A[pos * 8] for pos in list_of_sbox_inputs]
                for sbox_input in list_of_sbox_inputs:
                    list_of_actions.append(SBoxAction(sbox=self.sbox, input_start=sbox_input, output_start=list()))

        elif self.orientation == 8:
            new_x_variables_per_round = (xors + 2 * linear_transformations)
            x_vars_so_far = 34 + (rounds_til_now * new_x_variables_per_round)
            new_dummies_per_round = xors + linear_transformations
            dummies_so_far_prior_rounds = new_dummies_per_round * rounds_til_now

            # the actions are handled in the order of the numbering of their output variable in Fig.3 of Mouha et al
            def new_variable(i):
                return "x" + str(x_vars_so_far + i)
            list_of_xor_inputs = [(self.A[31], self.A[32]), (self.A[2], self.A[32]), (self.A[7], self.A[33])]
            for index, xor_input in enumerate(list_of_xor_inputs):  # total of 3 xors
                list_of_actions.append(XorAction(inputs=xor_input, output=new_variable(index),
                                                 dummy="d" + str(dummies_so_far_prior_rounds + index),
                                                 cipher_instance=self))
            xor_outputs_above_lin_trans = (new_variable(4), new_variable(5))

            lin_trans_outputs = (new_variable(6), new_variable(7))
            list_of_actions += [LinTransformationAction(inputs=xor_outputs_above_lin_trans, outputs=lin_trans_outputs,
                                                        dummy="d" + str(dummies_so_far_prior_rounds + 3),
                                                        cipher_instance=self)]

            list_of_xor_inputs = [(self.A[16], new_variable(6)), (self.A[29], new_variable(7)), (self.A[2], self.A[6]),
                                  (self.A[7], self.A[15]), (self.A[16], self.A[28])]
            for index, xor_input in enumerate(list_of_xor_inputs):  # additional 2 xors after the linear transformation
                list_of_actions.append(XorAction(inputs=xor_input, output=new_variable(index),
                                                 dummy="d" + str(dummies_so_far_prior_rounds + 4 + index),
                                                 cipher_instance=self))
        else:
            pass
        return list_of_actions

    def gen_long_constraint(self, action):
        """
        """
        action.run_action()
        return

    def shift_before(self):
        """
        In Enocoro, at the beginning of a round the bits are not shifted so this does nothing
        """
        pass
        return

    def shift_after(self):
        """"
        This function shifts all the bits used in the current round to the right.

        Parameters:
        ----------
        A   :   list
                Current variables

        Returns:
        ---------
        A   :   list
                Shifted variables that can be used for the next round
        """
        la = self.A[31]
        for i in range(31, -1, -1):
            temp = self.A[i]
            self.A[i + 1] = temp
        self.A[0] = la

        self.A[0] = "x" + str(34 + 10 * (self.round_number - 1))
        self.A[3] = "x" + str(34 + 10 * (self.round_number - 1) + 8)
        self.A[8] = "x" + str(34 + 10 * (self.round_number - 1) + 9)
        self.A[17] = "x" + str(34 + 10 * (self.round_number - 1) + 10)

        self.A[32] = "x" + str(34 + 10 * (self.round_number - 1) + 6)
        self.A[33] = "x" + str(34 + 10 * (self.round_number - 1) + 7)

        self.round_number += 1
        return

    def __init__(self, rounds=1, model_as_bit_oriented=False, convex_hull_applied=False):
        """
        Generates initialization and all neded structures for Enocoro and specified number of rounds.

        Parameters:
        ---------
        rounds  :   int
                    Number of rounds for the cipher

        Returns:
        ---------
        A       :   list
                    Names of all variables in this current round

        M       :   lil_matrix
                    The empty constraint matrix for the MILP

        V       :   list
                    This list saves all the variables

        next    :   int
                    Number for the next x-variable
        """

        if model_as_bit_oriented:
            super().__init__(rounds, orientation=1)
        else:
            super().__init__(rounds, orientation=8)

        inputsize = 256  # see an explanation of Enocoro for the weird breakdown (kex, input, pre-def constraints, etc)

        self.cryptanalysis_type = 'differential'

        # note that convex hull application (as shown in Sun et al. 2013 and Baksi 2020 is only used for sboxes which
        # are only modeled in bit-oriented ciphers)
        self.convex_hull_applied = convex_hull_applied

        # with mouha, every round, there are
        #   1 dummy + 1 output per XOR, 1 dummy per linear transformation, dummy + 2 output per 3-way fork,
        #   and 1 dummy + v output per w*v sbox
        #   4 inequalities per XOR
        #   2*l + 1 inequalities per linear transformation L: F_2^l -> F_2^l
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
            twf_per_round = int(64 / self.orientation)

        twf_dummy_variables_per_round = twf_per_round
        twf_constraints_per_round = 4 * twf_per_round
        twf_new_x_vars_per_round = 2 * twf_per_round

        #   determine linear transformation output vars, dummy vars, and constraints
        lt_per_round = 1
        lt_dummy_variables_per_round = lt_per_round
        lt_constraints_per_round = 5 * lt_per_round
        lt_new_x_vars_per_round = 2 * lt_per_round

        #   determine sbox output vars, dummy vars, and constraints
        if self.orientation == 1:
            sbox_subs = {key: value for key, value in enumerate(
                [99, 82, 26, 223, 138, 246, 174, 85, 137, 231, 208, 45, 189, 1, 36, 120, 27, 217, 227, 84, 200, 164,
                 236,
                 126, 171, 0, 156, 46, 145, 103, 55, 83, 78, 107, 108, 17, 178, 192, 130, 253, 57, 69, 254, 155, 52,
                 215,
                 167, 8, 184, 154, 51, 198, 76, 29, 105, 161, 110, 62, 197, 10, 87, 244, 241, 131, 245, 71, 31, 122,
                 165,
                 41, 60, 66, 214, 115, 141, 240, 142, 24, 170, 193, 32, 191, 230, 147, 81, 14, 247, 152, 221, 186, 106,
                 5,
                 72, 35, 109, 212, 30, 96, 117, 67, 151, 42, 49, 219, 132, 25, 175, 188, 204, 243, 232, 70, 136, 172,
                 139,
                 228, 123, 213, 88, 54, 2, 177, 7, 114, 225, 220, 95, 47, 93, 229, 209, 12, 38, 153, 181, 111, 224, 74,
                 59,
                 222, 162, 104, 146, 23, 202, 238, 169, 182, 3, 94, 211, 37, 251, 157, 97, 89, 6, 144, 116, 44, 39, 149,
                 160, 185, 124, 237, 4, 210, 80, 226, 73, 119, 203, 58, 15, 158, 112, 22, 92, 239, 33, 179, 159, 13,
                 166,
                 201, 34, 148, 250, 75, 216, 101, 133, 61, 150, 40, 20, 91, 102, 234, 127, 206, 249, 64, 19, 173, 195,
                 176,
                 242, 194, 56, 128, 207, 113, 11, 135, 77, 53, 86, 233, 100, 190, 28, 187, 183, 48, 196, 43, 255, 98,
                 65,
                 168, 21, 140, 18, 199, 121, 143, 90, 252, 205, 9, 79, 125, 248, 134, 218, 16, 50, 118, 180, 163, 63,
                 68,
                 129, 235])}
            # taken from the appendix of https://www.ipa.go.jp/en/security/jcmvp/g6ovkg00000065j3-att/23_00espec.pdf
            self.sbox = SBox(sbox_subs, 8, 8, self)

            self.sboxes = [self.sbox, self.sbox, self.sbox, self.sbox]

            sboxes_per_round = 4

            bijective_sboxes_per_round = sum([int(sbox.is_bijective) for sbox in self.sboxes])
            # the entry for a sbox is 1 iff the sbox is not invertible or its branch number is larger than 2
            extra_constraint_sboxes_per_round = sum(
                [1 ^ int(sbox.is_invertible and sbox.branch_number <= 2) for sbox in self.sboxes])
        else:
            sboxes_per_round = 0
            bijective_sboxes_per_round = 0
            extra_constraint_sboxes_per_round = 0

        sbox_new_x_variables_per_round = 4 * sboxes_per_round
        sbox_dummy_variables_per_round = sboxes_per_round
        sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large = extra_constraint_sboxes_per_round
        sbox_constraints_per_round = sboxes_per_round * (
                1 + 4) + bijective_sboxes_per_round * 2 + extra_constraint_sboxes_per_round * (1 + 4 + 4)

        encryption_key_vars = int((0 * self.rounds) / self.orientation)

        # self.M is lil_matrix((#constraints, #variables), dtype=int) with lil_matrix coming from the SciPy package

        number_constraints = ((xor_constraints_per_round +
                               twf_constraints_per_round +
                               sbox_constraints_per_round +
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
        self.number_d_vars = (
                                     xor_dummy_variables_per_round + twf_dummy_variables_per_round + lt_dummy_variables_per_round) * self.rounds
        self.number_a_vars = int(sbox_dummy_variables_per_round * self.rounds)
        self.number_ds_vars = int(sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large * self.rounds)

        self.V = {'x' + str(i): i for i in range(self.number_x_vars)}
        self.V |= {i: 'x' + str(i) for i in range(self.number_x_vars)}

        self.V |= {'d' + str(i): i + self.number_x_vars for i in range(self.number_d_vars)}
        self.V |= {i + self.number_x_vars: 'd' + str(i) for i in range(self.number_d_vars)}

        self.V |= {'a' + str(i): i + self.number_x_vars + self.number_d_vars for i in range(self.number_a_vars)}
        self.V |= {i + self.number_x_vars + self.number_d_vars: 'a' + str(i) for i in range(self.number_a_vars)}

        list_of_ds_vars = ['ds' + str(i) + str(r)
                           for i in range(sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large)
                           for r in range(self.rounds)]
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
        self.A = ['x' + str(i) for i in range(int((inputsize / self.orientation) + (16 / self.orientation)))]

        # making sure we have at least one active sbox (minimizing active sboxes to zero is possible)
        if model_as_bit_oriented:
            sbox_dummy_variables = ["a" + str(i) for i in range(sbox_dummy_variables_per_round)]
        else:
            sbox_dummy_variables = ["x" + str(number) for number in self.input_sbox()]

        for sbox_dummy in sbox_dummy_variables:
            self.M[self.M.get_shape()[0] - 1, self.V[sbox_dummy]] = 1
        self.M[self.M.get_shape()[0] - 1, self.V['constant']] = -1

        # adding a set to include the matrices of possible convex hull
        self.convex_hull_inequality_matrices = list()

        self.line = 0
        self.round_number = 1
        return

    def input_sbox(self):
        inputsbox = []
        for i in range(self.rounds):
            # first sbox
            if i < 3:
                inputsbox.append((2 - i))
            else:
                inputsbox.append(34 + (i - 3) * 10)
            # second sbox
            if i < 5:
                inputsbox.append(7 - i)
            else:
                inputsbox.append(41 + (i - 5) * 10)
            # third sbox
            if i < 9:
                inputsbox.append(16 - i)
            else:
                inputsbox.append(42 + (i - 9) * 10)
            # fourth sbox
            if i < 13:
                inputsbox.append(29 - i)
            else:
                inputsbox.append(43 + (i - 13) * 10)
        return inputsbox
