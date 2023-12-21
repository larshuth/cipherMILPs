import generate_constraints as gc
import sorting_functions as sf

import pickle
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt  # noqa
import matplotlib.pylab as pylab
from pylatex import Document, Section, Figure, NoEscape, NewPage, Matrix, Math, Alignat, Command, Subsection

from cipher.differential.aes import Aes as AesDifferential
from cipher.differential.lblock import LBlock as LBlockDifferential
from cipher.differential.gift import Gift64 as Gift64Differential
from cipher.linear.aes import Aes as AesLinear
from cipher.linear.lblock import LBlock as LBlockLinear
from cipher.linear.gift import Gift64 as Gift64Linear

plt.rcParams.update({'font.size': 5})

GOAL = 'tetrisfold'


def rearrange(cipher, matrix, variables, cipher_instance=None, chosen_type='Baksi 2020', **kwargs):
    """
    Quick visualization with zooming-in-ability, opens a new window and doesn't generate a pdf.
    Generates 4 visualizations of the same sparse matrix.

    Parameters:
    -----------
    rounds  :   int
                number of rounds

    cipher  :   A python class from the cipher/linear or cipher/differential folder
                class of the cipher type and analysis which is to be performed
    """

    rounds = cipher_instance.rounds

    if cipher == AesDifferential:
        matrix, variables = sf.tetrisfold_linear_aes_k_round(matrix, variables, k=rounds, **kwargs)
    elif cipher == AesLinear:
        matrix, variables = sf.tetrisfold_differential_aes_k_round(matrix, variables, k=rounds, **kwargs)
    elif cipher == LBlockDifferential:
        if GOAL == 'tetrisfold':
            matrix, variables = sf.tetrisfold_differential_LBlock_k_rounds(matrix, variables, k=rounds, **kwargs)
        else:
            if chosen_type == 'Baksi 2020':
                matrix, variables = sf.two_stage_differential_LBlock_k_rounds(matrix, variables, k=rounds, **kwargs)
            else:
                matrix, variables = sf.n_fold_differential_LBlock_k_rounds(matrix, variables, k=rounds, **kwargs)
    elif cipher == LBlockLinear:
        matrix, variables = sf.tetrisfold_linear_LBlock_k_rounds(matrix, variables, k=rounds, **kwargs)
    elif cipher == Gift64Differential:
        matrix, variables = sf.tetrisfold_differential_gift64_k_round(matrix, variables, k=rounds, **kwargs)
    elif cipher == Gift64Linear:
        matrix, variables = sf.tetrisfold_linear_gift64_k_round(matrix, variables, k=rounds, **kwargs)
    else:
        raise Exception('This type of cipher-cryptanalysis does not have a sorting function yet')

    columns = matrix.get_shape()[1]
    rows = matrix.get_shape()[0]
    fig = pylab.figure(figsize=(columns * 0.01, rows * 0.01))
    df = DataFrame(matrix.toarray())

    df = df.astype("bool")
    df = df.astype("float")
    # print(df)

    pylab.figimage(df, cmap='binary', origin='upper')
    return fig


def remove_zeros(matrix, variables: dict):
    colsnonzero = []
    rowsnonzero = []

    print('remove columns')
    # remove zero columns
    matrix.tocsc()
    for i in range(matrix.get_shape()[1]):
        if matrix.getcol(i).count_nonzero() != 0:
            colsnonzero.append(i)
    matrix = matrix[:, np.array(colsnonzero)]

    print('remove rows')
    matrix.tocsr()
    for i in range(matrix.get_shape()[0]):
        if matrix.getrow(i).count_nonzero() != 0:
            rowsnonzero.append(i)
    matrix = matrix[np.array(rowsnonzero), :]

    # remove zero row numbers from variables and mend remaining numbers
    variables_as_list = [(key, val) for key, val in variables.items()]
    variables_pos_to_var = list(filter(lambda pair: type(pair[0]) == int, variables_as_list))
    variables_var_to_pos = list(filter(lambda pair: type(pair[1]) == int, variables_as_list))

    variables_pos_to_var.sort(key=lambda pair: pair[0])
    variables_var_to_pos.sort(key=lambda pair: pair[1])

    print("rewrite variables")
    remove_counter = 0
    new_variables = dict()
    print(list(zip(variables_pos_to_var, variables_var_to_pos)))
    for pos_to_var, var_to_pos in zip(variables_pos_to_var, variables_var_to_pos):
        if pos_to_var[0] != var_to_pos[1]:
            raise Exception(f'Something is wrong, {pos_to_var} and {var_to_pos} should be the same.')
        if pos_to_var[0] not in colsnonzero:
            remove_counter += 1
        else:
            new_variables[pos_to_var[0] - remove_counter] = pos_to_var[1]
            new_variables[var_to_pos[0]] = var_to_pos[1] - remove_counter
    return matrix, new_variables


def invert_matrix(matrix, variables, horizontal=True, vertical=True):
    print("flip column order")
    # flip column order

    if horizontal:
        reversed_column_indices = list(range(matrix.get_shape()[1], -1, -1))
        matrix = sf.permutate_columns(matrix, reversed_column_indices)

        variables_as_list = [(key, val) for key, val in variables.items()]

        variables_pos_to_var = list(filter(lambda pair: type(pair[0]) == int, variables_as_list))
        variables_var_to_pos = list(filter(lambda pair: type(pair[1]) == int, variables_as_list))

        variables_pos_to_var.sort(key=lambda pair: pair[0])
        variables_var_to_pos.sort(key=lambda pair: pair[1])

        number_of_vars = len(variables_var_to_pos)
        reverse = lambda x: (number_of_vars - 1) - x

        reveresed_variables = dict()
        print(list(zip(variables_pos_to_var, variables_var_to_pos)))
        for pos_to_var, var_to_pos in zip(variables_pos_to_var, variables_var_to_pos):
            if pos_to_var[0] != var_to_pos[1]:
                raise Exception(f'Something is wrong, {pos_to_var} and {var_to_pos} should be the same.')
            else:
                reveresed_variables[reverse(pos_to_var[0])] = pos_to_var[1]
                reveresed_variables[var_to_pos[0]] = reverse(var_to_pos[1])

        variables = reveresed_variables

    print("flip row order")
    # flip row order
    if vertical:
        reversed_row_indices = list(range(matrix.get_shape()[0] - 1, -1, -1))
        matrix = sf.permutate_rows(matrix, reversed_row_indices)
    return matrix, variables


def matplotlibvis(filename, cipher, matrix, variables, cipher_instance=None, chosen_type='Baksi 2020', **kwargs):
    """
    Quick visualization with zooming-in-ability, opens a new window and doesn't generate a pdf.
    Generates 4 visualizations of the same sparse matrix.

    Parameters:
    -----------
    rounds  :   int
                number of rounds

    cipher  :   class
                class of the wanted cipher
    """

    columns = cipher_instance.M.get_shape()[1]
    rows = cipher_instance.M.get_shape()[0]
    fig = pylab.figure(figsize=(columns * 0.01, rows * 0.01))
    df = DataFrame(cipher_instance.M.toarray())

    df = df.astype("bool")
    df = df.astype("float")

    pylab.figimage(df, cmap='binary', origin='upper')
    return fig


def matrix_to_latex_nonzero(A):
    """
    Generates the latex code for a csr_matrix while displaying only the nonzero values.
    (Can I optimize this? Currently going through every element(also nonzero))
    Parameters:
    ----------
    A       :   scr_matrix
                Sparse matrix that we want to display in a latex file

    Returns:
    ----------
    matri   :   string 
                Code for displaying the matrix
    """
    A = A.toarray()
    matri = "\\begin{pmatrix}%\n"
    for i in range(len(A)):
        for j in range(len(A[i])):
            if j != 0:
                matri += "&"
            if A[i][j] != 0:
                matri += str(A[i][j])
        matri += "\\\ \n"
    matri += "\end{pmatrix}%\n"
    return matri


def vectormilp(V):
    """
    Generates the code for the vector in the MILP.

    Parameters:
    ----------
    V       :   list
                List with all variablenames that we want to display in a latex file as a vector

    Returns:
    ----------
    vec     :   string 
                Code for displaying the vector
    """
    vec = "\n \\begin{pmatrix}%\n"
    for i in V:
        vec = vec + i[0] + "_{" + i[1:] + "}\\\ \n"
    vec += "\end{pmatrix}%\n"
    return vec


def constraints(A, V):
    """
    Generates a string with every constraint (in Latexschreibweise).

    Parameters:
    ----------
    A       :   scr_matrix
                Sparse matrix that we want to multiply with the variablenames list

    V       :   list    
                Variablenames in a list, transposing this we get the vector to multiply the matrix with

    Returns:
    ----------
    cons    :   list of strings 
                Every element is the latexcode for the corresponding constraint
    """
    cons = []
    linebreak = 0
    for i in range(A.get_shape()[0]):
        if i == A.get_shape()[0]:
            linebreak = 1
        # getting the indices of the nonzero elements
        positions = A.getrow(i).nonzero()[1]
        con = ""
        for e in positions:
            if (linebreak == 0 and np.where(positions == e)[0][0] % 10 != 0) or np.where(positions == e)[0][0] == 0:
                con = con + str(A[i, e]) + V[e][0] + "_{" + V[e][1:] + "}+"
            else:
                con = con + str(A[i, e]) + V[e][0] + "_{" + V[e][1:] + "}+\\\\"

        # remove the last +
        if con[-4:] == "\\\\":
            con = con[:-5]
        else:
            con = con[:-1]
        con = con.replace("1x", "x")
        con = con.replace("1d", "d")
        con = con.replace("+-", "-")
        con += " \geq 0"

        # having -1 instead of -11 in the last constraint (idea: in V "s" anstatt "1" adden und das dann eliminieren)
        con = con.replace("-11", "-1")
        cons.append(con)
    return cons


def generate_constraints_as_text():
    """
    Generates the code for latex and generates the pdf.

    """

    constraints = list()
    for constraint in
    doc.append(NewPage())
    with doc.create(Section("Constraints")):
        B = constraints(A, V)
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            for i in B:
                agn.append(i + "\\\\")

    doc.generate_pdf(clean_tex=False)
