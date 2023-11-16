import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from itertools import chain


# https://stackoverflow.com/questions/28334719/swap-rows-csr-matrix-scipy

def permutate_rows(x, idenRows):
    """
    This function permutates the rows in the order that is given.

    Parameters:
    ---------
    H       :   csr_matrix
                Matrix which rows are going to be permutated

    indenRows:  list
                Order of rows how they should be (was ist das für ein Satz?!)

    Returns:
    --------
    H       :   csr_matrix
                Matrix with permutated rows
    """
    x = x.tocoo()
    idenRows = np.argsort(idenRows)
    idenRows = np.asarray(idenRows, dtype=x.row.dtype)
    x.row = idenRows[x.row]
    return x


def permutate_columns(x, idenCols):
    """
    This function permutates the columns in the order that is given.

    Parameters:
    ---------
    H       :   csr_matrix
                Matrix which columns are going to be permutated

    indenRows:  list
                Order of columns how they should be (was ist das für ein Satz?!)

    Returns:
    --------
    H       :   csr_matrix
                Matrix with permutated columns
    """
    x = x.tocoo()
    idenCols = np.argsort(idenCols)
    idenCols = np.asarray(idenCols, dtype=x.col.dtype)
    x.col = idenCols[x.col]
    return x


def long_constraints_to_top(cipher_instance):
    """
    This function permutates the rows(constraints) in a way such that the constraints with
    a lot nonzero entries are at the top. This way one could form a block at the top.
    This function could be optimized (especially for Enocoro)

    Parameters:
    --------
    M:  csr_matrix
        Matrix that will be permutated

    Returns:
    --------
    M:  csr_matrix
        Permutated matrix
        """
    dic = {}
    for i in range(cipher_instance.M.get_shape()[0]):
        dic[i] = cipher_instance.M.getrow(i).count_nonzero()
    dic2 = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
    sortedrows = list(dic2.keys())
    cipher_instance.M = permutate_rows(cipher_instance.M, sortedrows)
    return


def full_columns_begin(M):
    """
    This function permutates the columns in a way such that the columns with
    a lot nonzero entries are at the beginning(left part).

    Parameters:
    --------
    M:  csr_matrix
        Matrix that will be permutated

    Returns:
    --------
    M:  csr_matrix
        Permutated matrix
        """
    dic = {}
    for i in range(M.get_shape()[1]):
        dic[i] = M.getcol(i).count_nonzero()
    dic2 = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
    sortedcols = list(dic2.keys())
    M = permutate_columns(M, sortedcols)
    return M


def d_var_to_beginning(cipher_instance):
    """
    This function permutates the columns such that all the dummy variables are at the beginning, and then the
    x variables follow. And the variable for the added constraint goes to the beginnign

    Parameters:
    --------
    M   :   csr_matrix
            Matrix that will be permutated

    V   :   list
            List of all variable names. Also vector with which the matrix will be multiplied for the MILP

    Returns:
    --------
    M   :   csr_matrix
            Permutated matrix

    newV:   list
            List of all variable names. Also vector with which the matrix will be multiplied for the MILP
    """
    pos_first_d_var = cipher_instance.number_x_vars
    number_d_vars = cipher_instance.number_dx_vars + cipher_instance.number_dt_vars + cipher_instance.number_dl_vars
    sorted_indices = list(range(pos_first_d_var, pos_first_d_var + number_d_vars)) + list(
        range(pos_first_d_var)) + list(
        range(pos_first_d_var + number_d_vars, cipher_instance.M.get_shape()[1]))

    for key, value in cipher_instance.V.items():
        try:
            if key[0] in {'dx', 'dt', 'dl'}:
                cipher_instance.V[key] -= pos_first_d_var
            elif key[0] == 'x':
                cipher_instance.V[key] += (pos_first_d_var - cipher_instance.number_d_vars)
        except TypeError:
            pass

    cipher_instance.M = permutate_columns(cipher_instance.M, sorted_indices)
    return


def creating_diagonal_in4block(cipher_instance):
    """
    This function permutates the rows of the matrix, but not the ones in the block at the top.
    They are permutated in a way such that a diagonal will appear alongisde an vertical block on the left.

    Parameters:
    --------
    M:  csr_matrix
        Matrix that will be permutated

    V:  list
        List of all variable names. Also vector with which the matrix will be multiplied for the MILP

    Returns:
    --------
    M:  csr_matrix
        Permutated matrix

    V:  list
        List of all variable names. Also vector with which the matrix will be multiplied for the MILP
    """
    dic = {}
    # count how many dummy variables there are. This is so that we only permutate the rows in the diagonal
    for i in range(cipher_instance.M.get_shape()[0]):
        if i >= cipher_instance.number_d_vars:
            dic[i] = cipher_instance.M.getrow(i).nonzero()[1][1]
    dic2 = dict(sorted(dic.items(), key=lambda x: x[1], reverse=False))
    sortedrows = list(dic2.keys())
    beginofrows = [i for i in range(cipher_instance.number_d_vars)]
    sortedrows = beginofrows + sortedrows
    cipher_instance.M = permutate_rows(cipher_instance.M, sortedrows)
    return


def create_fourblock(cipher_instance):
    """
    Creates a four-block structure in the given matrix.

    Parameters:
    ---------
    M:  csr_matrix
        Matrix that will be permutated

    V:  list
        List of all variable names. Also vector with which the matrix will be multiplied for the MILP

    Returns:
    --------
    M:  csr_matrix
        Permutated matrix
    """
    d_var_to_beginning(cipher_instance)
    long_constraints_to_top(cipher_instance)
    creating_diagonal_in4block(cipher_instance)
    return


def changedvar(M, V):
    """
    changes the columns of the d-variables in order to get a better structure (does not work)
    """
    dic = {}
    # count how many dummy variables there are. This is so that we only permutate the rows in the diagonal
    count = 0  # begins at 1 because of the constraint that ensures that there is one active sbox
    for e in V:
        if e[0] != "x":
            count += 1
    M = M.tocsc()
    for i in range(M.get_shape()[1]):
        if i < count and i != 0:
            dic[i] = list(M.getcol(i).nonzero()[0])[0]
            # hier letzte Zahl ändern und .inke spalte wird anders sortiert
            print(M.getcol(i).nonzero())
    dic2 = dict(sorted(dic.items(), key=lambda x: x[1], reverse=False))
    sortedrows = [0] + list(dic2.keys())
    beginofrows = [i for i in range(count, M.get_shape()[1])]
    sortedrows = sortedrows + beginofrows
    M = permutate_columns(M, sortedrows)
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    im = plt.imshow(data2D, cmap="GnBu_r")
    plt.colorbar(im)
    # plt.plot([i for i in range(M.get_shape()[1])],[count-0.5 for i in range(M.get_shape()[1])],linewidth = 0.5)

    # vertikale striche
    leng = (M.get_shape()[1]) - 17 - count
    leng / 16
    # for e in range(int(teil)+2):
    # plt.plot([count+16*e-0.5 for i in range(M.get_shape()[0])],[i for i in range(M.get_shape()[0])],linewidth = 0.5)

    # horizontale linien
    leng2 = (M.get_shape()[0]) - 1 - count
    leng2 / 32
    # for e in range(int(teil2)+1):
    # plt.plot([i for i in range(M.get_shape()[1])],[count+16+32*e-0.5 for i in range(M.get_shape()[1])],linewidth = 0.5)
    # plt.show()
    return M
    # idee: da wo die diagonale gemacht wird die sachen die auf der gleichen höhe sind so lassen und nicht tauschen nach dem ersten element


def block_structure(M, V):
    """
    parameter:
    m   csr_matrix
    This function should create multiple blocks for the matrix
    NOT FINISHED
    """
    # idee: oberer block hat Länge Anzahl(lange constraints)+1
    count = 0
    for e in V:
        if e[0] == "d":
            count += 1
        else:
            break
    ind = [i for i in range(count)]
    out1 = M.tocsc()[:, ind]
    out1.tocsr()[ind, :]
    # Block C (tc) has to be AT LEAST this big

    # jetzt: wie höhe von Block A und B bestimmen? eig nur rundenanzahl aber wie findet man die raus?
    # vllt einfach alle langen constraints nehmen, also ab wenn weniger sachen in constraints sind.
    # liste die zählt wie viele constraints in jeder row sind? und dann gucken wann die größte abstufung ist?
    # alles was mehr als 2 in der reihe hat ist nicht mehr in den oberen blöcken drin
    numofvarinrow = []
    print(M.count_nonzero())
    for i in range(M.get_shape()[0]):
        numofvarinrow.append(len(list(M.getrow(i).nonzero()[1])))
    print(numofvarinrow)
    a = np.array(numofvarinrow)
    num = (np.where(a == 2)[0][0])  # row of first constraint that contains 2 elements
    sc = num - 0.5
    M.toarray()
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    im = plt.imshow(data2D, cmap="GnBu_r")
    plt.colorbar(im)
    plt.plot([i for i in range(M.get_shape()[1])], [sc for i in range(M.get_shape()[1])])
    plt.plot([count for i in range(int(sc + 0.5))], [i for i in range(int(sc + 0.5))])
    plt.show()


def twodiag(M, V):
    """
    Changes the diagonal that consists of two variables on top of each other into two diagonals that have only one line
    """
    count = 0  # begins at 1 because of the constraint that ensures that there is one active sbox
    oldorder = []
    for i in range(M.get_shape()[0]):
        oldorder.append(i)
    for e in V:
        if e[0] == "d":
            count += 1
    neworder = []
    for i in range(count + 17):
        neworder.append(i)
    leng2 = (M.get_shape()[0]) - 1 - count
    teil2 = leng2 / 32
    for e in range(int(teil2) - 1):
        for i in range(count + 17 + 32 * e, count + 17 + 32 * (e + 1)):
            if i % 2 == 1:
                neworder.append(i)
        for i in range(count + 17 + 32 * e, count + 17 + 32 * (e + 1)):
            if i % 2 == 0:
                neworder.append(i)
    for i in range(16, 0, -1):
        neworder.append(M.get_shape()[0] - i)
    C = permutate_rows(M, neworder)
    return C


def changediag(M, V):
    """
    Changes the columns of the diagonal (the A-blocks) so that the columns with the most non-zero values
    are at the beginning.
    """
    dic = {}
    count = 0
    for e in V:
        if e[0] != "x":
            count += 1
    M.tocsc()
    for i in range(count, M.get_shape()[1]):
        dic[i] = M.getcol(i).count_nonzero()
    dic2 = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
    sortedcols = [i for i in range(count)] + list(dic2.keys())
    M = permutate_columns(M, sortedcols)
    newV = [V[i] for i in sortedcols]
    return M, newV


def showmat(M, V):
    """
    Visualizes the matrix.
    """
    count = 0
    for e in V:
        if e[0] != "x":
            count += 1

    plt.plot([i for i in range(M.get_shape()[1])], [count - 0.5 for i in range(M.get_shape()[1])], linewidth=0.5,
             color="black")
    for e in range(count, M.get_shape()[0], 28):
        plt.plot([i for i in range(M.get_shape()[1])], [e - 0.5 for i in range(M.get_shape()[1])], linewidth=0.5,
                 color="black")
    plt.plot([count - 0.5 for i in range(M.get_shape()[0])], [i for i in range(M.get_shape()[0])], linewidth=0.5)

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    cmap = colors.ListedColormap(['#00315F', '#00315F', '#00315F', '#00618F', '#00618F', 'white', '#00A1CF'])
    # bounds=[-10,-1,-0.5,0.5,1]
    # norm = colors.BoundaryNorm(bounds, cmap.N)
    im = plt.imshow(data2D, cmap=cmap)
    cb = plt.colorbar(im)

    # cmap=cmap, norm=norm, boundaries=bounds, ticks=[-5,-1,0, 1]
    cb.remove()
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # plt.savefig("AES3rnative",dpi=400,bbox_inches='tight')
    plt.show()


def showfirststruc(M, V):
    """
    shows a structure for AES when it has a special form.
    """
    count = 0  # begins at 1 because of the constraint that ensures that there is one active sbox
    for e in V:
        if e[0] != "x":
            count += 1
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    cmap = colors.ListedColormap(['teal', 'teal', 'teal', 'lightseagreen', 'lightseagreen', 'white', 'turquoise'])
    im = plt.imshow(data2D, cmap=cmap)
    plt.colorbar(im)
    plt.plot([i for i in range(M.get_shape()[1])], [count - 0.5 for i in range(M.get_shape()[1])], linewidth=0.5)

    # vertikale striche
    leng = (M.get_shape()[1]) - 17 - count
    teil = leng / 16
    for e in range(int(teil) + 2):
        plt.plot([count + 16 * e - 0.5 for i in range(M.get_shape()[0])], [i for i in range(M.get_shape()[0])],
                 linewidth=0.5)

    # horizontale linien
    leng2 = (M.get_shape()[0]) - 1 - count
    teil2 = leng2 / 32
    for e in range(int(teil2) + 1):
        plt.plot([i for i in range(M.get_shape()[1])], [count + 16 + 32 * e - 0.5 for i in range(M.get_shape()[1])],
                 linewidth=0.5)
    plt.show()


def showsecstruc(M, V):
    count = 0  # begins at 1 because of the constraint that ensures that there is one active sbox
    for e in V:
        if e[0] != "x":
            count += 1
    num = M.getcol(M.get_shape()[1] - 1).count_nonzero()
    leng = M.get_shape()[1] - count
    for i in range(count, M.get_shape()[1]):
        if M.getcol(i).count_nonzero() == num:
            siz = M.get_shape()[1] - i
            break
    print(leng, siz)
    c = 1
    while True:
        if leng % (siz / c) == 0:
            break
        c += 1
    siz = int(siz / c)
    numofb = leng / siz
    print(numofb, siz)
    for e in range(int(numofb)):
        # print(M.getcol(count+siz*e).nonzero()[0][-1])
        if e == 0:
            anfang = 0
        elif len(M.getcol(count + siz * (e - 1)).nonzero()[0]) > 4:
            anfang = M.getcol(count + siz * (e - 1)).nonzero()[0][-2]
        else:
            anfang = M.getcol(count + siz * (e - 1)).nonzero()[0][-1]

        if e == numofb - 1 or e == 0:
            ende = M.get_shape()[0]
        else:
            ende = M.getcol(count + siz * (e + 1) - 1).nonzero()[0][-1]
            print(M.getcol(count + siz * (e + 1) - 1).nonzero()[0])
        plt.plot([count + siz * e - 0.5 for i in range(anfang, ende + 2)], [i - 0.5 for i in range(anfang, ende + 2)],
                 linewidth=0.5, color="grey")
        plt.plot([count + siz * e - 0.5 for i in range(count + 1)], [i - 0.5 for i in range(count + 1)], linewidth=0.5,
                 color="grey")

        # horizontal
        if len(M.getcol(count + siz * e).nonzero()[0]) > 4:
            eintrag = M.getcol(count + siz * e).nonzero()[0][-2]
        else:
            eintrag = M.getcol(count + siz * e).nonzero()[0][-1]
        if e == 0:
            plt.plot([i - 0.5 for i in range(M.get_shape()[1] + 1)],
                     [eintrag - 0.5 for i in range(M.get_shape()[1] + 1)], linewidth=0.5, color="grey")
        else:
            plt.plot([i - 0.5 for i in range(count + 1)], [eintrag - 0.5 for i in range(count + 1)], linewidth=0.5,
                     color="grey")
            plt.plot([i - 0.5 for i in range(count + siz * (e - 1), count + siz * (e + 1) + 1)],
                     [eintrag - 0.5 for i in range(count + siz * (e - 1), count + siz * (e + 1) + 1)], linewidth=0.5,
                     color="grey")

        # für beispiel generieren
        # plt.plot([i for i in range(M.get_shape()[1])],[4.5 for i in range(M.get_shape()[1])],linewidth = 0.5,color='#00315F')
        # plt.plot([i for i in range(M.get_shape()[1])],[8.5 for i in range(M.get_shape()[1])],linewidth = 0.5,color='#00315F')
        # hier gucken von der jeweilien column wo das größte
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    cmap = colors.ListedColormap(['#00315F', '#00315F', '#00315F', '#00618F', '#00618F', 'white', '#00A1CF'])
    im = plt.imshow(data2D, cmap=cmap)
    cb = plt.colorbar(im)
    cb.remove()
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.savefig("AES3rblock", dpi=400, bbox_inches='tight')
    plt.show()


def enostruc(M, V):
    count = 0
    for e in V:
        if e[0] != "x":
            count += 1
    plt.plot([i for i in range(M.get_shape()[1])], [count - 0.5 for i in range(M.get_shape()[1])], linewidth=0.5)
    plt.plot([count - 0.5 for i in range(M.get_shape()[0])], [i for i in range(M.get_shape()[0])], linewidth=0.5)

    la = [i for i in range(count, M.get_shape()[0])]
    C = M[la, :]
    lengthofblocks = [0, count]  # for test
    for i in range(count, M.get_shape()[1] - 1):
        if C.getcol(i).count_nonzero() != C.getcol(i + 1).count_nonzero():
            plt.plot([i + 0.5 for e in range(M.get_shape()[0])], [e for e in range(M.get_shape()[0])], linewidth=0.5)
            # horizontal
            plt.plot([e for e in range(M.get_shape()[1])],
                     [M.getcol(i).nonzero()[0][-1] + 0.5 for e in range(M.get_shape()[1])], linewidth=0.5)
            lengthofblocks.append(M.getcol(i).nonzero()[0][-1] + 1)
    lengthofblocks.append(M.get_shape()[0])
    for i in range(len(lengthofblocks) - 1):
        print(lengthofblocks[i + 1] - lengthofblocks[i])

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    cmap = colors.ListedColormap(['teal', 'teal', 'teal', 'lightseagreen', 'lightseagreen', 'white', 'turquoise'])
    im = plt.imshow(data2D, cmap=cmap)
    plt.colorbar(im)
    plt.show()


def enonewshape(M, V):
    count = 0  # begins at 1 because of the constraint that ensures that there is one active sbox
    for e in V:
        if e[0] != "x":
            count += 1
    # plt.plot([i for i in range(M.get_shape()[1])],[count-0.5 for i in range(M.get_shape()[1])],linewidth = 0.5)
    ##plt.plot([count-0.5 for i in range(M.get_shape()[0])],[i for i in range(M.get_shape()[0])],linewidth = 0.5)
    la = [i for i in range(count, M.get_shape()[0])]
    C = M[la, :]
    colInterval = []
    colInterval.append(count)
    for i in range(count, M.get_shape()[1] - 1):
        if C.getcol(i).count_nonzero() != C.getcol(i + 1).count_nonzero():
            # plt.plot([i+0.5 for e in range(M.get_shape()[0])],[e for e in range(M.get_shape()[0])],linewidth = 0.5)
            colInterval.append(i)
    rowInter = [count - 1]
    # plt.plot([e for e in range(M.get_shape()[1])],[count-1 for e in range(M.get_shape()[1])],linewidth = 0.5)
    for i in colInterval[1:]:
        rowInter.append(M.getcol(i).nonzero()[0][-1])
        # plt.plot([e for e in range(M.get_shape()[1])],[M.getcol(i).nonzero()[0][-1] for e in range(M.get_shape()[1])],linewidth = 0.5)
    order = [i for i in range(0, count)]
    neworder = []
    for i in range(len(rowInter) * -1, -1):
        s = i * -1
        for e in range(rowInter[i] + 1, rowInter[i + 1] + 1):  # +1 weggemacht
            if e % s == 1:
                order.append(e)
            else:
                neworder.append(e)
    order = order + [i for i in range(rowInter[-1] + 1, M.get_shape()[0])]
    order = neworder + order

    M = permutate_rows(M, order)
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    cmap = colors.ListedColormap(['teal', 'teal', 'teal', 'lightseagreen', 'lightseagreen', 'white', 'turquoise'])
    im = plt.imshow(data2D, cmap=cmap)
    plt.colorbar(im)
    plt.show()


def n_fold_differential_LBlock_k_rounds(matrix, variables, k=2, **kwargs):
    """
    The following applies for a differential LBlock cryptanalysis.

    Args:
        matrix: constraint matrix of lil_sparse format
        variables: dictionary mapping variable names to matrix columns and vice versa
        k: number or rounds

    Returns: Rearranged matrix to fit the n-fold structure and variables.

    """
    # first we rearrange the columns by
    # 1. collecting the variable names in our desired order
    # 2. mapping the names to column indices
    # 3. permuting according to said list of indices
    new_order_columns = list(range(matrix.get_shape()[1]))

    # Blocks for a S-box contain variables x input, x output, a dummy, k xor prior, x xor
    start_new_x_values = lambda n: 64 + (n * 96)

    # First we construct a list with the name of variables in the order we want their corresponding matrix columns to be

    # for each round we add 8 blocks
    # each block corresponds to a S-box in order to receive a better looking or more structured matrix
    blocks = [[
        # xor of key and left hand input variables (in F function)
        [f'k{(round_k * 32) + box * 4 + i}' for i in range(4)] +  # xor input, key
        [f'x{start_new_x_values(round_k) + box * 4 + i}' for i in range(4)] +  # xor output
        [f'dx{4 * box + (64 * round_k) + i}' for i in range(4)] +

        # S-box applicaiton of xor output (in F function)
        [f'a{box + (8 * round_k)}'] +  # sbox input
        [f'x{start_new_x_values(round_k) + 32 + box * 4 + i}' for i in range(4)] +  # sbox out, 2. xor 2. input

        # xor of right hand input variables and S-box output
        [f'x{start_new_x_values(round_k) + 64 + box * 4 + i}' for i in range(4)] +  # zweiter xor output
        [f'dx{4 * box + (64 * round_k) + 32 + i}' for i in range(4)]
        for box in range(8)] for round_k in range(k)]

    # for the first round, we add the initial inputs since they are not included in the previous list while the inputs
    # for subsequent rounds are automatically available thanks to them being outputs
    for index, box_list in enumerate(blocks[0].copy()):
        blocks[0][index] = box_list + [f'x{(index * 4) + i}' for i in range(4)] + [f'x{32 + 4 * index + i}' for i in
                                                                                   range(4)]

    # we transform the list of lists of lists into one long list by concatenating all lists
    blocks = list(chain.from_iterable(list(chain.from_iterable(blocks))))

    # and use the mapping from variable names to list indices to get a list of indices
    for index, var_name in enumerate(blocks):
        new_order_columns[index] = variables[var_name]

    # according to which we can permute the columns to fit our desired format
    matrix = permutate_columns(matrix, new_order_columns)
    # which finishes the column permutation

    # we begin to permute the rows by flipping the row order
    # this is done because the last added constraint is the one highest up in the picture
    # (i.e. the index counts up from the bottom of the constructed image)
    reversed_row_indices = list(range(matrix.get_shape()[0]))

    # now we collect the linking constraints which are all non-S-box constraints
    linking_constraints = reversed_row_indices[: k * ((2 * 16 + 7) * 8)].copy()
    for round_k in range(k):
        start_standard_box_constraints = (round_k * (2 * 16 * 8)) + (16 * 8)
        end_standard_box_constraints = start_standard_box_constraints + (7 * 8)
        linking_constraints = linking_constraints[:start_standard_box_constraints].copy() + linking_constraints[
                                                                                            end_standard_box_constraints:].copy()

    # then we collect the S-box constraints which are not introduced by the chosen additional modeling (e.g. from Boura)
    # but by the initial constraints from SunEtAl which do not really look into the concept of feasible transitions
    rows_of_standard_sbox_constraints = [
        [reversed_row_indices[round_k * (16 * 8 + 7 * 8 + 16 * 8) + 16 * 8 + i] for i in range(7 * 8)] for round_k in
        range(k)]

    # determine the position of the sum over all S-box activity indicators
    the_ultimate_linking_constraint = [(k * ((2 * 16 + 7) * 8)) + 1]

    # finally, we collect the S-box constraints which are introduced by the chosen additional
    # modeling (e.g. "Logical Conditional Modeling")
    amount_extra_sbox_constraints = len(reversed_row_indices) - ((k * ((2 * 16 + 7) * 8)) + 1)
    amount_extra_sbox_constraints_per_round = int(amount_extra_sbox_constraints / k)
    rows_of_extra_sbox_constraints = [[reversed_row_indices[the_ultimate_linking_constraint[0] + (
            round_k * amount_extra_sbox_constraints_per_round) + i] for i in
                                       range(amount_extra_sbox_constraints_per_round)] for round_k in range(k)]

    # after collecting the row indices previously, we now order them in accordance with our desired structure
    new_rows = the_ultimate_linking_constraint + linking_constraints
    for round_k in range(k):
        new_rows += rows_of_standard_sbox_constraints[round_k] + rows_of_extra_sbox_constraints[round_k]
    new_rows_reversed = [new_rows[i] for i in range(len(new_rows) - 1, -1, -1)]

    # permute rows according to list
    matrix = permutate_rows(matrix, new_rows_reversed)
    return matrix, variables


def two_stage_differential_LBlock_k_rounds(matrix, variables, k=2, **kwargs):
    """
    The following applies for a differential LBlock cryptanalysis

    Args:
        matrix: constraint matrix of lil_sparse format
        variables: dictionary mapping variable names to matrix columns and vice versa
        k: number of rounds the analysis has been constructed for

    Returns:
        matrix: rearranged matrix to fit the 2-stage structure
        variables: dictionary mapping variable names to matrix columns and vice versa

    """
    # the (extended) 2-stage we are looking to get for the structure is analogous to the n-fold of different modelings
    # in that the C_{extd. 2-stage} and A_{extd. 2-stage} constraints are almost the same as the A_{n-fold} and
    # B_{n-fold} constraints except for the fact that the additional S-box constraints are missing.
    # In their stead we introduce a lot of variables and constraints from the Baksi modeling for the B_{ 2-stage} blocks

    # Therefore, this code works as follows:
    # 1. collecting the variable names in our desired order
    #       which is: for every round and every word - left xor inputs in the form of key vars, xor outputs,
    #       s-box dummies, s-box outputs, right xor outputs, right xor dummies
    #    which is then followed by a large part for the many dummies/indicators introduced by the Baksi modeling,
    #    again sorted by round and S-box.
    # 2. mapping the names to column indices
    # 3. permuting according to said list of indices
    new_order_columns = list(range(matrix.get_shape()[1]))

    # Blocks for an S-box contain variables x input, x output, a dummy, k xor prior, x xor
    start_new_x_values = lambda n: 64 + (n * 96)

    blocks = [[[f'k{(round_k * 32) + box * 4 + i}' for i in range(4)] +  # xor input, key
               [f'x{start_new_x_values(round_k) + box * 4 + i}' for i in range(4)] +  # xor output
               [f'dx{4 * box + (64 * round_k) + i}' for i in range(4)] +
               [f'a{box + (8 * round_k)}'] +  # sbox input
               [f'x{start_new_x_values(round_k) + 32 + box * 4 + i}' for i in range(4)] +  # sbox out, 2. xor 2. input
               [f'x{start_new_x_values(round_k) + 64 + box * 4 + i}' for i in range(4)] +  # zweiter xor output
               [f'dx{4 * box + (64 * round_k) + 32 + i}' for i in range(4)]
               for box in range(8)] for round_k in range(k)]

    # first round additionally includes the first input (x_l, x_r) prior to the respective xors where they are used
    for index, box_list in enumerate(blocks[0].copy()):
        blocks[0][index] = box_list + [f'x{(index * 4) + i}' for i in range(4)] + [f'x{32 + 4 * index + i}' for i in
                                                                                   range(4)]

    # we transform the list of lists into one long list by concatenating all sub-lists
    blocks = list(chain.from_iterable(blocks))

    # collecting variables names of those variables specific to the Baksi modeling
    list_of_qijlp_vars = list(filter(lambda x: 'l' in str(x), list(variables)))
    count_of_qijlp_vars = len(list_of_qijlp_vars)
    list_of_qijp_vars = list(filter(lambda x: ('p' in str(x)) and ('l' not in str(x)), list(variables)))
    count_of_qijp_vars = len(list_of_qijp_vars)

    # creating lists for the variables corresponding to the activity of the single S-boxes
    for i in range(8 * k):
        dummy_var = 'a' + str(i)
        blocks += [list(filter(lambda x: dummy_var + 'p' == x[:len(dummy_var) + 1], list_of_qijp_vars))]
        blocks += [list(filter(lambda x: dummy_var + 'p' == x[:len(dummy_var) + 1], list_of_qijlp_vars))]

    # once again transform from list of lists into list
    blocks = list(chain.from_iterable(blocks))

    # and use the mapping from variable names to list indices to get a list of indices
    for index, var_name in enumerate(blocks):
        new_order_columns[index] = variables[var_name]

    matrix = permutate_columns(matrix, new_order_columns)

    # starting with the arrangement of rows

    # first flip row order
    reversed_row_indices = list(range(matrix.get_shape()[0]))

    # linking constraints zusammengruppieren
    linking_constraints = reversed_row_indices[: k * ((2 * 16 + 7) * 8)].copy()
    for round_k in range(k):
        start_standard_box_constraints = (round_k * (2 * 16 * 8)) + (16 * 8)
        end_standard_box_constraints = start_standard_box_constraints + (7 * 8)
        linking_constraints = linking_constraints[:start_standard_box_constraints].copy() + linking_constraints[
                                                                                            end_standard_box_constraints:].copy()

    rows_of_standard_sbox_constraints = list(chain.from_iterable([
        [[reversed_row_indices[round_k * (16 * 8 + 7 * 8 + 16 * 8) + 16 * 8 + (sbox * 7 + i)] for i in range(7)] for
         sbox in range(8)] for round_k in
        range(k)]))

    the_ultimate_linking_constraint = [(k * ((2 * 16 + 7) * 8)) + 1]
    amount_extra_sbox_constraints = len(reversed_row_indices) - ((k * ((2 * 16 + 7) * 8)) + 1)
    amount_extra_sbox_constraints_per_round = int(amount_extra_sbox_constraints / (k * 8))
    rows_of_extra_sbox_constraints = [[reversed_row_indices[the_ultimate_linking_constraint[0] + (
            round_k * amount_extra_sbox_constraints_per_round) + i] for i in
                                       range(amount_extra_sbox_constraints_per_round)] for round_k in range(k * 8)]

    print(len(rows_of_standard_sbox_constraints), rows_of_standard_sbox_constraints)
    print(len(rows_of_extra_sbox_constraints), rows_of_extra_sbox_constraints)

    def rearrange_extra_constraints(constraints):
        permutation = [1, 2, 4, 5, 78, 79] + [3] + list(range(6, 78)) + list(range(80, 104))
        permutation = [0, 1, 2] + [p + 2 for p in permutation]
        new_order = list()
        for pos in range(len(constraints)):
            new_order.append(constraints[permutation[pos]])
        return new_order

    new_rows = the_ultimate_linking_constraint + linking_constraints
    for round_k in range(k * 8):
        new_rows += rows_of_standard_sbox_constraints[round_k] + rearrange_extra_constraints(
            rows_of_extra_sbox_constraints[round_k])
    new_rows_reversed = [new_rows[i] for i in range(len(new_rows) - 1, -1, -1)]
    print(len(new_rows_reversed), new_rows_reversed)

    test_direction_of_where_should_be_what = [0 for _ in range(len(new_rows))]
    for i, p in enumerate(new_rows_reversed):
        test_direction_of_where_should_be_what[p] = i

    matrix = permutate_rows(matrix, new_rows_reversed)

    return matrix, variables


def tetrisfold_differential_LBlock_k_rounds(matrix, variables, k=2, **kwargs):
    """
    The following applies for a bit-oriented differential LBlock cryptanalysis

    Args:
        matrix: constraint matrix of lil_sparse format
        variables: dictionary mapping variable names to matrix columns and vice versa
        k: number of rounds the analysis has been constructed for

    Returns:
        matrix: rearranged matrix to fit the 2-stage structure
        variables: dictionary mapping variable names to matrix columns and vice versa

    """
    # The tetris-fold we are looking is made up of a xor block and s-box block in the F-function block. After that, a
    # block is included for the right-hand xor.
    # Thereby, the rows are ordered strictly by order of construction. (This requires a reordering as compared to the
    # current state where S-box constraints additional to those introduced in Sun et al. 2013 are added at the end of
    # the MILP constraint matrix).
    # Unlike in the n-fold and 2-stage modeling, blocks representing operations are not further divided into their words

    # built under the assumption that there are no constraints for being used for permutations and only for XOR & S-Box

    # 1. ordering the columns by
    #   a) looking up variables names and ordering them to fit their first appearance in the cipher
    #   b) mapping names to matrx indices
    #   c) sorting actual columns according to new index list
    new_order_columns = list(range(matrix.get_shape()[1]))

    # starting off with the input to the first F-function as that not already included
    blocks = [f'x{i}' for i in range(64)]

    for r in range(k):
        xors_so_far = 64 * r
        # Add F-stuff
        # add xor with key input
        blocks += [f'k{i + int(xors_so_far/2)}' for i in range(32)]
        # add xor with key dummies
        blocks += [f'dx{i + xors_so_far}' for i in range(32)]
        # add xor with key output
        blocks += [f'x{i + 96 * r + 64}' for i in range(32)]
        # add sbox dummies
        blocks += [f'a{i + 8 * r}' for i in range(8)]
        # add sbox output
        blocks += [f'x{i + 96 * r + 64 + 32}' for i in range(32)]

        xors_so_far = 64 * r + 32

        # Add righthand xor stuff
        # add xor with key dummies
        blocks += [f'dx{i + xors_so_far}' for i in range(32)]
        # add xor with key output
        blocks += [f'x{i + 96 * r + 64}' for i in range(32)]

    for index, var_name in enumerate(blocks):
        new_order_columns[index] = variables[var_name]

    matrix = permutate_columns(matrix, new_order_columns)

    # 2. ordering the rows according to appearance by
    #   a) finding the number of constraints per F-function and right-hand xor in the upper part
    #   b) finding the number of S-box constraints per S-box in the lower part
    #   c) sorting list by [index of linking constraint] + [the correct mix of first f-function then right-hand xor]
    #   d) reverse order of rows in reference assignment because they are visualized upside down
    #   e) sorting actual rows according to new index list

    # a)
    number_constraints_xor_in_f_function = 4 * 32
    number_constraints_sbox_in_f_function = 7 * 8  # could be done nicer, but we are brute counting at this point
    number_constraints_per_f_function_block = (number_constraints_xor_in_f_function +
                                               number_constraints_sbox_in_f_function)
    number_constraints_per_right_hand_xor_block = 4 * 32
    number_constraints_per_round = number_constraints_per_f_function_block + number_constraints_per_right_hand_xor_block

    list_constraints_xor_in_f_function = [list(range(1 + r * number_constraints_per_round,
                                                     1 + r * number_constraints_per_round +
                                                     number_constraints_xor_in_f_function))
                                          for r in range(k)]
    list_constraints_sbox_in_f_function = [list(
        range(1 + r * number_constraints_per_round + number_constraints_xor_in_f_function,
              1 + r * number_constraints_per_round + number_constraints_xor_in_f_function +
              number_constraints_sbox_in_f_function))
        for r in range(k)]
    list_constraints_right_hand_xor = [list(
        range(1 + r * number_constraints_per_round + number_constraints_xor_in_f_function +
              number_constraints_sbox_in_f_function,
              1 + r * number_constraints_per_round + number_constraints_xor_in_f_function +
              number_constraints_sbox_in_f_function + number_constraints_per_right_hand_xor_block))
        for r in range(k)]

    # b)
    number_all_constraints_upper_part_incl_linking = (number_constraints_per_round * k) + 1
    number_constraints_in_lower_s_box_part = matrix.get_shape()[0] - number_all_constraints_upper_part_incl_linking
    number_constraints_in_lower_s_box_part_per_round = int(number_constraints_in_lower_s_box_part / k)
    number_constraints_in_lower_s_box_part_per_sbox = 12    # unsure, counted by hand; only counted for the
                                                            # greedy convex hull modeling from Sun et al. 2013

    # The following is a list which includes one list per round including one list per S-box
    #
    # list_constraint_indices_lower_sboxes = [[list(range(number_all_constraints_upper_part_incl_linking +
    #                                                   r * number_constraints_in_lower_s_box_part_per_round +
    #                                                   sbox * number_constraints_in_lower_s_box_part_per_sbox,
    #                                                   number_all_constraints_upper_part_incl_linking +
    #                                                   r * number_constraints_in_lower_s_box_part_per_round +
    #                                                   (sbox + 1) * number_constraints_in_lower_s_box_part_per_sbox))
    #                                        for sbox in range(8)] for r in range(k)]

    list_constraint_indices_lower_sboxes = [list(
        range(1 + number_all_constraints_upper_part_incl_linking + r * number_constraints_in_lower_s_box_part_per_round,
              1 + number_all_constraints_upper_part_incl_linking + (
                      r + 1) * number_constraints_in_lower_s_box_part_per_round))
        for r in range(k)]

    # c)
    # for each round, we include first the list of xor with key constraints, then the sbox constraints (upper and lower)
    # and then the right-hand xor constraints
    list_of_indices = [list_constraints_xor_in_f_function[r] + list_constraints_sbox_in_f_function[r] +
                       list_constraint_indices_lower_sboxes[r] + list_constraints_right_hand_xor[r] for r in range(k)]

    list_of_indices = [0] + list(chain.from_iterable(list_of_indices))
    print(list_of_indices)
    print(len(list_of_indices), len(set(list_of_indices)))
    set_of_indices = set()
    for index in list_of_indices:
        if index in set_of_indices:
            print(index)
        else:
            set_of_indices.add(index)
    # TODO: take a look at whether interweaving the s-box constraints looks better

    # d)
    list_of_indices.reverse()

    # e)
    matrix = permutate_rows(matrix, list_of_indices)
    return matrix, variables


def tetrisfold_differential_aes_k_round(matrix, variables, k=2, **kwargs):
    matrixshape = matrix.get_shape()
    new_order_columns = list(range(matrixshape[1]))
    print('matrix', matrix.get_shape())
    print('variables', len(variables))

    # xor prior to round 1
    blocks = [  # initial round key xor
        [f'x{byte}' for byte in range(16)] +  # first xor input
        [f'k{byte}' for byte in range(16)] +  # xor key var
        [f'dx{byte}' for byte in range(16)] +  # xor dummy var
        [f'x{byte + 16}' for byte in range(16)]  # xor output
    ]

    #
    for i in range(k):
        blocks += [  # mix column action
            [f'dl{byte + (4 * i)}' for byte in range(4)] +  # mix columns as linear transformation dummy variable
            [f'x{byte + (32 * (i + 1))}' for byte in range(16)]  # mix columns output variables
        ]
        blocks += [  # initial round key xor
            [f'k{byte + (16 * (i + 1))}' for byte in range(16)] +  # xor input: key variables
            [f'dx{byte + (16 * (i + 1))}' for byte in range(16)] +  # xor dummy variable
            [f'x{byte + 16 + (32 * (i + 1))}' for byte in range(16)]  # xor output
        ]

    blocks = list(chain.from_iterable(blocks))

    for index, var_name in enumerate(blocks):
        new_order_columns[index] = variables[var_name]  # variables[var_name]

    matrix = permutate_columns(matrix, new_order_columns)

    new_rows_reversed = list(range(matrixshape[0] - 1, -1, -1))

    matrix = permutate_rows(matrix, new_rows_reversed)

    return matrix, variables


def tetrisfold_linear_aes_k_round(matrix, variables, k=2, **kwargs):
    matrixshape = matrix.get_shape()
    new_order_columns = list(range(matrixshape[1]))
    print('matrix', matrix.get_shape())
    print('variables', len(variables))

    blocks = [[f'x{i}' for i in range(16)]]

    for i in range(k):
        blocks += [  # mix column action
            [f'dl{byte + (4 * i)}' for byte in range(4)] +  # mix columns as linear transformation dummy variable
            [f'x{byte + (16 * (i + 1))}' for byte in range(16)]  # mix columns output variables
        ]

    blocks = list(chain.from_iterable(blocks))

    print(blocks)

    for index, var_name in enumerate(blocks):
        new_order_columns[index] = variables[var_name]  # variables[var_name]

    matrix = permutate_columns(matrix, new_order_columns)

    new_rows_reversed = list(range(matrixshape[0] - 1, -1, -1))

    matrix = permutate_rows(matrix, new_rows_reversed)

    return matrix, variables


def tetrisfold_differential_gift64_k_round(matrix, variables, k=2, **kwargs):
    matrixshape = matrix.get_shape()
    new_order_columns = list(range(matrixshape[1]))
    print('matrix', matrix.get_shape())
    print('variables', len(variables))

    blocks = [[f'x{i}' for i in range(64)]]

    for i in range(k):
        blocks += [  # sbox action
            [f'a{box + (16 * i)}' for box in range(16)] +  # sbox input
            [f'x{bit + 64 + 128 * i}' for bit in range(64)]
        ]
        blocks += [  # xor actions
            [f'k{bit + (32 * i)}' for bit in range(32)] +
            [f'dx{bit + (32 * i)}' for bit in range(32)] +  # mix columns as linear transformation dummy variable
            [f'dl{bit + (7 * i)}' for bit in range(7)] +  # mix columns as linear transformation dummy variable
            [f'x{bit + 64 * (2 * i + 2)}' for bit in range(64)]  # mix columns output variables
        ]

    blocks = list(chain.from_iterable(blocks))

    print(blocks)

    for index, var_name in enumerate(blocks):
        new_order_columns[index] = variables[var_name]  # variables[var_name]

    matrix = permutate_columns(matrix, new_order_columns)

    # 2. ordering the rows according to appearance by
    #   a) finding the number of constraints per F-function and right-hand xor in the upper part
    #   b) finding the number of S-box constraints per S-box in the lower part
    #   c) sorting list by [index of linking constraint] + [the correct mix of first f-function then right-hand xor]
    #   d) reverse order of rows in reference assignment because they are visualized upside down
    #   e) sorting actual rows according to new index list

    # a)
    number_constraints_sbox_in_f_function_per_round = 7 * 16
    number_constraints_xor_in_f_function_per_round = 7 * 8  # could be done nicer, but we are brute counting at this point
    number_constraints_per_f_function_block = (number_constraints_xor_in_f_function_per_round +
                                               number_constraints_sbox_in_f_function_per_round)
    number_constraints_per_right_hand_xor_block = 4 * 32
    number_constraints_per_round = number_constraints_per_f_function_block + number_constraints_per_right_hand_xor_block

    list_constraints_xor_in_f_function = [list(range(1 + r * number_constraints_per_round,
                                                     1 + r * number_constraints_per_round +
                                                     number_constraints_xor_in_f_function_per_round))
                                          for r in range(k)]
    list_constraints_sbox_in_f_function = [list(
        range(1 + r * number_constraints_per_round + number_constraints_xor_in_f_function_per_round,
              1 + r * number_constraints_per_round + number_constraints_xor_in_f_function_per_round +
              number_constraints_sbox_in_f_function_per_round))
        for r in range(k)]
    list_constraints_right_hand_xor = [list(
        range(1 + r * number_constraints_per_round + number_constraints_xor_in_f_function_per_round +
              number_constraints_sbox_in_f_function_per_round,
              1 + r * number_constraints_per_round + number_constraints_xor_in_f_function_per_round +
              number_constraints_sbox_in_f_function_per_round + number_constraints_per_right_hand_xor_block))
        for r in range(k)]

    # b)
    number_all_constraints_upper_part_incl_linking = (number_constraints_per_round * k) + 1
    number_constraints_in_lower_s_box_part = matrix.get_shape()[0] - number_all_constraints_upper_part_incl_linking
    number_constraints_in_lower_s_box_part_per_round = int(number_constraints_in_lower_s_box_part / k)
    number_constraints_in_lower_s_box_part_per_sbox = 12    # unsure, counted by hand; only counted for the
                                                            # greedy convex hull modeling from Sun et al. 2013

    # The following is a list which includes one list per round including one list per S-box
    #
    # list_constraint_indices_lower_sboxes = [[list(range(number_all_constraints_upper_part_incl_linking +
    #                                                   r * number_constraints_in_lower_s_box_part_per_round +
    #                                                   sbox * number_constraints_in_lower_s_box_part_per_sbox,
    #                                                   number_all_constraints_upper_part_incl_linking +
    #                                                   r * number_constraints_in_lower_s_box_part_per_round +
    #                                                   (sbox + 1) * number_constraints_in_lower_s_box_part_per_sbox))
    #                                        for sbox in range(8)] for r in range(k)]

    list_constraint_indices_lower_sboxes = [list(
        range(1 + number_all_constraints_upper_part_incl_linking + r * number_constraints_in_lower_s_box_part_per_round,
              1 + number_all_constraints_upper_part_incl_linking + (
                      r + 1) * number_constraints_in_lower_s_box_part_per_round))
        for r in range(k)]

    # c)
    # for each round, we include first the list of xor with key constraints, then the sbox constraints (upper and lower)
    # and then the right-hand xor constraints
    list_of_indices = [list_constraints_xor_in_f_function[r] + list_constraints_sbox_in_f_function[r] +
                       list_constraint_indices_lower_sboxes[r] + list_constraints_right_hand_xor[r] for r in range(k)]

    list_of_indices = [0] + list(chain.from_iterable(list_of_indices))
    print(list_of_indices)
    print(len(list_of_indices), len(set(list_of_indices)))
    set_of_indices = set()
    for index in list_of_indices:
        if index in set_of_indices:
            print(index)
        else:
            set_of_indices.add(index)
    # TODO: take a look at whether interweaving the s-box constraints looks better

    # d)
    list_of_indices.reverse()

    # e)
    matrix = permutate_rows(matrix, list_of_indices)

    return matrix, variables
