from cipher.differential.lblock import LBlock
from cipher.actions.permutationaction import PermutationAction
from cipher.actions.threeforkedbranchaction import ThreeForkedBranchAction
from cipher.actions.sboxaction import SBoxAction


class LBlock(LBlock):
    """
    Class in which all functions for LBlock cipher [Wu et al. 2011] are defined.
    """

    def calculate_output_vars_for_round(self):
        half_plaintext_vars = int(self.plaintext_vars / 2)
        permutation = self.get_permutation()

        list_of_output_vars = [0 for _ in range(half_plaintext_vars)]
        for index, position in enumerate(permutation):
            list_of_output_vars[index] = self.A[position + half_plaintext_vars]
        # given self.A as [0, ..., 31, 32, ..., 63]
        # we should get [36, 37, 38, 39, 44, 45, 46, 47, 32, 33, 34, 35, 40, 41, 42, 43, ...]
        return list_of_output_vars

    def generate_threeforkedbranch_actions_for_round(self, output_vars):
        list_of_threeforkedbranch_actions = list()
        half_plaintext_vars = int(self.plaintext_vars / 2)
        if self.orientation == 1:
            for i in range(half_plaintext_vars):
                list_of_threeforkedbranch_actions.append(
                    ThreeForkedBranchAction(input_var=self.A[i], cipher_instance=self,
                                            a_positions_to_overwrite=(i, None),
                                            linear_helper_positions_to_overwrite=(None, i),
                                            optional_output_vars=(None, None)))
        else:
            for i in range(half_plaintext_vars):
                list_of_threeforkedbranch_actions.append(
                    ThreeForkedBranchAction(input_var=self.A[i], cipher_instance=self,
                                            a_positions_to_overwrite=(None, i),
                                            linear_helper_positions_to_overwrite=(i, None),
                                            optional_output_vars=(None, output_vars[i]))
                )
        return list_of_threeforkedbranch_actions

    def generate_sbox_actions_for_round(self, output_vars):
        list_of_sbox_actions = list()
        if self.orientation == 1:
            for ith_sbox in range(8):
                sbox_outputs = tuple([output_vars[ith_sbox * 4 + bits] for bits in range(4)])
                sbox_input_vars = [self.A[ith_sbox * 4 + var] for var in range(self.sboxes[ith_sbox].in_bits)]
                list_of_sbox_actions.append(SBoxAction(sbox=self.sboxes[ith_sbox], input_vars=sbox_input_vars,
                                                       cipher_instance=self,
                                                       first_a_position_to_overwrite=4 * ith_sbox,
                                                       optional_output_vars=sbox_outputs))
        else:
            pass
        return list_of_sbox_actions

    def generate_bitshift_actions_for_round(self):
        list_of_bitshift_actions = list()
        start_first_half = 0
        end_first_half = int((self.plaintextsize / 2) / self.orientation)
        permutation = list(range(start_first_half, end_first_half))
        # permutation needs to span the whole A list, even if not all of them are changed
        # using the previously written code if just due to laziness
        block_size = int(4 / self.orientation)
        for index, shift in enumerate([+2] * 8):
            permutation += [((index + shift) * block_size + i) % (8 * block_size) + end_first_half for i in
                            range(block_size)]
        # this shifts the elements in self.A such that [0,1,2,3,4,5,6,7 ...] becomes [8,9,10,11,12,13,14,15 ...]
        list_of_bitshift_actions.append(PermutationAction(permutation, self))
        return list_of_bitshift_actions

    def run_round(self):
        # first we save the input vars as they will be needed later on
        x1_size = int((self.plaintextsize / 2) / self.orientation)

        # first we need to calculate the outputs of, depending on our orientation, 3-forked branched or sboxes
        for bitshift in self.generate_bitshift_actions_for_round():
            bitshift.run_action()

        output_vars = self.calculate_output_vars_for_round()

        # generate constraints and modify self.A to include all the values from 3-forked branches
        for threeforkedbranch_action in self.generate_threeforkedbranch_actions_for_round(output_vars):
            threeforkedbranch_action.run_action()

        # generate constraints and modify self.A to include all the values from s-boxes
        for sbox_action in self.generate_sbox_actions_for_round(output_vars):
            sbox_action.run_action()

        # renew the elements s.t. the first half of A, X_1 in the og paper,
        self.A[:x1_size] = self.linear_helper

        # and switch left and right
        self.A = self.A[x1_size:] + self.A[:x1_size]

        self.round_number += 1
        return True

    def __init__(self, rounds=32, model_as_bit_oriented=True, type_of_modeling='SunEtAl 2013', **kwargs):
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
        super().__init__(rounds, model_as_bit_oriented, cryptanalysis_type="linear", type_of_modeling=type_of_modeling,
                         lin_args=kwargs)

        self.linear_helper = [None for _ in range(int(self.plaintext_vars / 2))]
        return
