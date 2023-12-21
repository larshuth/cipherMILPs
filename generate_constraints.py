import numpy as np
from scipy.sparse import vstack


def generate_constraints(rounds, chosen_cipher, bit_oriented, chosen_type, **kwargs):
    """
    This function generates the constraint matrix for a number of rounds of a given cipher.

    Parameters:
    ----------
    rounds  :   int
                Number of rounds the cipher should go through

    cipher  :   class
                Cipher for which we generate the matrix

    Returns:
    -----------
    M       :   csr_matrix
                Generated constraint matrix for the MILP

    V       :   dictionary
                Mapping from variable name to index of corresponding column and vice versa.
    """
    cipher_instance = chosen_cipher(rounds, model_as_bit_oriented=bit_oriented, type_of_modeling=chosen_type, **kwargs)
    cipher_instance.round_number = 1
    for r in range(cipher_instance.rounds):
        cipher_instance.run_round()
    print("Created constraints")

    if cipher_instance.orientation == 1:
        cipher_instance.M = vstack([cipher_instance.M] + cipher_instance.sbox_inequality_matrices, dtype=float)
    print("Combined normal constraints and extra S-box constraints.")

    return cipher_instance


