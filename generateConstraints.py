import numpy as np
from scipy.sparse import csr_matrix
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
            next=16
            for j in range(4):
                for i in range(4):
                    #we take the first row and search the index for the variable
                    print(np.where(M.getrow(0).toarray()==A[i][j]))
                    print("lala")
                    ind= np.where(M.getrow(0).toarray()==A[i][j])[0][0]
                    M[line][ind]=1
                for i in range(4):
                    inde= M.getrow(0).count_nonzero() #ist das richtig?
                    M[0][inde]="x"+str(next+i)
                    A[i][j]="x"+str(next+i)
                    M[line][inde]=1
                next=next+4    
                M[0][inde+1]="d"+str(r*4+j) #erste Nullstelle wird zur dummy variablen
                M[line][inde+1]=-5
                M, line = generate_smallconstraints(M, line)
                line+=1
            #hier mit getattr?
            A=shiftrows(A)
    return M


def shiftrows(a):
    tmp = [0,0,0,0]
    for i in range (0,4):
        for j in range(0,4):
            tmp[j]= a[i][(j+i)%4]
        for j in range(0,4):
            a[i][j] = tmp[j]   
    return a

def generate_smallconstraints(M, line):
    """
    generates all the constraints with two variables
    """
    dummyIndex=np.where(M.getrow(line).toarray()==-5)[0][0]
    for ind in np.where(M.getrow(line).toarray()==1)[0]:
        line+=1
        M[line][ind]=-1
        M[line][dummyIndex]=1
    return M, line

def aes(rounds):
    M=csr_matrix((36*rounds,16+20*rounds),dtype=np.object_)
    #V=csr_matrix(1,16+20*rounds,dtype=np.char)
    A = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    next=0
    for i in range(4):
        for j in range(4):
            A[i][j]="x"+str(next)
            M[0][next]="x"+str(next)
            next=next+1
    
    M = generate_constraints(rounds, A, M)
    return 
    
#
# aes(3)

tewst=np.array(("3","e"))
print(tewst)

row = np.array([0, 0, 1, 2, 2, 2])

col = np.array([0, 2, 2, 0, 1, 2])

data = np.array(["e", "2", "3", "4", "5", "6"],dtype='<U1')

csr_matrix((data, (row, col)), shape=(3, 3)).toarray()