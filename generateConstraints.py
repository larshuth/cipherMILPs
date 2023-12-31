import numpy as np
from scipy.sparse import vstack


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


def removezerorows(matrix):
    """
    Removes all rows that have no non-zero value.

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
    matrix = matrix.tocsr()
    print(matrix.get_shape())
    nonzero_row_indice, _ = matrix.nonzero()
    unique_nonzero_indice = np.unique(nonzero_row_indice)
    matrix = matrix[unique_nonzero_indice]
    # this return might not be necessary as the matrix should be call by reference
    return matrix


def new_generate_constraints(rounds, chosen_cipher, bit_oriented, chosen_type, **kwargs):
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
    cipher_instance = chosen_cipher(rounds, model_as_bit_oriented=bit_oriented, type_of_modeling=chosen_type, **kwargs)
    cipher_instance.round_number = 1
    for r in range(cipher_instance.rounds):
        cipher_instance.run_round()
    print("Created constraints")

    if cipher_instance.orientation == 1:
        cipher_instance.M = vstack([cipher_instance.M] + cipher_instance.sbox_inequality_matrices, dtype=float)
    print("Combined normal constraints and extra S-box constraints.")

    cipher_instance.M = removezerorows(cipher_instance.M)
    # cipher_instance.M = cipher_instance.M.tocsr()
    return cipher_instance
