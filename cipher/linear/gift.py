from cipher.differential.gift import Gift64
from cipher.cipher import Cipher
from cipher.sbox import SBox
from cipher.actions.threeforkedbranchaction import ThreeForkedBranchAction


class Gift64_linear(Gift64):
    """
    Class in which all functions for AES are defined.
    """
    def generate_threeforkedbranch_actions_for_round(self):
        list_of_threeforkedbranch_actions = list()
        for i in range():

        return

    def run_round(self):
        print(f"Round {self.round_number} start")
        for threewayforkaction in self.generate_threewayfork_actions_for_round():
            threewayforkaction.run_action()

        for sboxaction in self.generate_sbox_actions_for_round():
            sboxaction.run_action()

        for permutationsaction in self.generate_permutation_actions_for_round():
            permutationsaction.run_action()

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
