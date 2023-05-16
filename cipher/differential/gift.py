from cipher.cipher import Cipher
from cipher.sbox import SBox
from cipher.actions.permutationaction import PermutationAction
from cipher.actions.lineartransformationaction import LinTransformationAction
from cipher.actions.xoraction import XorAction
from cipher.actions.sboxaction import SBoxAction


class Gift64(Cipher):
    """
    Class in which all functions for AES are defined.
    """

    def generate_sbox_actions_for_round(self):
        list_of_sbox_actions = list()
        rounds_til_now = self.rounds - 1
        for index, sbox in enumerate(self.sboxes):
            sbox_input_vars = [self.A[index * 4 + var] for var in range(sbox.in_bits)]
            list_of_sbox_actions.append(SBoxAction(sbox=sbox, input_vars=sbox_input_vars, cipher_instance=self,
                                                   first_a_position_to_overwrite=index * 4))
        return list_of_sbox_actions

    def generate_permutation_actions_for_round(self):
        new_position_of_x = lambda x: (4 * (x // 16)) + (16 * (((3 * ((x % 16) // 4)) + (x % 4)) % 4)) + (x % 4)
        permutation = [0 for _ in range(64)]
        for i in range(64):
            permutation[new_position_of_x(i)] = i
        list_of_permutation_actions = [PermutationAction(permutation, self)]
        return list_of_permutation_actions

    def generate_key_xor_actions_for_round(self):
        list_of_key_xor_actions = list()
        set_of_xor_positions = set([4 * i for i in range(16)] + [(4 * i) + 1 for i in range(16)])
        xors_so_far = 0
        for a_index, a_var in enumerate(self.A):
            if a_index in set_of_xor_positions:
                list_of_key_xor_actions.append(
                    XorAction((a_var, self.K[xors_so_far]), self, a_position_to_overwrite=a_index))
                xors_so_far += 1
        return list_of_key_xor_actions

    def generate_single_bit_xor_actions(self):
        list_of_single_bit_xor_actions = list()
        single_bit_xor_positions = [3, 7, 11, 15, 19, 23, self.plaintextsize - 1]
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

    def __init__(self, rounds=1, model_as_bit_oriented=True, cryptanalysis_type='differential'):
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

        if not model_as_bit_oriented:
            raise Exception(
                "GIft64 can only be called as bit-oriented, there is no word-orientation of word size > 1 available.")

        super().__init__(rounds, plaintextsize, keysize, orientation=1)

        self.cryptanalysis_type = cryptanalysis_type

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
