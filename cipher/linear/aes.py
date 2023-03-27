from cipher.differential.aes import *


class AesLin(Aes):
    """
    So far, for Aes the MILP modelling of the linear cryptanalysis is made up of the same inequalities as the MILP
    modelling of its differential cryptanalysis
    """
    def __init__(self, rounds=1):
        super().__init__(rounds)
        return
