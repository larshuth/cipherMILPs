import numpy as np
#im not sure if the functions for the ciphers also belong here

def generate_constraints(rounds, A, M, function=""):
    """
    Generates the constraint matrix with the given parameters.

    Parameters:
    -----------
    rounds      :   int
                    Number of rounds for the cipher

    A           :   List or Matrix (depends on the cipher)
                    These are the names of the bits that are used in the cipher in this moment

    M           :   scr(sparse compressed row) Matrix
                    Matrix of constraints

    function    :   string
                    Name of the function that has to be used between rounds


    Returns:
    -----------
                :   scr Matrix
                    Constraint Matrix of the corresponding MILP

    """
    line = 1 #shows in which row we are
    for r in range(rounds):
        if len(A)==4: #has to be changed to if its a twodimensional list
            #now we have to calculate with the matrix
            for j in range(4):
                for i in range(4):
                    #we take the first row and search the index for the variable
                    ind= np.where(M.getrow(0).toarray()==A[i][j])[0][0]
                    M[line][ind]=1
