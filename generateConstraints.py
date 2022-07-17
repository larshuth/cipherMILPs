import numpy as np
from scipy.sparse import csr_matrix
#im not sure if the functions for the ciphers also belong here

class Aes:
    """
    Class in which all functions for AES are defined.
    """
    def rangenumber(A):
        """
        Defines how often we need to call gen_long_constraint.

        Parameters:
        ----------
        A   :   list of lists
                needed because other ciphers need this input

        Returns:
        ----------
        The range for generating long constraints.
        """
        return range(4)
    
    def gen_long_constraint(A, M, V, line, next, r, j, S):
        """
        Generates a long constraint depending on which variable is currently j.
        For AES, it is just the current column and the new variables.
        (A part of mixColumn)

        Parameters:
        ----------
        A       :   list of lists
                    4x4 matrix where the names of the current variables are saved

        M       :   scr_matrix
                    The matrix in which all the constraints are saved

        V       :   list
                    List of all the variablenames to date

        line    :   int
                    Index of row where we are currently

        next    :   int 
                    Number of next x-variable that will be generated
        
        r       :   int
                    Number of the round in which we are currently

        j       :   int
                    Column which is currently used for generating the constraint

        S       :   list of lists
                    very unnecessary, I have to see if I can delete it

        Returns:
        --------
        A       :   list of lists
                    4x4 matrix where the new names of the variables are saved

        M       :   scr_matrix
                    The matrix in which all the constraints are saved

        V       :   list
                    List of all the variablenames to date

        line    :   int
                    Index of row where we are currently

        next    :   int 
                    Number of next x-variable that will be generated

        S       :   list of lists
                    very unnecessary, I have to see if I can delete it


        """
        for i in range(4):
            #evey element in column is added to the constraint
            ind = V.index(A[i][j])
            M[line,ind] = 1
        for i in range(4):
            #every new variable added to the constraint and to V
            V.append("x"+str(next+i))
            A[i][j]="x"+str(next+i)
            M[line,len(V)-1]=1
        next=next+4    
        V.append("d"+str(r*4+j))
        M[line,len(V)-1] = -5
        return A, M, V, line, next, S

    def shift_before(A):
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
    
    def shift_after(A):
        """
        In AES the bits dont change after one round so this function does nothing.
        """
        return A

    def initialize(rounds):
        """
        Generates initialization and all neded structures for AES and specified number of rounds.

        Parameters:
        ---------
        rounds  :   int
                    number of rounds for the cipher

        Returns:
        ---------
        A       :   list of lists
                    4x4 matrix where the names of the current variables are saved
        
        M       :   scr_matrix
                    the empty constraint matrix for the MILP

        V       :   list
                    this list saves all the variables

        next    :   int 
                    number for the next x-variable
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
        return A, M, V, next

class Enocoro:
    """
    Class in which all functions for Enocoro are defined.
    """
    def rangenumber(A):
        """
        Defines what to go through in the for loop for gen_long_constraint.

        Parameters:
        ----------
        A   :   list
                names of all variables in this current round

        Returns:
        ----------
            :   list of lists
                specifies which variables belong in the constraint
        """
        return [[A[31],A[32],31],[A[32],A[2],"0"],[A[33],A[7],"1"],[0,1,"2","3"],[A[16],"2",32],[A[29],"3",33],[A[2],A[6],2],[A[7],A[15],7],[A[16],A[28],16]]
    
    def gen_long_constraint(A, M, V, line, next, r, e, S):
        """
        Generates a long constraint depending on which variable is currently j.
        For Enocoro we take the first variables in j. With the last one, we use it to define it new 

        Parameters:
        ----------
        A       :   list
                    names of all variables in this current round

        M       :   scr_matrix
                    the matrix in which all the constraints are saved

        V       :   list
                    list of all the variablenames to date

        line    :   int
                    Index of row where we are currently

        next    :   int 
                    Number of next x-variable that will be generated
        
        r       :   int
                    Number of the round in which we are currently

        j       :   list
                    variables used for the new long constraint

        S       :   list
                    list in which variables are saved that are needed temporarily

        Returns:
        --------
        A       :   list
                    names of all variables in this current round

        M       :   scr_matrix
                    the matrix in which all the constraints are saved

        V       :   list
                    list of all the variablenames to date

        line    :   int
                    Index of row where we are currently

        next    :   int 
                    Number of next x-variable that will be generated

        S       :   list
                    list in which variables are saved that are needed temporarily
        """
        V.append("x"+str(next))
        V.append("d"+ str(9*r+Enocoro.rangenumber(A).index(e)))
        if len(e)==3:
            M[line,V.index(e[0])]=1
            if e[1][0]=="x": M[line,V.index(e[1])]=1
            else: M[line,V.index(S[int(e[1])])]=1
            M[line,len(V)-2]=1
            M[line,len(V)-1]=-2
            if type(e[2])==int:
                A[e[2]]="x"+str(next)
            else:
                S[int(e[2])]="x"+str(next)
            next+=1
        else:
            V.append("x"+str(next+1))
            M[line,V.index(S[e[0]])]=1
            M[line,V.index(S[e[1]])]=1
            M[line,len(V)-3]=1
            M[line,len(V)-1]=1
            M[line,len(V)-2]=-3
            #here we dont need to check if we assign it to S or A 
            S[int(e[2])]="x"+str(next)
            S[int(e[3])]="x"+str(next+1)
            next=next+2
        return A, M, V, line, next, S

    def shift_before(A):
        """
        In Enocoro, at the beginning of a round the bits are not shifted so this does nothing
        """
        return A

    def shift_after(A):
        """"
        This function shifts all the bits used in the current round to the right.

        Parameters:
        ----------
        A   :   list
                current variables
            
        Returns:
        ---------
        A   :   list
                shifted variables that can be used for the next round
        """
        la=A[31]
        for i in range(30,-1,-1):
            temp = A[i]
            A[i+1]=temp
        A[0]=la
        return A

    def initialize(rounds):
        """
        Generates initialization and all neded structures for Enocoro and specified number of rounds.

        Parameters:
        ---------
        rounds  :   int
                    number of rounds for the cipher

        Returns:
        ---------
        A       :   list
                    names of all variables in this current round
        
        M       :   scr_matrix
                    the empty constraint matrix for the MILP

        V       :   list
                    this list saves all the variables

        next    :   int 
                    number for the next x-variable
        """
        next=0
        M = csr_matrix((37*rounds,34+19*rounds),dtype=int)
        V = []
        #Array mit den Bits die momentan in der Cipher sind
        A=[]
        for e in range(34):
            A.append("x"+str(next))
            V.append("x"+str(next))
            next+=1
        return A, M, V, next

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
    
def new_generate_constraints(rounds, cipher):
    """
    This function generates the constraint matrix for a number of rounds of a given cipher.

    Parameters:
    ----------
    rounds  :   int
                number of rounds the cipher should go through

    cipher  :   class  
                cipher for which we generate the matrix

    Returns:
    -----------
    M       :   csr_matrix
                generated constraint matrix for the MILP
    """
    line=0
    A, M, V, next = cipher.initialize(rounds)
    for r in range(rounds):
        A=cipher.shift_before(A)
        S = [0,0,0,0]
        for j in cipher.rangenumber(A):
            A, M, V, line, next, S = cipher.gen_long_constraint(A, M, V, line, next, r, j, S)
            M, line = generate_smallconstraints(M, line)
            line+=1
        A = cipher.shift_after(A)
    return M


print(new_generate_constraints(3,Aes))

#print(enocoro(1))
#print(aes(3))