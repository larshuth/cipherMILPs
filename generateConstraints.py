import numpy as np
from scipy.sparse import csr_matrix
#im not sure if the functions for the ciphers also belong here

def generate_constraints(rounds, A, M, V, function=""):
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
    M           :   scr Matrix
                    Constraint Matrix of the corresponding MILP

    """
    line = 0 #shows in which row we are
    next=16
    for r in range(rounds):
        if len(A)==4: #has to be changed to if its a twodimensional list EDIT:IM SORRY SOFI BUT THIS IS BS!
            #now we have to calculate with the matrix
            A=shiftrows(A)
            A, M, V, line, next = mix_column(A, M, V, line, next, r)
            #hier mit getattr?
            
    return M


def mix_column(A, M, V, line, next, r):
    """
    Goes trough the mixcolumn step of AES and generates the constraint for that.

    Parameters:
    ----------
    A       :   list of lists
                4x4 matrix where the names of the variables are saved

    M       :   scr_matrix
                The matrix in which all the constraints are saved

    V       :   list
                List of all the variablenames to date

    line    :   int
                Index of row where we are currently

    r       :   int
                Number of the round in which we are currently

    Returns:
    --------
    genau das gleiche oder?
    uhhh ja und genau das wird dann auch bei der function für enocoro gemacht :)))))) nice nice nice wenn das klappt
    """
    for j in range(4):
        for i in range(4):
            #we take the first row and search the index for the variable
            ind= V.index(A[i][j])
            M[line,ind]=1
        for i in range(4):
            V.append("x"+str(next+i))
            A[i][j]="x"+str(next+i)
            M[line,len(V)-1]=1
        next=next+4    
        V.append("d"+str(r*4+j)) #erste Nullstelle wird zur dummy variablen'ÄMDERN!!!!!!!!!!
        M[line,len(V)-1]=-5
        M, line = generate_smallconstraints(M, line)
        line+=1
    return A, M, V, line, next

def shiftrows(A):
    """
    This functions performs the shiftrows operation that is executed after each round in AES.

    Parameters:
    --------
    A       :   list of lists
                The variablenames of the bits used in this round are saved in A
    
    Returns:
    --------
    A       :   list of lists
                The same list, but the rows are shifted
    """
    tmp = [0,0,0,0]
    for i in range (0,4):
        for j in range(0,4):
            tmp[j]= A[i][(j+i)%4]
        for j in range(0,4):
            A[i][j] = tmp[j]   
    return A

def generate_smallconstraints(M, line):
    """
    Generates all the constraint-inequalities that consist of a dummy and a x- variable.
    Those constraints follow after a constraint that models going through a path in a cipher,
    and they just indicate that if a x-variable is 1, then the dummy variable is also 1 and the path
    is active.

    Parameters:
    ----------
    M       :   scr_matrix
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
    dummyIndex=np.where((M.getrow(line).toarray()[0]!=0)&(M.getrow(line).toarray()[0]!=1))[0][0]
    for ind in np.where(M.getrow(line).toarray()[0]==1)[0]:
        line+=1
        M[line,ind]=-1
        M[line,dummyIndex]=1
    return M, line

def aes(rounds):
    """
    Generates the constraint matrix for an MILP which calculates an bound for the number of active s-boxes

    Parameters:
    ---------
    rounds  :   int
                number of rounds for the cipher

    Returns:
    ---------
    M       :   scr_matrix
                the generated constraint matrix for the MILP, still unsorted
    """
    M = csr_matrix((36*rounds,16+20*rounds),dtype=int)
    V = []
    A = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    next=0
    for i in range(4):
        for j in range(4):
            A[i][j]="x"+str(next)
            V.append("x"+str(next))
            next=next+1
    M = generate_constraints(rounds, A, M, V)
    return M
    
print(aes(3))

test=csr_matrix((2,3),dtype=int)
test[1,0]=7
print(test.toarray())

def aus(vari):
    print(vari)

def testing(function):
    function("lala")


testing(aus)