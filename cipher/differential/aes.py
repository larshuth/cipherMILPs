from cipher.cipher import Cipher
from scipy import lil_matrix

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
        self.round_number += 1
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
        super().__init__(rounds, orientation=8)
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