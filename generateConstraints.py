import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
import cipher as cip


def generate_smallconstraints(M, line):
    """
    Generates all the constraint-inequalities that consist of a dummy and a x- variable.
    Those constraints follow after a constraint that models going through a path in a cipher,
    and they just indicate that if a x-variable is 1, then the dummy variable is also 1 and the path
    is active.

    Parameters:
    ----------
    M       :   lil_matrix
                The matrix in which all the constraints are saved

    line    :   int
                The index of the row from which we want to generate the remaining constraints


    Returns:
    ----------
    M       :   scr_matrix
                The matrix with all new constraints in it

    line    :   int
                Index of the row that we last filled in

    """
    dummyIndex = np.where((M.getrow(line).toarray()[0] != 0) & (M.getrow(line).toarray()[0] != 1))[0][0]
    for ind in np.where(M.getrow(line).toarray()[0] == 1)[0]:
        line += 1
        M[line, ind] = -1
        M[line, dummyIndex] = 1
    return M, line


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
    return M, newV


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
    line = 0
    A, M, V, next = cipher.initialize(rounds)
    for r in range(rounds):
        A = cipher.shift_before(A)
        S = [0, 0, 0, 0]
        for j in cipher.rangenumber(A):
            A, M, V, line, next, S = cipher.gen_long_constraint(A, M, V, line, next, r, j, S)
            M, line = generate_smallconstraints(M, line)
            line += 1
        A = cipher.shift_after(A)
    M = M.tocsr()
    V.append("1")
    M, V = removezerocols(M, V)
    return M, V
