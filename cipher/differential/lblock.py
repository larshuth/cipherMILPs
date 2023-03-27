from cipher.cipher import Cipher
from cipher.sbox import SBox

from scipy import lil_matrix


class LBlock(Cipher):
    """
    Class in which all functions for LBlock cipher [Wu et al 2011] are defined.
    """

    def extra_permutation_after_sbox(self, pos):
        if pos % 4 == 0:
            shift = -2
        elif pos % 4 == 1:
            shift = +1
        elif pos % 4 == 2:
            shift = -1
        elif pos % 4 == 3:
            shift = +2
        return shift * 4

    def rangenumber(self):
        """
        Defines what happens in a round.

        Parameters:
        ----------
        A   :   list
                Names of all variables in this current round

        Returns:
        ----------
            :   list of lists
                Specifies which variables belong in the constraint
        """
        # actions contain lists of either xors ['xor', input 1, input 2, output, dummy var],
        # 3-way forks ['3wf', input, output 1, output 2, dummy var], sboxes ['sbox', input start number, output start number, dummy var]
        words_total = int(64 / self.orientation)
        words_half = int(words_total / 2)
        first_number = int(self.A[0][1:])

        if self.round_number == 1:
            bonus = 32
        else:
            bonus = 0

        if self.cryptanalysis_type == 'differential':
            if self.orientation == 1:
                # sboxes are now required
                new_x_variables_per_round = 96  # 32 var for xor (1st half plaintext, key)
                new_xor_dummies_per_round = 64  # 32 var for xor (1st half plaintext, key)

                # 32 var for SBox (xor output), 32 var for xor (sbox output, 2nd half plaintext)
                # TODO: Grafik die das vernünftig darstellt/erklärt
                actions = [
                    ['xor',
                     self.A[i],
                     self.K[i],
                     'x' + str(int(self.A[i][1:]) + int(words_half) + bonus),
                     'd' + str((self.round_number - 1) * new_xor_dummies_per_round + i)
                     ] for i in range(words_half)]

                for i in range(8):
                    actions += [['sbox',
                                 new_x_variables_per_round * self.round_number - words_half + i * 4,
                                 new_x_variables_per_round * self.round_number + i * 4,
                                 'a' + str((self.round_number - 1) * int(self.number_a_vars / self.rounds) + i)]]

                start_val = 96 * self.round_number
                for index, shift in enumerate([+4, +8, -8, -4, +4, +8, -8, -4]):
                    actions += [['xor', 'x' + str(start_val + (index * 4) + shift + i), 'x' + str(32 + (index * 4) + i),
                                 'x' + str(128 + (index * 4) + i),
                                 'd' + str(32 + 64 * (self.round_number - 1) + (index * 4) + i)] for i in range(4)]
            else:
                pass

        elif self.cryptanalysis_type == 'linear':
            # TODO: Linear Cryptanalysis
            actions = [['3wf', self.A[i], self.round_number] for i in range(int(64 / self.orientation))]

        print(actions)
        return actions

    def gen_long_constraint(self, line, e):
        """
        Generates a long constraint depending on which variable is currently j.
        For Enocoro we take the first variables in j. With the last one, we use it to define it new
        """
        sbox_bijective = True
        sbox_invertible = True
        sbox_branchnumber = 2

        if e[0] == 'xor':
            # inequalities of xor are
            # (1.) input1 + input2 + output \leq 2*dummy
            # (2.) input1 \leq dummy
            # (3.) input2 \leq dummy
            # (4.) output \leq dummy
            input_var_1 = e[1]
            input_var_2 = e[2]
            output_var = e[3]
            dummy_var = e[4]
            input_var_1_pos_in_matrix = self.V[input_var_1]
            input_var_2_pos_in_matrix = self.V[input_var_2]
            output_var_pos_in_matrix = self.V[output_var]
            dummy_var_pos_in_matrix = self.V[dummy_var]

            # starting with (1.)
            self.M[line, input_var_1_pos_in_matrix] = 1
            self.M[line, input_var_2_pos_in_matrix] = 1
            self.M[line, output_var_pos_in_matrix] = 1
            self.M[line, dummy_var_pos_in_matrix] = -2
            line += 1

            # then (2.), (3.), and (4.)
            self.M[line, input_var_1_pos_in_matrix] = 1
            self.M[line, dummy_var_pos_in_matrix] = -1
            line += 1

            self.M[line, input_var_2_pos_in_matrix] = 1
            self.M[line, dummy_var_pos_in_matrix] = -1
            line += 1

            self.M[line, output_var_pos_in_matrix] = 1
            self.M[line, dummy_var_pos_in_matrix] = -1
            line += 1
        elif e[0] == 'sbox':
            # inequalities of sbox are
            # (1.) input \leq dummy for all inputs
            # (2.) sum over all inputs \geq dummy
            # (3.) if sbox bijective: sum_{i \in all_inputs}
            # (4.) if the sbox invertible with branch number 2:
            # (4.1) sum over inputs + sum over outputs \geq branch * new dummy
            # (4.2) input \leq new dummy for all inputs
            # (4.3) output \leq dummy for all outputs

            sbox_input_size = 4
            sbox_output_size = 4
            input_vars = ['x' + str(e[1] + i) for i in range(sbox_input_size)]
            output_vars = ['x' + str(e[2] + i) for i in range(sbox_output_size)]
            dummy_var = e[3]
            dummy_var_pos_in_matrix = self.V[dummy_var]

            # starting with (1.)
            for i in input_vars:
                input_var_pos_in_matrix = self.V[i]
                self.M[line, input_var_pos_in_matrix] = 1
                self.M[line, dummy_var_pos_in_matrix] = -1
                line += 1

            # then (2.)
            for i in input_vars:
                input_var_pos_in_matrix = self.V[i]
                self.M[line, input_var_pos_in_matrix] = -1
            self.M[line, dummy_var_pos_in_matrix] = 1
            line += 1

            # then (3.)
            if sbox_bijective:
                for i in input_vars:
                    input_var_pos_in_matrix = self.V[i]
                    self.M[line, input_var_pos_in_matrix] = sbox_input_size
                for o in output_vars:
                    output_var_pos_in_matrix = self.V[o]
                    self.M[line, output_var_pos_in_matrix] = -1
                line += 1

                for i in input_vars:
                    input_var_pos_in_matrix = self.V[i]
                    self.M[line, input_var_pos_in_matrix] = -1
                for o in output_vars:
                    output_var_pos_in_matrix = self.V[o]
                    self.M[line, output_var_pos_in_matrix] = sbox_output_size
                line += 1
            # and finally (4.) sbox invertible with branch number 2
            if (not sbox_invertible) or (not (sbox_branchnumber <= 2)):
                pass
                # TODO for when it comes up
                # Make a new dummy
                # (4.1) sum over inputs + sum over outputs \geq branch * new dummy
                # (4.2) input \leq new dummy for all inputs
                # (4.3) output \leq dummy for all outputs

        return line

    def shift_before(self):
        # in X0, there is a 8 bit shift to the left
        # pos is a short function to return  the proper position depending on whether we model LBlock as 4-bit word oriented of just bit oriented
        pos = lambda x: int(x / self.orientation)
        tmp = [self.A[pos(32 + i)] for i in range(pos(8))]
        for i in range(pos(32), pos(56)):
            self.A[i] = self.A[i + pos(8)]
        for index, elem in enumerate(range(pos(56), pos(64))):
            self.A[elem] = tmp[index]
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
        if self.orientation == 1:
            for i in range(32, 64):
                self.A[i] = self.A[i - 32]

            for i in range(32):
                self.A[i] = 'x' + str(96 * self.round_number + 32 + i)

        # this is actually not the size of the key but the array representing the subkey in each round
        keysize = int((64 / 2) / self.orientation)
        self.K = ['k' + str(self.round_number * keysize + i) for i in range(keysize)]
        self.round_number += 1
        return

    def __init__(self, rounds=32, model_as_bit_oriented=True):
        """
        Generates initialization and all needed structures for LBlock and specified number of rounds.

        Parameters:
        ---------
        rounds                  :   int
                                    Number of rounds for the cipher

        model_as_bit_oriented   :   bool
                                    Argument on whether or not LBlock should be modeled as a bit-oriented cipher instead
                                    of as a 4-bit word-oriented cipher.

                                    TODO: 4-bit word-oriented cipher not supported as of now
        """
        if model_as_bit_oriented:
            super().__init__(rounds, orientation=1)
        else:
            super().__init__(rounds, orientation=4)

        inputsize = 64

        self.cryptanalysis_type = 'differential'

        # Summary of what's happening in LBlock:
        #   1. Teile Input in vordere Hälfte X_1, hintere Hälfte X_0
        #   2. Get subkey K_1 von K, bitshift X_0 <<< 8
        #   3. Round function mit X_1 und K_1 = F_1
        #   4. X_0 xor F_1
        #   5. X_1 und X_0 tauschen
        #   6. That was 1 round, now repeat 32 times

        # self.next = number of currently used (x) variable
        self.next = 0
        # self.M = matrix representing the linear inequalities

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

        xor_dummy_variables_per_round = xors_per_round
        xor_constraints_per_round = 4 * xors_per_round
        xor_new_x_vars_per_round = xors_per_round

        #   determine 3 way fork output vars, dummy vars, and constraints
        if self.cryptanalysis_type == 'differential':
            twf_per_round = 0
        elif self.cryptanalysis_type == 'linear':
            twf_per_round = int(32 / self.orientation)

        twf_dummy_variables_per_round = twf_per_round
        twf_constraints_per_round = 4 * twf_per_round
        twf_new_x_vars_per_round = 2 * twf_per_round

        #   determine linear transformation output vars, dummy vars, and constraints
        lt_per_round = 0
        lt_dummy_variables_per_round = lt_per_round
        lt_constraints_per_round = 4 * lt_per_round
        lt_new_x_vars_per_round = 2 * lt_per_round

        #   determine sbox output vars, dummy vars, and constraints
        # TODO: Find out LBLOCK SBox Branch Number
        sbox_branch_number_leq_2 = True
        sbox_invertible = True
        sbox_bijective = True

        if self.orientation == 1:
            sboxes_per_round = 8

            # instantiating all sboxes
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

        else:
            sboxes_per_round = 0

        sbox_new_x_variables_per_round = 4 * sboxes_per_round
        sbox_dummy_variables_per_round = sboxes_per_round
        sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large = sboxes_per_round * sbox_branch_number_leq_2 * sbox_invertible
        sbox_constraints_per_round = sboxes_per_round * (
                1 + 4 + (sbox_bijective * 2) + (sbox_branch_number_leq_2 * sbox_invertible * (1 + 4 + 4)))

        encryption_key_vars = int((32 * self.rounds) / self.orientation)

        # self.M is lil_matrix((#constraints, #variables), dtype=int) with lil_matrix coming from the SciPy package

        number_constraints = ((xor_constraints_per_round +
                               twf_constraints_per_round +
                               sbox_constraints_per_round +
                               lt_constraints_per_round) * self.rounds) + 1

        number_variables = (plaintext_vars +
                            encryption_key_vars +
                            (
                                    xor_new_x_vars_per_round + xor_dummy_variables_per_round +
                                    twf_new_x_vars_per_round + twf_dummy_variables_per_round +
                                    lt_new_x_vars_per_round + lt_dummy_variables_per_round +
                                    sbox_new_x_variables_per_round + sbox_dummy_variables_per_round +
                                    sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large
                            ) * self.rounds) + 1

        self.M = lil_matrix((int(number_constraints), int(number_variables)), dtype=int)

        print(number_variables)

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
        self.V |= {'ds' + str(i): i + self.number_x_vars + self.number_d_vars + self.number_a_vars for i in
                   range(self.number_ds_vars)}
        self.V |= {i + self.number_x_vars + self.number_d_vars + self.number_a_vars: 'ds' + str(i) for i in
                   range(self.number_ds_vars)}

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
            for round in range(1, self.rounds + 1):
                sbox_dummy_variables = ["x" + str(i) for i in range(16 * round, 16 * (round + 1))]

        for sbox_dummy in sbox_dummy_variables:
            self.M[self.M.get_shape()[0] - 1, self.V[sbox_dummy]] = 1
        self.M[self.M.get_shape()[0] - 1, self.V['constant']] = -1

        self.round_number = 1
        return
