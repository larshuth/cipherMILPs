from cipher.cipher import Cipher
from cipher.sbox import SBox
from cipher.actions import SBoxAction, XorAction, PermutationAction, OverwriteAction

from scipy.sparse import lil_matrix


class Aes(Cipher):
    """
    Class in which all functions for AES are defined.
    """

    def generate_sbox_actions_for_round(self):
        list_of_sbox_actions = list()
        rounds_til_now = self.rounds - 1
        if self.orientation == 1:
            for i in range(16):
                first_element = int(self.A[i*8][1:])
                list_of_sbox_actions.append(SBoxAction(sbox=self.sboxes[first_element], input_start=first_element, cipher_instance=self, first_a_position_to_overwrite=first_element))
        else:
            pass
        return list_of_sbox_actions

    def generate_key_xor_actions_for_round(self):
        list_of_key_xor_actions = list()
        for var in range(self.plaintext_vars):
            list_of_key_xor_actions.append(XorAction((self.A[var], self.K[var]), self))
        return list_of_key_xor_actions

    def generate_shift_rows_actions_for_round(self):
        permutation = [0, 5, 10, 15,
                       4, 9, 14, 3,
                       8, 13, 2, 7,
                       12, 1, 6, 11]
        if self.orientation == 1:
            sub_permutations = [[(val * 8) + i for i in range(8)] for val in permutation]
            permutation = list()
            for sub_permutation in sub_permutations:
                permutation += sub_permutation
        print(permutation)
        list_of_permutation_actions = [PermutationAction(permutation, self)]
        return list_of_permutation_actions

    def generate_mix_columns_actions_for_round(self):
        list_of_mix_columns_actions = list()
        if self.orientation == 1:
            list_of_mix_columns_actions.append(OverwriteAction(list(range(16 * 8)), self))
            # TODO: Check for inequality for the mix columns operation. Is that doable without modulo?
            # byte_list_to_value = lambda byte_list: sum([bit * (2 ** bit_pos) for bit_pos,bit in enumerate(byte_list)])
            # for column_number in range(4):
            #     bit_vars_so_var = column_number * 4 * 8     # number columns * number bytes per column * bits per byte
            #     column = [[bit_number + bit_vars_so_var for bit_number in range(8)] for byte_number in range(4)]
            #     for byte in column:
            #         self.A[byte] = None

        else:
            list_of_mix_columns_actions.append(OverwriteAction(list(range(16)), self))
        return list_of_mix_columns_actions

    def run_round(self):
        print(f"Round {self.round_number} start")

        if self.round_number == 1:
            for keyaction in self.generate_key_xor_actions_for_round():
                keyaction.run_action()
            self.K = ['k' + str(self.round_number * self.key_vars + i) for i in range(self.key_vars)]

        for sboxaction in self.generate_sbox_actions_for_round():
            sboxaction.run_action()

        for shiftrowsaction in self.generate_shift_rows_actions_for_round():
            shiftrowsaction.run_action()

        for mixcolumnsaction in self.generate_mix_columns_actions_for_round():
            mixcolumnsaction.run_action()

        for keyaction in self.generate_key_xor_actions_for_round():
            keyaction.run_action()

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

        plaintextsize = 16 * 8
        keysize = 16 * 8

        if model_as_bit_oriented:
            super().__init__(rounds, plaintextsize, keysize, orientation=1)
        else:
            super().__init__(rounds, plaintextsize, keysize, orientation=8)

        self.cryptanalysis_type = 'differential'

        # Summary of what's happening in AES:

        #   determine xor output vars, dummy vars, and constraints
        if self.cryptanalysis_type == 'differential':
            xors_per_round = int(self.plaintext_vars)
            extra_xors = self.plaintext_vars
        elif self.cryptanalysis_type == 'linear':
            xors_per_round = 0
        else:
            xors_per_round = 0

        #   determine 3 way fork output vars, dummy vars, and constraints
        if self.cryptanalysis_type == 'differential':
            twf_per_round = 0
        else:  # self.cryptanalysis_type == 'linear':
            twf_per_round = int(0 / self.orientation)

        #   determine self.linear transformation output vars, dummy vars, and constraints
        lt_per_round = 0

        #   determine sbox output vars, dummy vars, and constraints
        if self.orientation == 1:
            # instantiating all SBoxes
            sbox_aes_subs = {index: value for index, value in
                             enumerate(
                                 [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130,
                                  201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38,
                                  54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5,
                                  154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59,
                                  214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74,
                                  76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
                                  81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12,
                                  19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34,
                                  42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194,
                                  211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244,
                                  234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75,
                                  189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
                                  225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161,
                                  137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22])}
            # with the list taken from https://github.com/pcaro90/Python-AES/blob/master/AES_base.py and not verified :)
            self.sbox = SBox(sbox_aes_subs, 8, 8)

            self.sboxes = [self.sbox] * 16

        overwrites = 16 * int(8/self.orientation)   # for the ColumnMix operations in AES where (as off Zhou) the
        # variables are just overwritten because otherwise it is too complex

        sbox_dummy_variables_per_round = self.calculate_vars_and_constraints(xors_per_round, twf_per_round,
                                                                             lt_per_round, extra_xors, overwrites, new_keys_every_round=True)

        # making sure we have at least one active sbox (minimizing active sboxes to zero is possible)
        if model_as_bit_oriented:
            sbox_dummy_variables = ["a" + str(i) for i in range(self.number_a_vars)]
        else:
            # this one is a bit tricky as the user has to determine which x variables pass through S-boxes
            sbox_dummy_variables = ["x" + str(i) for i in range(16, 16 * self.rounds)]

        for sbox_dummy in sbox_dummy_variables:
            self.M[self.M.get_shape()[0] - 1, self.V[sbox_dummy]] = 1
        self.M[self.M.get_shape()[0] - 1, self.V['constant']] = -1

        # adding a set to include the matrices of possible convex hull
        self.sbox_inequality_matrices = list()

        self.line = 0
        self.round_number = 1
        return
