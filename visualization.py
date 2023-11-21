import scipy.sparse

import generateConstraints as gc
import sortingFunctions as sf
import cipher as cip
import numpy as np
from pylatex import Document, Section, Figure, NoEscape, NewPage, Matrix, Math, Alignat, Command, Subsection
# matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib as mpl
import matplotlib.pyplot as plt  # noqa
import matplotlib.pylab as pylab
import pickle
from pandas import DataFrame
import os.path
from cipher.differential.aes import Aes as AesDifferential
from cipher.differential.lblock import LBlock as LBlockDifferential
from cipher.differential.gift import Gift64 as Gift64Differential
from cipher.linear.aes import Aes as AesLinear
from cipher.linear.lblock import LBlock as LBlockLinear
from cipher.linear.gift import Gift64 as Gift64Linear


plt.rcParams.update({'font.size': 5})


def rearrange(rounds, cipher, bit_oriented, chosen_type, **kwargs):
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
    title = [str(cipher)[15:-2], str(rounds)]
    filename = f'{title[0]}{title[1]}rounds_bitoriented_{str(bit_oriented)}_{chosen_type.replace(" ", "")}'
    filename += ''.join([f'{key}_{val}' for key, val in kwargs.items()])

    if os.path.isfile(f'{filename}_matrix.pkl') and os.path.isfile(f'{filename}_variables.pkl'):
        file = open(f'{filename}_matrix.pkl', 'rb')
        matrix = pickle.load(file)
        file.close()

        file = open(f'{filename}_variables.pkl', 'rb')
        variables = pickle.load(file)
        file.close()
    else:
        cipher_instance = gc.new_generate_constraints(rounds, cipher, bit_oriented, chosen_type, **kwargs)
        matrix = cipher_instance.M
        variables = cipher_instance.V

        file = open(f'{filename}_matrix.pkl', 'wb')
        pickle.dump(cipher_instance.M.copy(), file)
        file.close()

        file = open(f'{filename}_variables.pkl', 'wb')
        pickle.dump(cipher_instance.V.copy(), file)
        file.close()

    print(matrix.get_shape()[0], matrix.get_shape()[1])

    if cipher == AesDifferential:
        matrix, variables = sf.tetrisfold_linear_aes_k_round(matrix, variables, k=rounds, **kwargs)
    elif cipher == AesLinear:
        matrix, variables = sf.tetrisfold_differential_aes_k_round(matrix, variables, k=rounds, **kwargs)
    elif cipher == LBlockDifferential:
        matrix, variables = sf.tetrisfold_differential_LBlock_k_rounds(matrix, variables, k=rounds, **kwargs)

        # if chosen_type == 'Baksi 2020':
        #     matrix, variables = sf.two_stage_differential_LBlock_k_rounds(matrix, variables, k=rounds, **kwargs)
        # else:
        #     matrix, variables = sf.n_fold_differential_LBlock_k_rounds(matrix, variables, k=rounds, **kwargs)

    elif cipher == Gift64Differential:
        matrix, variables = sf.tetrisfold_differential_gift64_k_round(matrix, variables, k=rounds, **kwargs)

    columns = matrix.get_shape()[1]
    rows = matrix.get_shape()[0]
    fig = pylab.figure(figsize=(columns * 0.01, rows * 0.01))
    df = DataFrame(matrix.toarray())

    df = df.astype("bool")
    df = df.astype("float")
    # print(df)

    pylab.figimage(df, cmap='binary', origin='upper')
    fig.savefig(f"{filename}_sorted.png")

    plt.show()
    print("plot should have been shown")
    return


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


def matplotlibvis(rounds, cipher, bit_oriented, chosen_type, **kwargs):
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
    title = [str(cipher)[15:-2], str(rounds)]
    filename = f'{title[0]}{title[1]}rounds_bitoriented_{str(bit_oriented)}_{chosen_type.replace(" ", "")}'
    filename += ''.join([f'{key}_{val}' for key, val in kwargs.items()])

    fig, axs = plt.subplots(1, 4)
    fig.canvas.manager.set_window_title(
        'Mit schönen Farben vom Meer damit es für Leo wie Heimat ist (weil Nordsee und so)')
    ax1 = axs[0]
    ax2 = axs[1]
    ax3 = axs[2]
    ax4 = axs[3]

    cipher_instance = gc.new_generate_constraints(rounds, cipher, bit_oriented, chosen_type, **kwargs)

    columns = cipher_instance.M.get_shape()[1]
    rows = cipher_instance.M.get_shape()[0]
    fig = pylab.figure(figsize=(columns * 0.01, rows * 0.01))
    df = DataFrame(cipher_instance.M.toarray())
    # s = df.select_dtypes(include='object').columns
    # print(s)
    df = df.astype("bool")
    df = df.astype("float")
    # print(df)

    pylab.figimage(df, cmap='binary', origin='upper')
    fig.savefig(f"{filename}.png")

    file = open(f'{filename}_matrix.pkl', 'wb')
    pickle.dump(cipher_instance.M.copy(), file)
    file.close()

    file = open(f'{filename}_variables.pkl', 'wb')
    pickle.dump(cipher_instance.V.copy(), file)
    file.close()

    if False:
        A = cipher_instance.M.copy()
        sf.d_var_to_beginning(cipher_instance)
        M = cipher_instance.M.copy()
        sf.long_constraints_to_top(cipher_instance)
        B = cipher_instance.M.copy()
        # sf.create_fourblock(cipher_instance)
        C = cipher_instance.M

        axs[0].set_title('native')
        axs[1].set_title('d_variables to the beginning')
        axs[2].set_title('long constraints to the top')
        axs[3].set_title('creating 4-block')

        ax1.spy(A, markersize=1, color="teal")
        ax2.spy(M, markersize=1, color="steelblue")
        ax3.spy(B, markersize=1, color="mediumturquoise")
        ax4.spy(C, markersize=1, color="skyblue")

    plt.show()
    print("plot should have been shown")
    return


def matplot_scatterplot():
    """
    https://stackoverflow.com/questions/24013962/how-to-draw-a-matrix-sparsity-pattern-with-color-code-in-python
    Function that visualizes not only the structure of the matrix but also the different values.
    Not sure if it could be useful in the future.
    """
    A, V = gc.new_generate_constraints(5, cip.Aes)
    A, V = sf.create_fourblock(A, V)
    A = sf.block_structure(A, V)
    mat = A.toarray()

    fig, ax = plt.subplots(figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')

    # prepare x and y for scatter plot
    plot_list = []
    for rows, cols in zip(np.where(mat != 0)[0], np.where(mat != 0)[1]):
        plot_list.append([cols, rows, mat[rows, cols]])
    plot_list = np.array(plot_list)

    # scatter plot with color bar, with rows on y axis
    plt.scatter(plot_list[:, 0], plot_list[:, 1], c=plot_list[:, 2], s=50)
    cb = plt.colorbar()

    # full range for x and y axes
    plt.xlim(0, mat.shape[1])
    plt.ylim(0, mat.shape[0])
    # invert y axis to make it similar to imshow
    plt.gca().invert_yaxis()

    plt.show()


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


def mainly(fname, A, V, title, *args, **kwargs):
    """
    Generates the code for latex and generates the pdf.

    """
    geometry_options = {"right": "2cm", "left": "2cm"}
    doc = Document(fname, geometry_options=geometry_options)
    doc.preamble.append(Command("usepackage{amsmath}"))
    doc.preamble.append(Command("allowdisplaybreaks"))
    doc.preamble.append(Command("textwidth15cm"))
    doc.preamble.append(Command("usepackage[labelformat=empty]{caption}"))
    doc.preamble.append(NoEscape("\setcounter{MaxMatrixCols}{10000}"))
    doc.preamble.append(NoEscape("\setlength{\headsep}{10pt}"))
    doc.preamble.append(NoEscape("\setlength{\\textheight}{650pt}"))
    doc.append(NoEscape("\setlength{\\voffset}{-0.50in}"))
    with doc.create(Section("Matrix Structure " + title[0] + ", " + title[1] + " rounds")):
        with doc.create(Figure(position='h!p')) as plot:
            plot.add_plot(width=460, *args, **kwargs)

    # Unfortunately creating the matrix does not work with bigger rounds
    """doc.append(NewPage())
    with doc.create(Section("MILP")): 
        doc.append(NoEscape("\[\\resizebox{\linewidth}{!}{%\n" + matrix_to_latex_nonzero(A)+vectormilp(V)+"}\n\geq 0\]"))
    """
    doc.append(NewPage())
    with doc.create(Section("Constraints")):
        B = constraints(A, V)
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            for i in B:
                agn.append(i + "\\\\")

    doc.generate_pdf(clean_tex=False)


def gen_pdf(rounds, cipher, bit_oriented, chosen_type, **kwargs):
    """
    Generates the plots in matplotlib and calls the function to generate the pdf.

    Parameters:
    -----------
    rounds  :   int
                Number of rounds
    
    cipher  :   class
                Class of the wanted cipher
    """
    fig, axs = plt.subplots(2, 2, figsize=(6, 8))
    ax1 = axs[0][0]
    ax2 = axs[0][1]
    ax3 = axs[1][0]
    ax4 = axs[1][1]

    cipher_instance = gc.new_generate_constraints(rounds, cipher, bit_oriented, chosen_type, **kwargs)
    A = cipher_instance.M.copy()
    print(cipher_instance.M.get_shape())
    # sf.d_var_to_beginning(cipher_instance)
    M = cipher_instance.M.copy()
    print(cipher_instance.M.get_shape())
    # sf.long_constraints_to_top(cipher_instance)
    B = cipher_instance.M.copy()
    print(cipher_instance.M.get_shape())
    # sf.create_fourblock(cipher_instance)
    C = cipher_instance.M

    ax1.set_title('native')
    ax2.set_title('d_variables to the left')
    ax3.set_title('long constraints to the top')
    ax4.set_title('creating 4-block')

    ax1.spy(A, markersize=1, color="teal")
    ax2.spy(M, markersize=1, color="steelblue")
    ax3.spy(B, markersize=1, color="mediumturquoise")
    ax4.spy(C, markersize=1, color="skyblue")

    title = [str(cipher)[15:-2], str(rounds)]
    print(type(A))
    print("lala")  # r'1\textwidth',
    mainly(f'{title[0]}{title[1]}rounds_bitoriented_{str(bit_oriented)}_{chosen_type.replace(" ", "")}', A=A, V=cipher_instance.V, title=title,
           dpi=300)


def no_viz_just_testrun(rounds, cipher, bit_oriented, chosen_type, **kwargs):
    """
    Generates the plots in matplotlib and calls the function to generate the pdf.

    Parameters:
    -----------
    rounds  :   int
                Number of rounds

    cipher  :   class
                Class of the wanted cipher
    """
    gc.new_generate_constraints(rounds, cipher, bit_oriented, chosen_type, **kwargs)
    return True
