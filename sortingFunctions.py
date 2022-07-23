import numpy as np
import scipy.sparse as sps
import generateConstraints as gc

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
    THIS FUNCTION IS DUMB BECAUSE IT DOESNT WORK RIGHT (CAUSE OF VARIABLES THAT ARE ONLY USED IN BEGINNING AND END)

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
    x variables follow.

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
        else:
            orderofxvar.append(V.index(i))
    sortedindices = sortedindices + orderofxvar
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
    count=0
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



