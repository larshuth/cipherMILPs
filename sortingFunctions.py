import numpy as np
import scipy.sparse as sps
import generateConstraints as gc
import cipher as cip
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

#https://stackoverflow.com/questions/28334719/swap-rows-csr-matrix-scipy

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

def long_constraints_to_top(M):
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
    dic={}
    for i in range(M.get_shape()[0]):
        dic[i] = M.getrow(i).count_nonzero()
    dic2 = dict(sorted(dic.items(),key= lambda x:x[1],reverse=True))
    sortedrows = list(dic2.keys())
    M = permutate_rows(M, sortedrows)
    return M

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
    dic2 = dict(sorted(dic.items(),key= lambda x:x[1],reverse=True))
    sortedcols = list(dic2.keys())
    M = permutate_columns(M, sortedcols)
    return M

def d_var_to_beginning(M, V):
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
    sortedindices=[]
    orderofxvar=[]
    for i in V:
        if i[0]=="d":
            sortedindices.append(V.index(i))
        elif i[0]=="x":
            orderofxvar.append(V.index(i))
        else:
            first = [V.index(i)]
    sortedindices = first + sortedindices + orderofxvar
    newV=[V[i] for i in sortedindices]
    M = permutate_columns(M, sortedindices)
    return M, newV

def creating_diagonal_in4block(M,V):
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
    dic={}
    #count how many dummy variables there are. This is so that we only permutate the rows in the diagonal
    count=1 #begins at 1 because of the constraint that ensures that there is one active sbox
    for e in V:
        if e[0]=="d":
            count+=1
    for i in range(M.get_shape()[0]):
        if i>=count:
            dic[i] = M.getrow(i).nonzero()[1][1]
    dic2 = dict(sorted(dic.items(),key= lambda x:x[1],reverse=False))
    sortedrows = list(dic2.keys())
    beginofrows = [i for i in range(count)]
    sortedrows = beginofrows + sortedrows
    M = permutate_rows(M, sortedrows)
    return M

def create_fourblock(M, V):
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
    M, V=d_var_to_beginning(M, V)
    B=long_constraints_to_top(M)
    C=creating_diagonal_in4block(B, V)
    return C, V

def changedvar(M,V):
    """
    changes the columns of the d-variables in order to get a better structure (does not work)
    """
    dic={}
    #count how many dummy variables there are. This is so that we only permutate the rows in the diagonal
    count=0 #begins at 1 because of the constraint that ensures that there is one active sbox
    for e in V:
        if e[0]!="x":
            count+=1
    M=M.tocsc()
    for i in range(M.get_shape()[1]):
        if i<count:
            dic[i] = list(M.getcol(i).nonzero()[0])[-1]
            #print((dic[i]))
    dic2 = dict(sorted(dic.items(),key= lambda x:x[1],reverse=False))
    sortedrows = list(dic2.keys())
    beginofrows = [i for i in range(count,M.get_shape()[1])]
    sortedrows =sortedrows + beginofrows
    #M = permutate_columns(M, sortedrows)
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    im = plt.imshow(data2D, cmap="GnBu_r")
    plt.colorbar(im)
    plt.plot([i for i in range(M.get_shape()[1])],[count-0.5 for i in range(M.get_shape()[1])],linewidth = 0.5)
    
    #vertikale striche
    leng= (M.get_shape()[1])-17-count
    teil = leng/16
    for e in range(int(teil)+2):
        plt.plot([count+16*e-0.5 for i in range(M.get_shape()[0])],[i for i in range(M.get_shape()[0])],linewidth = 0.5)

    #horizontale linien
    leng2=(M.get_shape()[0])-1-count
    teil2 = leng2 / 32
    for e in range(int(teil2)+1):
        plt.plot([i for i in range(M.get_shape()[1])],[count+16+32*e-0.5 for i in range(M.get_shape()[1])],linewidth = 0.5)
    plt.show()
    return M
    #idee: da wo die diagonale gemacht wird die sachen die auf der gleichen höhe sind so lassen und nicht tauschen nach dem ersten element

def block_structure(M, V):
    """
    parameter:
    m   csr_matrix
    This function should create multiple blocks for the matrix
    NOT FINISHED
    """
    #idee: oberer block hat Länge Anzahl(lange constraints)+1
    count=0
    for e in V:
        if e[0]=="d":
            count+=1
        else: break
    ind= [i for i in range(count)]
    out1 = M.tocsc()[:,ind]
    blockC = out1.tocsr()[ind,:]
    #Block C (tc) has to be AT LEAST this big

    #jetzt: wie höhe von Block A und B bestimmen? eig nur rundenanzahl aber wie findet man die raus?
    #vllt einfach alle langen constraints nehmen, also ab wenn weniger sachen in constraints sind.
    #liste die zählt wie viele constraints in jeder row sind? und dann gucken wann die größte abstufung ist?
    #alles was mehr als 2 in der reihe hat ist nicht mehr in den oberen blöcken drin
    numofvarinrow=[]
    print(M.count_nonzero())
    for i in range(M.get_shape()[0]):
            numofvarinrow.append(len(list(M.getrow(i).nonzero()[1])))
    print(numofvarinrow)
    a = np.array(numofvarinrow)
    num = (np.where(a == 2)[0][0]) #row of first constraint that contains 2 elements
    sc = num-0.5
    test =M.toarray()
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    im = plt.imshow(data2D, cmap="GnBu_r")
    plt.colorbar(im)
    plt.plot([i for i in range(M.get_shape()[1])],[sc for i in range(M.get_shape()[1])])
    plt.plot([count for i in range(int(sc+0.5))],[i for i in range(int(sc+0.5))])
    plt.show()
    
def twodiag(M,V):
    """
    Changes the diagonal that consists of two variables on top of each other into two diagonals that have only one line
    """
    count=0 #begins at 1 because of the constraint that ensures that there is one active sbox
    oldorder=[]
    for i in range(M.get_shape()[0]):
        oldorder.append(i)
    for e in V:
        if e[0]=="d":
            count+=1
    neworder=[]
    for i in range(count+17):
        neworder.append(i)
    leng2=(M.get_shape()[0])-1-count
    teil2 = leng2 / 32
    for e in range(int(teil2)-1):
        for i in range(count+17+32*e,count+17+32*(e+1)):
            if i %2 == 1:
                neworder.append(i)
        for i in range(count+17+32*e,count+17+32*(e+1)):
            if i %2 == 0:
                neworder.append(i)
    for i in range(16,0,-1):
        neworder.append(M.get_shape()[0]-i)
    C = permutate_rows(M,neworder)
    return C

def changediag(M,V):
    """
    Changes the columns of the diagonal (the A-blocks) so that the columns with the most non-zero values
    are at the beginning.
    """
    dic={}
    count=0
    for e in V:
        if e[0]!="x":
            count+=1
    M.tocsc()
    for i in range(count, M.get_shape()[1]):
        dic[i] = M.getcol(i).count_nonzero()
    dic2 = dict(sorted(dic.items(),key= lambda x:x[1],reverse=True))
    sortedcols = [i for i in range(count)]+list(dic2.keys())
    M = permutate_columns(M, sortedcols)
    newV=[V[i] for i in sortedcols]
    return M,newV

def showmat(M):
    """
    Visualizes the matrix.
    """
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    cmap = colors.ListedColormap(['teal','teal','teal', 'lightseagreen','lightseagreen','white','turquoise'])
    #bounds=[-10,-1,-0.5,0.5,1]
    #norm = colors.BoundaryNorm(bounds, cmap.N)
    im = plt.imshow(data2D, cmap=cmap)
    plt.colorbar(im)
    #cmap=cmap, norm=norm, boundaries=bounds, ticks=[-5,-1,0, 1]
    plt.show()

def showfirststruc(M,V):
    """
    shows a structure for AES when it has a special form.
    """
    count=0 #begins at 1 because of the constraint that ensures that there is one active sbox
    for e in V:
        if e[0]!="x":
            count+=1
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    data2D = M.toarray()
    cmap = colors.ListedColormap(['teal','teal','teal', 'lightseagreen','lightseagreen','white','turquoise'])
    im = plt.imshow(data2D, cmap=cmap)
    plt.colorbar(im)
    plt.plot([i for i in range(M.get_shape()[1])],[count-0.5 for i in range(M.get_shape()[1])],linewidth = 0.5)
    
    #vertikale striche
    leng= (M.get_shape()[1])-17-count
    teil = leng/16
    for e in range(int(teil)+2):
        plt.plot([count+16*e-0.5 for i in range(M.get_shape()[0])],[i for i in range(M.get_shape()[0])],linewidth = 0.5)

    #horizontale linien
    leng2=(M.get_shape()[0])-1-count
    teil2 = leng2 / 32
    for e in range(int(teil2)+1):
        plt.plot([i for i in range(M.get_shape()[1])],[count+16+32*e-0.5 for i in range(M.get_shape()[1])],linewidth = 0.5)
    plt.show()


aes = cip.Enocoro
A, V=gc.new_generate_constraints(3, aes)
M, v=d_var_to_beginning(A, V)
B=long_constraints_to_top(M)
C, W=create_fourblock(A, V)
#block_structure(C,W)
#C =twodiag(C,W)
#changedvar(C,W)
C,W =changediag(C,W)
C=creating_diagonal_in4block(C,W)
C,W = changediag(C,W)
print(W)
#C,W =deletecolszero(C,W)
showmat(C)
#showfirststruc(C,W)
