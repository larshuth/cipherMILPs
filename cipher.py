import numpy as np
from scipy.sparse import csr_matrix, lil_matrix


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

        M       :   lil_matrix
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
                    Very unnecessary, I have to see if I can delete it

        Returns:
        --------
        A       :   list of lists
                    4x4 matrix where the new names of the variables are saved

        M       :   lil_matrix
                    The matrix in which all the constraints are saved

        V       :   list
                    List of all the variablenames to date

        line    :   int
                    Index of row where we are currently

        next    :   int 
                    Number of next x-variable that will be generated

        S       :   list of lists
                    Very unnecessary, I have to see if I can delete it
        """
        for i in range(4):
            # evey element in column is added to the constraint
            ind = V.index(A[i][j])
            M[line, ind] = 1
            # last constraint
            M[M.get_shape()[0] - 1, ind] = 1
        for i in range(4):
            # every new variable added to the constraint and to V
            V.append("x" + str(next + i))
            A[i][j] = "x" + str(next + i)
            M[line, len(V) - 1] = 1
        next = next + 4
        V.append("d" + str(r * 4 + j))
        M[line, len(V) - 1] = -5
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
        tmp = [0, 0, 0, 0]
        for i in range(0, 4):
            for j in range(0, 4):
                tmp[j] = A[i][(j + i) % 4]
            for j in range(0, 4):
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
                    Number of rounds for the cipher

        Returns:
        ---------
        A       :   list of lists
                    4x4 matrix where the names of the current variables are saved
        
        M       :   lil_matrix
                    The empty constraint matrix for the MILP

        V       :   list
                    This list saves all the variables

        next    :   int 
                    Number for the next x-variable
        """
        M = lil_matrix((36 * rounds + 1, (16 + 20 * rounds) + 1), dtype=int)
        V = []
        A = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        next = 0
        for i in range(4):
            for j in range(4):
                A[i][j] = "x" + str(next)
                V.append("x" + str(next))
                next = next + 1
        M[M.get_shape()[0] - 1, M.get_shape()[1] - 1] = -1
        return A, M, V, next

    def input_sbox(rounds):
        """
        all variable indices of variables that are input of an sbox
        """
        inputsbox = []  # wo fangen variablen nochmal an? kontrollieren!
        for i in range((rounds * 16)):
            inputsbox.append(i)
        return inputsbox


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
                Names of all variables in this current round

        Returns:
        ----------
            :   list of lists
                Specifies which variables belong in the constraint
        """
        return [[A[31], A[32], 31], [A[32], A[2], "0"], [A[33], A[7], "1"], [0, 1, "2", "3"], [A[16], "2", 32],
                [A[29], "3", 33], [A[2], A[6], 2], [A[7], A[15], 7], [A[16], A[28], 16]]

    def gen_long_constraint(A, M, V, line, next, r, e, S):
        """
        Generates a long constraint depending on which variable is currently j.
        For Enocoro we take the first variables in j. With the last one, we use it to define it new 

        Parameters:
        ----------
        A       :   list
                    Names of all variables in this current round

        M       :   lil_matrix
                    The matrix in which all the constraints are saved

        V       :   list
                    List of all the variablenames to date

        line    :   int
                    Index of row where we are currently

        next    :   int 
                    Number of next x-variable that will be generated
        
        r       :   int
                    Number of the round in which we are currently

        j       :   list
                    Variables used for the new long constraint

        S       :   list
                    List in which variables are saved that are needed temporarily

        Returns:
        --------
        A       :   list
                    Names of all variables in this current round

        M       :   lil_matrix
                    The matrix in which all the constraints are saved

        V       :   list
                    List of all the variablenames to date

        line    :   int
                    Index of row where we are currently

        next    :   int 
                    Number of next x-variable that will be generated

        S       :   list
                    List in which variables are saved that are needed temporarily
        """
        V.append("x" + str(next))
        V.append("d" + str(9 * r + Enocoro.rangenumber(A).index(e)))
        if len(e) == 3:
            M[line, V.index(e[0])] = 1
            if e[1][0] == "x":
                M[line, V.index(e[1])] = 1
            else:
                M[line, V.index(S[int(e[1])])] = 1
            M[line, len(V) - 2] = 1
            M[line, len(V) - 1] = -2
            if type(e[2]) == int:
                A[e[2]] = "x" + str(next)
            else:
                S[int(e[2])] = "x" + str(next)
            next += 1
        else:
            V.append("x" + str(next + 1))
            M[line, V.index(S[e[0]])] = 1
            M[line, V.index(S[e[1]])] = 1
            M[line, len(V) - 3] = 1
            M[line, len(V) - 1] = 1
            M[line, len(V) - 2] = -3
            # here we dont need to check if we assign it to S or A
            S[int(e[2])] = "x" + str(next)
            S[int(e[3])] = "x" + str(next + 1)
            next = next + 2

        # updating the last constraint
        indicesofsboxinput = Enocoro.input_sbox(r + 1)
        for i in indicesofsboxinput:
            if "x" + str(i) in V:
                M[M.get_shape()[0] - 1, V.index("x" + str(i))] = 1
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
                Current variables
            
        Returns:
        ---------
        A   :   list
                Shifted variables that can be used for the next round
        """
        la = A[31]
        for i in range(30, -1, -1):
            temp = A[i]
            A[i + 1] = temp
        A[0] = la
        return A

    def initialize(rounds):
        """
        Generates initialization and all neded structures for Enocoro and specified number of rounds.

        Parameters:
        ---------
        rounds  :   int
                    Number of rounds for the cipher

        Returns:
        ---------
        A       :   list
                    Names of all variables in this current round
        
        M       :   lil_matrix
                    The empty constraint matrix for the MILP

        V       :   list
                    This list saves all the variables

        next    :   int 
                    Number for the next x-variable
        """
        next = 0
        M = lil_matrix((37 * rounds + 1, (34 + 19 * rounds) + 1), dtype=int)
        V = []
        # Array mit den Bits die momentan in der Cipher sind
        A = []
        indicesofsboxinput = Enocoro.input_sbox(rounds)
        for e in range(34):
            A.append("x" + str(next))
            V.append("x" + str(next))
            if next in indicesofsboxinput:
                M[M.get_shape()[0] - 1, next] = 1
            next += 1
        M[M.get_shape()[0] - 1, M.get_shape()[1] - 1] = -1
        return A, M, V, next

    def input_sbox(rounds):
        inputsbox = []
        for i in range(rounds):
            # first sbox
            if i < 3:
                inputsbox.append((2 - i))
            else:
                inputsbox.append(34 + (i - 3) * 10)
            # second sbox
            if i < 5:
                inputsbox.append(7 - i)
            else:
                inputsbox.append(41 + (i - 5) * 10)
            # third sbox
            if i < 9:
                inputsbox.append(16 - i)
            else:
                inputsbox.append(42 + (i - 9) * 10)
            # fourth sbox
            if i < 13:
                inputsbox.append(29 - i)
            else:
                inputsbox.append(43 + (i - 13) * 10)
        return inputsbox


class Enocorolin:
    """
    Class in which all functions for Enocoro are defined.
    """

    def rangenumber(A):
        """
        Defines what to go through in the for loop for gen_long_constraint.

        Parameters:
        ----------
        A   :   list
                Names of all variables in this current round

        Returns:
        ----------
            :   list of lists
                Specifies which variables belong in the constraint
        """
        return [[A[31], A[32], "0"], [0, A[33], "2", "3"], [A[2], "0", 2], [A[6], 2, 6], [A[7], A[33], 7],
                [A[15], 7, 15], [A[16], "2", 16], [A[28], 16, 28], [A[29], "3", 29]]

    def gen_long_constraint(A, M, V, line, next, r, e, S):
        """
        Generates a long constraint depending on which variable is currently j.
        For Enocoro we take the first variables in j. With the last one, we use it to define it new 

        Parameters:
        ----------
        A       :   list
                    Names of all variables in this current round

        M       :   lil_matrix
                    The matrix in which all the constraints are saved

        V       :   list
                    List of all the variablenames to date

        line    :   int
                    Index of row where we are currently

        next    :   int 
                    Number of next x-variable that will be generated
        
        r       :   int
                    Number of the round in which we are currently

        j       :   list
                    Variables used for the new long constraint

        S       :   list
                    List in which variables are saved that are needed temporarily

        Returns:
        --------
        A       :   list
                    Names of all variables in this current round

        M       :   lil_matrix
                    The matrix in which all the constraints are saved

        V       :   list
                    List of all the variablenames to date

        line    :   int
                    Index of row where we are currently

        next    :   int 
                    Number of next x-variable that will be generated

        S       :   list
                    List in which variables are saved that are needed temporarily
        """
        V.append("x" + str(next))
        V.append("d" + str(9 * r + Enocorolin.rangenumber(A).index(e)))
        if Enocorolin.rangenumber(A).index(e) == 8:
            A[32] = S[2]
            A[33] = S[3]
        if len(e) == 3:
            M[line, V.index(e[0])] = 1
            if type(e[1]) == int:
                M[line, V.index(A[e[1]])] = 1
            elif e[1][0] == "x":
                M[line, V.index(e[1])] = 1
            else:
                M[line, V.index(S[int(e[1])])] = 1
            M[line, len(V) - 2] = 1
            M[line, len(V) - 1] = -2
            if type(e[2]) == int:
                A[e[2]] = "x" + str(next)
            else:
                S[int(e[2])] = "x" + str(next)
            next += 1
        else:
            V.append("x" + str(next + 1))
            M[line, V.index(S[e[0]])] = 1
            M[line, V.index(e[1])] = 1
            M[line, len(V) - 3] = 1
            M[line, len(V) - 1] = 1
            M[line, len(V) - 2] = -3
            # here we dont need to check if we assign it to S or A
            S[int(e[2])] = "x" + str(next)
            S[int(e[3])] = "x" + str(next + 1)
            next = next + 2

        # updating the last constraint
        indicesofsboxinput = Enocorolin.input_sbox(r + 1)  # plus one so that the last round isnt missing

        for i in indicesofsboxinput:
            if "x" + str(i) in V:
                M[M.get_shape()[0] - 1, V.index("x" + str(i))] = 1
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
                Current variables
            
        Returns:
        ---------
        A   :   list
                Shifted variables that can be used for the next round
        """
        la = A[31]
        for i in range(30, -1, -1):
            temp = A[i]
            A[i + 1] = temp
        A[0] = la
        return A

    def initialize(rounds):
        """
        Generates initialization and all neded structures for Enocoro and specified number of rounds.

        Parameters:
        ---------
        rounds  :   int
                    Number of rounds for the cipher

        Returns:
        ---------
        A       :   list
                    Names of all variables in this current round
        
        M       :   lil_matrix
                    The empty constraint matrix for the MILP

        V       :   list
                    This list saves all the variables

        next    :   int 
                    Number for the next x-variable
        """
        next = 0
        M = lil_matrix((37 * rounds + 1, (34 + 19 * rounds) + 1), dtype=int)
        V = []
        # Array mit den Bits die momentan in der Cipher sind
        A = []
        indicesofsboxinput = Enocorolin.input_sbox(rounds)
        for e in range(34):
            A.append("x" + str(next))
            V.append("x" + str(next))
            if next in indicesofsboxinput:
                M[M.get_shape()[0] - 1, next] = 1
            next += 1
        M[M.get_shape()[0] - 1, M.get_shape()[1] - 1] = -1
        return A, M, V, next

    def input_sbox(rounds):
        inputsbox = []
        for i in range(rounds):
            # first sbox
            inputsbox.append(34 + (i) * 10)
            # second sbox
            if i == 0:
                inputsbox.append(33)
            else:
                inputsbox.append(36 + (i - 1) * 10)
            # third sbox
            inputsbox.append(35 + (i) * 10)
            # fourth sbox
            inputsbox.append(36 + (i) * 10)
        return inputsbox
