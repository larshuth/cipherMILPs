import numpy as np
import generateConstraints as gc
import cipher as cip
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


# https://stackoverflow.com/questions/28334719/swap-rows-csr-matrix-scipy

def permutate_rows(H, idenRows):
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
    x = H.tocoo()
    idenRows = np.argsort(idenRows)
    idenRows = np.asarray(idenRows, dtype=x.row.dtype)
    x.row = idenRows[x.row]
    H = x.tocsr()
    return H


def permutate_columns(H, idenCols):
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
    x = H.tocoo()
    idenCols = np.argsort(idenCols)
    idenCols = np.asarray(idenCols, dtype=x.col.dtype)
    x.col = idenCols[x.col]
    H = x.tocsr()
    return H


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


if False:
    aes = cip.Enocoro
    A, V = gc.new_generate_constraints(7, aes)
    # showmat(A)
    M, v = d_var_to_beginning(A, V)
    B = long_constraints_to_top(M)
    C, W = create_fourblock(A, V)
    # block_structure(C,W)
    # C =twodiag(C,W)
    # C,W =changediag(C,W)
    # C=creating_diagonal_in4block(C,W)
    # C,W = changediag(C,W)
    # C =changedvar(C,W)
    # C,W =deletecolszero(C,W)
    showmat(B, v)
    # showfirststruc(C,W)
    # showsecstruc(C,W)
    # print(W)
    # enostruc(C,W)
    # enonewshape(C,W)

    # was es alles gibt:
