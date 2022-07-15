
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
                :   scr Matrix
                    Constraint Matrix of the corresponding MILP

    """
    line = 0 #shows in which row we are
    next=16
    for r in range(rounds):
        if len(A)==4: #has to be changed to if its a twodimensional list
            #now we have to calculate with the matrix
            
            for j in range(4):
                for i in range(4):
                    #we take the first row and search the index for the variable
                    #print(np.where(M.getrow(0).toarray()==A[i][j]))
                    ##print("lala")
                    #print(M.toarray())
                    ind= V.index(A[i][j])
                    M[line,ind]=1
                for i in range(4):
                    #inde= M.getrow(0).count_nonzero() #ist das richtig?
                    V.append("x"+str(next+i))
                    A[i][j]="x"+str(next+i)
                    M[line,len(V)-1]=1
                next=next+4    
                V.append("d"+str(r*4+j)) #erste Nullstelle wird zur dummy variablen
                M[line,len(V)-1]=-5
                M, line = generate_smallconstraints(M, line)
                line+=1
                #print(M.toarray())
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
    dummyIndex=np.where(M.getrow(line).toarray()[0]==-5)[0][0]
    for ind in np.where(M.getrow(line).toarray()[0]==1)[0]:
        line+=1
        M[line,ind]=-1
        M[line,dummyIndex]=1
    return M, line

def aes(rounds):
    M=csr_matrix((36*rounds,16+20*rounds),dtype=int)
    V=[]
    A = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    next=0
    for i in range(4):
        for j in range(4):
            A[i][j]="x"+str(next)
            V.append("x"+str(next))
            next=next+1
    
    M = generate_constraints(rounds, A, M, V)
    return M
    
print(aes(3).toarray())

test=csr_matrix((2,3),dtype=int)
test[1,0]=7
print(test.toarray())
