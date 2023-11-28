from cipher.differential.gift import Gift64
from cipher.actions.overwriteaction import OverwriteAction


class Gift64(Gift64):
    """
    Class in which all functions for AES are defined.
    """

    def generate_equality_overwrite_actions(self):
        list_of_equality_overwrite_actions = list()
        set_of_xor_positions = set()
        set_of_single_bit_xor_positions = {3, 7, 11, 15, 19, 23, self.plaintextsize - 1}
        list_of_equality_overwrite_positions = set(range(self.plaintextsize)) - (
                set_of_xor_positions | set_of_single_bit_xor_positions)
        list_of_equality_overwrite_actions = [
            OverwriteAction(list_of_equality_overwrite_positions, cipher_instance=self, equality=True)]
        return list_of_equality_overwrite_actions

    def run_round(self):
        print(f"Round {self.round_number} start")

        for sboxaction in self.generate_sbox_actions_for_round():
            sboxaction.run_action()

        for permutationsaction in self.generate_permutation_actions_for_round():
            permutationsaction.run_action()

        for single_bit_xor_action in self.generate_single_bit_xor_actions():
            single_bit_xor_action.run_action()

        if self.overwrite_equals:
            for equality_overwrite_action in self.generate_equality_overwrite_actions():
                equality_overwrite_action.run_action()

        print(f"Round {self.round_number} end")
        self.round_number += 1
        return True

    def __init__(self, rounds=1, model_as_bit_oriented=True, type_of_modeling='SunEtAl 2013', **kwargs):
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
        super().__init__(rounds, model_as_bit_oriented=model_as_bit_oriented, cryptanalysis_type='linear',
                         type_of_modeling=type_of_modeling, **kwargs)
        return
