import numpy as np
from scipy.sparse import csr_matrix, lil_matrix


# If a new cipher is added, do not forget to add it to the list stored in the AVAILABLE variable at the end of the file.


class Cipher:
    """
    Superclass for better readability in code
    """

    def __init__(self, rounds=1):
        self.S = [0, 0, 0, 0]
        self.rounds = rounds
        return


class Aes(Cipher):
    """
    Class in which all functions for AES are defined.
    """

    def rangenumber(self):
        """
        Defines how often we need to call gen_long_constraint.

        Returns:
        ----------
        The range for generating long constraints.
        """
        return range(4)

    def gen_long_constraint(self, line, r, j):
        """
        Generates a long constraint depending on which variable is currently j.
        For AES, it is just the current column and the new variables.
        (A part of mixColumn)

        Parameters:
        ----------
        line    :   int
                    Index of row where we are currently

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
            ind = self.V.index(self.A[i][j])
            self.M[line, ind] = 1
            # last constraint
            self.M[self.M.get_shape()[0] - 1, ind] = 1
        for i in range(4):
            # every new variable added to the constraint and to V
            self.V.append("x" + str(self.next + i))
            self.A[i][j] = "x" + str(self.next + i)
            self.M[line, len(self.V) - 1] = 1
        self.next += 4
        self.V.append("d" + str(r * 4 + j))
        self.M[line, len(self.V) - 1] = -5
        return line

    def shift_before(self):
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
                tmp[j] = self.A[i][(j + i) % 4]
            for j in range(0, 4):
                self.A[i][j] = tmp[j]
        return

    def shift_after(self):
        """
        In AES the bits do not change after one round so this function does nothing.
        """
        pass
        return

    def __init__(self, rounds=1):
        """
        Generates initialization and all neded structures for AES and specified number of rounds.

        Parameters:
        ---------
        rounds  :   int
                    Number of rounds for the cipher

        Returns:
        ---------
        Creates Instance, no return value
        """
        # TODO: Generalization of numbers in self.M definition to take it into class cipher
        super().__init__(rounds)
        self.M = lil_matrix((36 * self.rounds + 1, (16 + 20 * self.rounds) + 1), dtype=int)
        self.V = []
        self.A = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.next = 0
        for i in range(4):
            for j in range(4):
                self.A[i][j] = "x" + str(self.next)
                self.V.append("x" + str(self.next))
                self.next += 1
        self.M[self.M.get_shape()[0] - 1, self.M.get_shape()[1] - 1] = -1
        return

    def input_sbox(self, rounds):
        """
        all variable indices of variables that are input of an sbox
        """
        inputsbox = []  # wo fangen variablen nochmal an? kontrollieren!
        for i in range((self.rounds * 16)):
            inputsbox.append(i)
        return inputsbox


class Enocoro(Cipher):
    """
    Class in which all functions for Enocoro are defined.
    """

    def rangenumber(self):
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
        return [[self.A[31], self.A[32], 31], [self.A[32], self.A[2], "0"], [self.A[33], self.A[7], "1"],
                [0, 1, "2", "3"], [self.A[16], "2", 32], [self.A[29], "3", 33], [self.A[2], self.A[6], 2],
                [self.A[7], self.A[15], 7], [self.A[16], self.A[28], 16]]

    def gen_long_constraint(self, line, r, e):
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
        self.V.append("x" + str(self.next))
        self.V.append("d" + str(9 * r + self.rangenumber().index(e)))
        if len(e) == 3:
            self.M[line, self.V.index(e[0])] = 1
            if e[1][0] == "x":
                self.M[line, self.V.index(e[1])] = 1
            else:
                self.M[line, self.V.index(self.S[int(e[1])])] = 1
            self.M[line, len(self.V) - 2] = 1
            self.M[line, len(self.V) - 1] = -2
            if type(e[2]) == int:
                self.A[e[2]] = "x" + str(self.next)
            else:
                self.S[int(e[2])] = "x" + str(self.next)
            self.next += 1
        else:
            self.V.append("x" + str(self.next + 1))
            self.M[line, self.V.index(self.S[e[0]])] = 1
            self.M[line, self.V.index(self.S[e[1]])] = 1
            self.M[line, len(self.V) - 3] = 1
            self.M[line, len(self.V) - 1] = 1
            self.M[line, len(self.V) - 2] = -3
            # here we dont need to check if we assign it to S or A
            self.S[int(e[2])] = "x" + str(self.next)
            self.S[int(e[3])] = "x" + str(self.next + 1)
            self.next += 2

        # updating the last constraint
        indicesofsboxinput = self.input_sbox()
        for i in indicesofsboxinput:
            if "x" + str(i) in self.V:
                self.M[self.M.get_shape()[0] - 1, self.V.index("x" + str(i))] = 1
        return line

    def shift_before(self):
        """
        In Enocoro, at the beginning of a round the bits are not shifted so this does nothing
        """
        pass
        return

    def shift_after(self):
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
        la = self.A[31]
        for i in range(30, -1, -1):
            temp = self.A[i]
            self.A[i + 1] = temp
        self.A[0] = la
        return

    def __init__(self, rounds=1):
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
        super().__init__(rounds)

        self.next = 0
        self.M = lil_matrix((37 * self.rounds + 1, (34 + 19 * self.rounds) + 1), dtype=int)
        self.V = []
        # Array mit den Bits die momentan in der Cipher sind
        self.A = []
        indicesofsboxinput = self.input_sbox()
        for e in range(34):
            self.A.append("x" + str(self.next))
            self.V.append("x" + str(self.next))
            if self.next in indicesofsboxinput:
                self.M[self.M.get_shape()[0] - 1, self.next] = 1
            self.next += 1
        self.M[self.M.get_shape()[0] - 1, self.M.get_shape()[1] - 1] = -1
        return

    def input_sbox(self):
        inputsbox = []
        for i in range(self.rounds):
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


AVAILABLE = [Enocoro, Aes]
