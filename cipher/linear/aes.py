from cipher.differential.aes import Aes


class Aes(Aes):
    """
    So far, for Aes the MILP modelling of the linear cryptanalysis is made up of the same inequalities as the MILP
    modelling of its differential cryptanalysis
    """
    def run_round(self):
        print(f"Round {self.round_number} start")

        for sboxaction in self.generate_sbox_actions_for_round():
            sboxaction.run_action()

        for shiftrowsaction in self.generate_shift_rows_actions_for_round():
            shiftrowsaction.run_action()

        for mixcolumnsaction in self.generate_mix_columns_actions_for_round():
            mixcolumnsaction.run_action()

        self.K = ['k' + str(self.round_number * self.key_vars + i) for i in range(self.key_vars)]
        print(f"Round {self.round_number} end")
        self.round_number += 1
        return True

    def __init__(self, rounds=1, model_as_bit_oriented=False):
        super().__init__(rounds, model_as_bit_oriented, cryptanalysis_type='linear')
        return
