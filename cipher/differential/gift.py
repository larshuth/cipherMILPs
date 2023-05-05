from cipher.cipher import Cipher
from cipher.sbox import SBox
from cipher.actions import SBoxAction, XorAction, PermutationAction, OverwriteAction, LinTransformationAction

from scipy.sparse import lil_matrix


class Gift64(Cipher):
    """
    Class in which all functions for AES are defined.
    """

    def generate_sbox_actions_for_round(self):
        list_of_sbox_actions = list()
        rounds_til_now = self.rounds - 1
        for index, sbox in enumerate(self.sboxes):
            first_element = int(self.A[index * 4][1:])
            list_of_sbox_actions.append(SBoxAction(sbox=sbox, input_start=first_element, cipher_instance=self,
                                                   first_a_position_to_overwrite=index * 4))
        return list_of_sbox_actions

    def generate_permutation_actions_for_round(self):
        permutation = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3, 4, 21, 38, 55, 52, 5, 22, 39, 36, 53,
                       6, 23, 20, 37, 54, 7, 8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11, 12, 29, 46,
                       63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]
        list_of_permutation_actions = [PermutationAction(permutation, self)]
        return list_of_permutation_actions

    def generate_key_xor_actions_for_round(self):
        list_of_key_xor_actions = list()
        list_of_xor_positions = [4 * i for i in range(16)] + [(4 * i) + 1 for i in range(16)]
        for key_index, a_index in enumerate(list_of_xor_positions):
            list_of_key_xor_actions.append(XorAction((self.A[a_index], self.K[key_index]), self))
        return list_of_key_xor_actions

    def generate_single_bit_xor_actions(self):
        list_of_single_bit_xor_actions = list()
        single_bit_xor_positions = [self.plaintextsize - 1, 23, 19, 15, 11, 7, 3]
        for pos in single_bit_xor_positions:
            list_of_single_bit_xor_actions.append(LinTransformationAction([self.A[pos]], self, 1, [pos]))
        return list_of_single_bit_xor_actions

    def run_round(self):
        print(f"Round {self.round_number} start")

        for sboxaction in self.generate_sbox_actions_for_round():
            sboxaction.run_action()

        for permutationsaction in self.generate_permutation_actions_for_round():
            permutationsaction.run_action()

        for keyaction in self.generate_key_xor_actions_for_round():
            keyaction.run_action()

        for single_bit_xor_action in self.generate_single_bit_xor_actions():
            single_bit_xor_action.run_action()

        self.K = ['k' + str(self.round_number * self.key_vars + i) for i in range(self.key_vars)]
        print(f"Round {self.round_number} end")
        self.round_number += 1
        return True

    def __init__(self, rounds=1, model_as_bit_oriented=False):
        """
        Generates initialization and all needed structures for AES and specified number of rounds.

        Parameters:
        ---------
        rounds  :   int
                    Number of rounds for the cipher

        Returns:
        ---------
        Creates Instance, no return value
        """
        plaintextsize = 64
        keysize = 32

        super().__init__(rounds, plaintextsize, keysize, orientation=1)

        self.cryptanalysis_type = 'differential'

        # Summary of what's happening in GIFT:

        #   determine xor output vars, dummy vars, and constraints
        if self.cryptanalysis_type == 'differential':
            xors_per_round = 32
            extra_xors = 0
        elif self.cryptanalysis_type == 'linear':
            xors_per_round = 0
            extra_xors = 0
        else:
            xors_per_round = 0
            extra_xors = 0

        #   determine 3 way fork output vars, dummy vars, and constraints
        if self.cryptanalysis_type == 'differential':
            twf_per_round = 0
        else:  # self.cryptanalysis_type == 'linear':
            twf_per_round = 0

        #   determine linear transformation output vars, dummy vars, and constraints
        lt_per_round = [1 for _ in range(7)]

        #   determine sbox output vars, dummy vars, and constraints
        if self.orientation == 1:
            # instantiating all SBoxes
            sbox_aes_subs = {index: value for index, value in
                             enumerate(
                                 [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14])}
            # with the list taken from https://github.com/pcaro90/Python-AES/blob/master/AES_base.py and not verified :)
            self.sbox = SBox(sbox_aes_subs, 4, 4)

            self.sboxes = [self.sbox] * 16

        overwrites = 0  # for the ColumnMix operations in AES where (as off Zhou) the
        # variables are just overwritten because otherwise it is too complex

        sbox_dummy_variables_per_round = self.calculate_vars_and_constraints(xors_per_round, twf_per_round,
                                                                             lt_per_round, extra_xors, overwrites,
                                                                             new_keys_every_round=True)

        # making sure we have at least one active sbox (minimizing active sboxes to zero is possible)
        sbox_dummy_variables = ["a" + str(i) for i in range(self.number_a_vars)]

        for sbox_dummy in sbox_dummy_variables:
            self.M[self.M.get_shape()[0] - 1, self.V[sbox_dummy]] = 1
        self.M[self.M.get_shape()[0] - 1, self.V['constant']] = -1

        # adding a set to include the matrices of possible convex hull
        self.sbox_inequality_matrices = list()

        self.line = 0
        self.round_number = 1
        return
