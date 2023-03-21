import numpy as np
from scipy.sparse import csr_matrix, lil_matrix


# If a new cipher is added, do not forget to add it to the list stored in the AVAILABLE variable at the end of the file.


class Cipher:
    """
    Superclass for better readability in code
    """

    def __init__(self, rounds=1, orientation=1):
        self.S = [0, 0, 0, 0]
        self.rounds = rounds
        self.orientation = orientation
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
            #
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


class LBlock(Cipher):
    """
    Class in which all functions for LBlock cipher [Wu et al 2011] are defined.
    """

    def rangenumber(self):
        """
        Defines what happens in a round.

        Parameters:
        ----------
        A   :   list
                Names of all variables in this current round

        Returns:
        ----------
            :   list of lists
                Specifies which variables belong in the constraint
        """
        # actions contain lists of either xors ['xor', input 1, input 2, output, dummy var],
        # 3-way forks ['3wf', input, output 1, output 2, dummy var], sboxes ['sbox', input start number, output start number, dummy var]
        words_total = int(64 / self.orientation)
        words_half = int(words_total / 2)

        if self.cryptanalysis_type == 'differential':
            if self.orientation == 1:
                # sboxes are now required
                new_x_variables_per_round = 96  # 32 var for xor (1st half plaintext, key)
                new_xor_dummies_per_round = 64  # 32 var for xor (1st half plaintext, key)

                # 32 var for Sbox (xor output), 32 var for xor (sbox output, 2nd half plaintext)
                # TODO: Grafik die das vernünftig /erklärt
                actions = [
                    ['xor',
                     self.A[i],
                     self.K[i],
                     'x' + str(int(self.A[i][1:]) + int(words_half)),
                     'd' + str((self.round_number - 1) * new_xor_dummies_per_round + i)
                     ] for i in range(words_half)]
                for i in range(8):
                    actions += [['sbox',
                                 new_x_variables_per_round * self.round_number - words_half + i * 4,
                                 new_x_variables_per_round * self.round_number + i * 4,
                                 'a' + str(int(self.A[i][1:]) + int(words_half))]]
            else:
                new_x_variables_per_round = words_total  # 32 var for xor (1st half plaintext, key)
                new_xor_dummies_per_round = words_total  # 32 var for xor (1st half plaintext, key)
                actions = [
                    ['xor',     # category
                     'x' + str(new_x_variables_per_round * self.round_number + i),
                     self.A[words_half + index],  # input var
                     'x' + str(int(self.A[i][1:]) + words_total),    # output var
                     'd' + str((self.round_number - 1) * new_xor_dummies_per_round + 32 + i)    # dummy var
                     ] for i, index in enumerate(range(words_half))]

        elif self.cryptanalysis_type == 'linear':
            # TODO: Linear Cryptanalysis
            actions = [['3wf', self.A[i], self.round_number] for i in range(int(64 / self.orientation))]

        print(actions)
        return actions

    def gen_long_constraint(self, line, e):
        """
        Generates a long constraint depending on which variable is currently j.
        For Enocoro we take the first variables in j. With the last one, we use it to define it new
        """
        sbox_bijective = True
        sbox_invertible = True
        sbox_branchnumber = 2

        if e[0] == 'xor':
            # inequalities of xor are
            # (1.) input1 + input2 + output \leq 2*dummy
            # (2.) input1 \leq dummy
            # (3.) input2 \leq dummy
            # (4.) output \leq dummy
            input_var_1 = e[1]
            input_var_2 = e[2]
            output_var = e[3]
            dummy_var = e[4]
            input_var_1_pos_in_matrix = self.V[input_var_1]
            input_var_2_pos_in_matrix = self.V[input_var_2]
            output_var_pos_in_matrix = self.V[output_var]
            dummy_var_pos_in_matrix = self.V[dummy_var]

            # starting with (1.)
            self.M[line, input_var_1_pos_in_matrix] = 1
            self.M[line, input_var_2_pos_in_matrix] = 1
            self.M[line, output_var_pos_in_matrix] = 1
            self.M[line, dummy_var_pos_in_matrix] = -2
            line += 1

            # then (2.), (3.), and (4.)
            self.M[line, input_var_1_pos_in_matrix] = 1
            self.M[line, dummy_var_pos_in_matrix] = -1
            line += 1

            self.M[line, input_var_2_pos_in_matrix] = 1
            self.M[line, dummy_var_pos_in_matrix] = -1
            line += 1

            self.M[line, output_var_pos_in_matrix] = 1
            self.M[line, dummy_var_pos_in_matrix] = -1
            line += 1
        elif e[0] == 'sbox':
            # inequalities of sbox are
            # (1.) input \leq dummy for all inputs
            # (2.) sum over all inputs \geq dummy
            # (3.) if sbox bijective: sum_{i \in all_inputs}
            # (4.) if the sbox invertible with branch number 2:
            # (4.1) sum over inputs + sum over outputs \geq branch * new dummy
            # (4.2) input \leq new dummy for all inputs
            # (4.3) output \leq dummy for all outputs

            sbox_input_size = 4
            sbox_output_size = 4
            input_vars = ['x' + str(e[1] + i) for i in range(sbox_input_size)]
            output_vars = ['x' + str(e[2] + i) for i in range(sbox_output_size)]
            dummy_var = e[3]
            dummy_var_pos_in_matrix = self.V[dummy_var]

            # starting with (1.)
            for i in input_vars:
                input_var_pos_in_matrix = self.V[i]
                self.M[line, input_var_pos_in_matrix] = 1
                self.M[line, dummy_var_pos_in_matrix] = -1
                line += 1

            # then (2.)
            for i in input_vars:
                input_var_pos_in_matrix = self.V[i]
                self.M[line, input_var_pos_in_matrix] = -1
            self.M[line, dummy_var_pos_in_matrix] = 1
            line += 1

            # then (3.)
            if sbox_bijective:
                for i in input_vars:
                    input_var_pos_in_matrix = self.V[i]
                    self.M[line, input_var_pos_in_matrix] = sbox_input_size
                for o in output_vars:
                    output_var_pos_in_matrix = self.V[o]
                    self.M[line, output_var_pos_in_matrix] = -1
                line += 1

                for i in input_vars:
                    input_var_pos_in_matrix = self.V[i]
                    self.M[line, input_var_pos_in_matrix] = -1
                for o in output_vars:
                    output_var_pos_in_matrix = self.V[o]
                    self.M[line, output_var_pos_in_matrix] = sbox_output_size
                line += 1
            # and finally (4.) sbox invertible with branch number 2
            if (not sbox_invertible) or (not (sbox_branchnumber <= 2)):
                pass
                # TODO for when it comes up
                # Make a new dummy
                # (4.1) sum over inputs + sum over outputs \geq branch * new dummy
                # (4.2) input \leq new dummy for all inputs
                # (4.3) output \leq dummy for all outputs

        return line

    def shift_before(self):
        # in X0, there is a 8 bit shift to the left
        # pos is a short function to return  the proper position depending on whether we model LBlock as 4-bit word oriented of just bit oriented
        pos = lambda x: int(x / self.orientation)
        tmp = [self.A[pos(32 + i)] for i in range(pos(32))]
        for i in range(pos(32), pos(56)):
            self.A[i] = self.A[i + pos(8)]
        for i, index in enumerate(range(pos(56), pos(64))):
            self.A[i] = tmp[index]
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
        if self.orientation == 1:
            for i in range(32, 64):
                self.A[i] = self.A[i-32]

            if self.round_number == 1:
                bonus = 32
            else:
                bonus = 0

            for i in range(32):
                self.A[i] = 'x' + str(i + 96 + bonus)
        return

    def __init__(self, rounds=32, model_as_bit_oriented=False):
        """
        Generates initialization and all needed structures for LBlock and specified number of rounds.

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
        if model_as_bit_oriented:
            super().__init__(rounds, orientation=1)
        else:
            super().__init__(rounds, orientation=4)

        inputsize = 64

        self.cryptanalysis_type = 'differential'

        # Summary of what's happening in LBlock:
        #   1. Teile Input in vordere Hälfte X_1, hintere Hälfte X_0
        #   2. Get subkey K_1 von K, bitshift X_0 <<< 8
        #   3. Round function mit X_1 und K_1 = F_1
        #   4. X_0 xor F_1
        #   5. X_1 und X_0 tauschen
        #   6. That was 1 round, now repeat 32 times

        # self.next = number of currently used (x) variable
        self.next = 0
        # self.M = matrix representing the linear inequalities

        # with mouha, every round, there are
        #   1 dummy + 1 output per XOR, 1 dummy per linear transformation, dummy + 2 output per 3-way fork,
        #   and 1 dummy + v output per w*v sbox
        #   4 inequalities per XOR
        #   2*l + 1 inequalities per linear transformation L: F_2^l -> F_2^l
        #   4 per 3-fork branch
        # Das Nicky Paper war byte-oriented (e.g. 32 byte input in Enocoro) während das
        # Sun Paper bit-oriented ist (e.g. 64 bit input in LBlock)
        # with sun, every round there are:
        #   1 + w constraints are necessary for all (w*v)-sboxes
        #   2 more are needed if the sbox is symmetric
        #   w + v + 1 more, redundant if the sbox invertible with branch number 2

        # we could implement different fine-graining of the xors, right now we are treating them as 4-bit word xors
        xors_per_round = 16
        xor_variables_per_round = xors_per_round
        xor_constraints_per_round = 7 * xors_per_round

        # there are no linear transformations in LBlock
        lt_per_round = 16
        lt_variables_per_round = xors_per_round
        lt_constraints_per_round = 7 * xors_per_round

        # TODO: Find out LBLOCK SBox Branch Number
        sbox_branch_number_equals_2 = True

        sboxes_per_round = 8

        if self.orientation == 1:
            sbox_dummy_variables_per_round = sboxes_per_round
            sbox_output_variables_per_round = 4 * sboxes_per_round
            sbox_variables_per_round = sbox_dummy_variables_per_round + sbox_output_variables_per_round
            sbox_constraints_per_round = 7 * sboxes_per_round + sbox_branch_number_equals_2 * 9

        else:
            sbox_variables_per_round = 0
            sbox_constraints_per_round = 0

        # we order M by: x variables (cipher bits), d dummy variables (xor), a dummy variables (bit oriented sboxes),
        # linear transformation dummy variables, the 1 constant
        # self.M is lil_matrix((#constraints, #variables), dtype=int) with lil_matrix coming from the SciPy package
        self.M = lil_matrix((
            (xor_constraints_per_round + sbox_constraints_per_round + lt_constraints_per_round) * self.rounds + 1, (
                    inputsize / self.orientation + (
                    inputsize / self.orientation + xor_variables_per_round + sbox_variables_per_round + lt_variables_per_round) * self.rounds) + 1),
            dtype=int)

        # self.V = dict of all variables mapping names to entry in self.M
        self.V = {'x' + str(i): i for i in range(int(inputsize / self.orientation) * (self.rounds + 1))}

        self.V['constant'] = self.M.get_shape()[1] - 1

        # list mit den Bits die momentan in der Cipher sind
        self.A = ['x' + str(i) for i in range(int(inputsize / self.orientation))]

        if model_as_bit_oriented:
            sbox_dummy_variables = ["a" + str(i) for i in range(sboxes_per_round * self.rounds)]
            for sbox_dummy, index in enumerate(sbox_dummy_variables):
                self.V[sbox_dummy] = 64 * (self.rounds + 1) + xor_variables_per_round * self.rounds + index
        else:
            for round in range(1, self.rounds + 1):
                sbox_dummy_variables = ["x" + str(i) for i in range(16 * round, 16 * (round + 1))]

        # making sure we have at least one active sbox (minimizing active sboxes to zero is possible)
        for sbox_dummy in sbox_dummy_variables:
            self.M[self.M.get_shape()[0] - 1, self.V[sbox_dummy]] = 1
        self.M[self.M.get_shape()[0] - 1, self.V['constant']] = -1

        self.round_number = 0
        return


class CipherTemplate(Cipher):
    def __init__(self, rounds=1):
        super().__init__(rounds)
        # self.next = number of currently used (x) variable
        self.next = 0

        # with mouha, every round, there are
        #   1 dummy per XOR, 1 dummy per linear transformation, and 1 dummy per sbox
        #   k + 1 inequalities per k-XOR
        #   2*l + 1 inequalities per linear transformation L: F_2^l -> F_2^l
        #   4 per 3-fork branch
        # Das Nicky Paper war byte-oriented (e.g. 32 byte input in Enocoro) während das
        # Sun Paper bit-oriented ist (e.g. 64 bit input in LBlock)
        # with sun, every round there are:
        #   1 + w constraints are necessary for all (w*v)-sboxes
        #   2 more are needed if the sbox is symmetric
        #   w + v + 1 more if the sbox does not have branch number 2 or is not invertible
        # self.M = matrix representing the linear inequalities

        self.M = lil_matrix((64 * self.rounds + 1, (64 + 19 * self.rounds) + 1), dtype=int)
        # self.V = ist of all variables
        self.V = []
        # list mit den Bits die momentan in der Cipher sind
        self.A = []
        indicesofsboxinput = self.input_sbox()
        # create variable for input (plaintext) bits/bytes/word, depending on how the cipher is oriented
        input_words = 64
        for e in range(input_words):
            self.A.append("x" + str(self.next))
            self.V.append("x" + str(self.next))
            if self.next in indicesofsboxinput:
                self.M[self.M.get_shape()[0] - 1, self.next] = 1
            self.next += 1
        self.M[self.M.get_shape()[0] - 1, self.M.get_shape()[1] - 1] = -1
        return


AVAILABLE = [Enocoro, Aes, LBlock]
BIT_ORIENTED = [LBlock]
