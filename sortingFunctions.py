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

M =gc.new_generate_constraints(7,gc.Aes)
M=long_constraints_to_top(M)
M=full_columns_begin(M)


