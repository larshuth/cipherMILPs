import numpy as np
from scipy.sparse import csr_matrix, lil_matrix, vstack
import cipher as cip
import pickle
import cipher


def removezerocols(M, V):
    """
    Removes all Columns that have no non-zero value.

    Parameters:
    ---------
    M:  csr_matrix
        Matrix where the Columns will be deleted

    V:  list
        List of all variable names. Also vector with which the matrix will be multiplied for the MILP

    Returns:
    --------
    M:  csr_matrix
        New matrix that has only columns with an non zero entry.

    V:  list
        List of all variable names. Also vector with which the matrix will be multiplied for the MILP
    """
    colszero = []
    newV = []
    M.tocsc()
    for i in range(M.get_shape()[1]):
        if M.getcol(i).count_nonzero() != 0:
            colszero.append(i)
            newV.append(V[i])
    colszero = np.array(colszero)
    M = M[:, colszero]
    return M


def new_generate_constraints(rounds, cipher):
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

    V       :   list
                List that constrains the variables. When multiplying the matrix with this
                list one gets the constraints.
    """
    cipher_instance = cipher(rounds)
    cipher_instance.round_number = 1
    for r in range(cipher_instance.rounds):
        print(cipher_instance.round_number)
        cipher_instance.shift_before()
        for cipher_action in cipher_instance.generate_actions_for_round():
            line = cipher_instance.gen_long_constraint(cipher_action)
            # TODO: figure out how to add generate_smallconstraints from Aes, Enocoro, and EnocoroLin to the class
            # line = generate_smallconstraints(cipher_instance, line)
        cipher_instance.shift_after()

    if cipher_instance.orientation == 1:
        cipher_instance.M = vstack([cipher_instance.M] + cipher_instance.sbox_inequality_matrices, dtype=int)

    cipher_instance.M = cipher_instance.M.tocsr()
    cipher_instance.M = removezerocols(cipher_instance.M, cipher_instance.V)
    return cipher_instance
