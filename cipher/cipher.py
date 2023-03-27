from scipy.sparse import lil_matrix
from differential.enocoro import Enocoro
from differential.aes import Aes
from differential.lblock import LBlock
from linear.enocoro import Enocorolin

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


class CipherTemplate(Cipher):
    # still a work in progress
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


AVAILABLE = [Enocoro, Enocorolin, Aes, LBlock]
BIT_ORIENTED = [LBlock]
