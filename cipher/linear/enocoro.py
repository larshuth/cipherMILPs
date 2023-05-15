from cipher.cipher import Cipher
from scipy.sparse import lil_matrix


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
        return [[self.A[31], self.A[32], "0"], [0, self.A[33], "2", "3"], [self.A[2], "0", 2], [self.A[6], 2, 6],
                [self.A[7], self.A[33], 7],
                [self.A[15], 7, 15], [self.A[16], "2", 16], [self.A[28], 16, 28], [self.A[29], "3", 29]]

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
        self.V.append("d" + str(9 * r + self.rangenumber(self.A).index(e)))
        if self.rangenumber(self.A).index(e) == 8:
            self.A[32] = self.S[2]
            self.A[33] = self.S[3]
        if len(e) == 3:
            self.M[line, self.V.index(e[0])] = 1
            if type(e[1]) == int:
                self.M[line, self.V.index(self.A[e[1]])] = 1
            elif e[1][0] == "x":
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
            self.M[line, self.V.index(e[1])] = 1
            self.M[line, len(self.V) - 3] = 1
            self.M[line, len(self.V) - 1] = 1
            self.M[line, len(self.V) - 2] = -3
            # here we dont need to check if we assign it to S or A
            self.S[int(e[2])] = "x" + str(self.next)
            self.S[int(e[3])] = "x" + str(self.next + 1)
            self.next = self.next + 2

        # updating the last constraint
        indicesofsboxinput = Enocorolin.input_sbox(r + 1)  # plus one so that the last round isnt missing

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
        tmp = self.A[31]
        for i in range(30, -1, -1):
            self.A[i + 1] = self.A[i]
        self.A[0] = tmp
        self.round_number += 1
        return

    def __init__(self, rounds):
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
        super().__init__(rounds, orientation=8)

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

