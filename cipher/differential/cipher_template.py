from cipher.cipher import Cipher
from cipher.sbox import SBox
from cipher.actions.permutationaction import PermutationAction
from cipher.actions.lineartransformationaction import LinTransformationAction
from cipher.actions.xoraction import XorAction
from cipher.actions.sboxaction import SBoxAction
from cipher.actions.overwriteaction import OverwriteAction


class Template(Cipher):
    """
    Template for a class in which all functions for some cipher would be defined.
    This template has been structured as follows:
    1. Functions which generate constraints by round, further divided into
        a. Functions generating actions using modules from cipherMILPS/cipher/actions
        b. Calling functions for generating and executing actions
    2. Initialization of everything required to generate said constraints

    Someone looking to implement a cipher within this framework should start out with 2. and then move on to the
    functions in 1., where again one should start with b. and only then continue on to b.
    """

    def generate_sbox_actions_for_round(self):
        # collect all sbox actions in a list ordered by when you want them to be performed
        list_of_sbox_actions = list()
        # now for every
        for index, sbox in enumerate(self.sboxes):
            sbox_input_vars = [self.A[index * 4 + var] for var in range(sbox.in_bits)]
            list_of_sbox_actions.append(SBoxAction(sbox=sbox, input_vars=sbox_input_vars, cipher_instance=self,
                                                   first_a_position_to_overwrite=index * 4))
        return list_of_sbox_actions

    def generate_permutation_actions_for_round(self):
        def new_position_of_x(x):
            return 4 * (x // 16) + 16 * ((3 * (x % 16 // 4) + x % 4) % 4) + x % 4

        permutation = [0 for _ in range(64)]

        for i in range(64):
            permutation[new_position_of_x(i)] = i

        list_of_permutation_actions = [PermutationAction(permutation, self)]
        return list_of_permutation_actions

    def generate_key_xor_actions_for_round(self):
        list_of_key_xor_actions = list()
        set_of_xor_positions = set([4 * i for i in range(16)] + [(4 * i) + 1 for i in range(16)])
        xors_so_far = 0
        for a_index, a_var in enumerate(self.A):
            if a_index in set_of_xor_positions:
                list_of_key_xor_actions.append(
                    XorAction((a_var, self.K[xors_so_far]), self, a_position_to_overwrite=a_index))
                xors_so_far += 1
        return list_of_key_xor_actions

    def generate_single_bit_xor_actions(self):
        list_of_single_bit_xor_actions = list()
        single_bit_xor_positions = [3, 7, 11, 15, 19, 23, self.plaintextsize - 1]
        for pos in single_bit_xor_positions:
            list_of_single_bit_xor_actions.append(LinTransformationAction([self.A[pos]], self, 1, [pos]))
        return list_of_single_bit_xor_actions

    def generate_equality_overwrite_actions(self):
        list_of_equality_overwrite_actions = list()
        set_of_xor_positions = {4 * i for i in range(16)} | {(4 * i) + 1 for i in range(16)}
        set_of_single_bit_xor_positions = {3, 7, 11, 15, 19, 23, self.plaintextsize - 1}
        list_of_equality_overwrite_positions = set(range(self.plaintextsize)) - (
                set_of_xor_positions | set_of_single_bit_xor_positions)
        list_of_equality_overwrite_actions = [
            OverwriteAction(list_of_equality_overwrite_positions, cipher_instance=self, equality=True)]
        return list_of_equality_overwrite_actions

    def run_round(self):
        print(f"Round {self.round_number} start")

        for sboxaction in self.generate_sbox_actions_for_round():
            sboxaction.run_action()

        for permutationsaction in self.generate_permutation_actions_for_round():
            permutationsaction.run_action()

        for keyaction in self.generate_key_xor_actions_for_round():
            keyaction.run_action()

        for single_bit_xor_action in self.generate_single_bit_xor_actions():
            single_bit_xor_action.run_action()

        if self.overwrite_equals:
            for equality_overwrite_action in self.generate_equality_overwrite_actions():
                equality_overwrite_action.run_action()

        self.K = ['k' + str(self.round_number * self.key_vars + i) for i in range(self.key_vars)]
        print(f"Round {self.round_number} end")
        self.round_number += 1
        return True

    def __init__(self, rounds=1, model_as_bit_oriented=True, cryptanalysis_type='differential',
                 type_of_modeling='SunEtAl 2013', **kwargs):
        """
        Generates initialization and all needed structures for AES and specified number of rounds.

        Parameters:
        ---------
        rounds  :   int
                    Number of rounds for the cipher

        Returns:
        ---------
        Creates Instance, no return value
        """
        # plaintesxt variables are the number of input as well as output bits (not sum, value each)
        # e.g. 64 in Gift64, 64 in LBlock, and 128 in AES
        plaintextsize = 0
        assert plaintextsize > 0

        # number of variables added per round iff the key is xored or the like
        keysize = 0

        # number of bits that make up one word if the analysis is not done bit-oriented,
        # e.g. 8 in byte oriented AES and 4 in nibble-oriented LBlock
        # not interesting for ciphers such as Gift64 which can not be analyzed non-bit-oriented
        word_size = 0

        ################################################################################################################
        # DEPENDING ON THE CIPHER AND FLEXIBILITY OF ANALYSES, IT IS RECOMMENDED ADD EITHER OF THE FOLLOWING BLOCKS
        ################################################################################################################
        if model_as_bit_oriented:
            orientation = 1
        else:
            orientation = word_size
        ################################################################################################################
        # add exception iff cipher can only be modeled bit-oriented
        if not model_as_bit_oriented:
            raise Exception(
                "CIPHER can only be called as bit-oriented, there is no word-orientation of word size > 1 available.")
        ################################################################################################################

        ################################################################################################################
        # ADD THE FOLLOWING BLOCK IF YOU HAVE NOT IMPLEMENTED ALL TYPES OF ANALYSES
        ################################################################################################################
        if cryptanalysis_type == 'linear':
            raise Exception("Template: Linear cryptanalysis has not been implemented for CIPHER.")
        elif cryptanalysis_type == 'differential':
            raise Exception("Template: Differential cryptanalysis has not been implemented for CIPHER.")
        else:
            raise Exception(
                f"Template: Call CIPHER with a valid type of cryptanalysis and not {str(cryptanalysis_type)}.")
        ################################################################################################################

        # calling the cipher class and establishing all previously already named variables as instance attributes
        super().__init__(rounds, plaintextsize, keysize, orientation=orientation, type_of_modeling=type_of_modeling,
                         cryptanalysis_type=cryptanalysis_type)

        ################################################################################################################

        self.overwrite_equals = kwargs['overwrite_equals']
        self.permutation_as_constraints = kwargs['permutation_as_constraints']

        # COUNT THE TYPES OF OPERATIONS PERFORMED AND ADD THEM BELOW. THIS EXAMPLE GOES INTO DETAIL BUT IF ONLY 1 TYPE
        # OF CRYPTANALYSIS IS OF INTEREST TO YOU, NO IF-CLAUSE ARE REQUIRED.

        # The calculations for the numbers of required variables and constraints are performed under the expectation of
        # uniform rounds. If your cipher is different, please open a github issue.

        # XORS
        # xors_per_round for the number of xors performed per round (if two bytes are xored that still counts as 8 xors)
        # extra_xors for the number of xors performed outside the regular number per round. E.g. AES has an extra key
        # xor-ing step in (or before) round 1 which would be counted here.
        if self.cryptanalysis_type == 'differential':
            xors_per_round = 32
            extra_xors = 0
        elif self.cryptanalysis_type == 'linear':
            # Linear cryptanalysis generally does not analyze xors. See Howard M Heys'
            # "A Tutorial on Linear and Differential Cryptanalysis" [http://www.cs.bc.edu/~straubin/crypto2017/heys.pdf]
            # as to why that is the case
            xors_per_round = 0
            extra_xors = 0
        else:
            xors_per_round = 0
            extra_xors = 0

        # THREE WAY FORKS (TWF)
        # twf_per_round for the number of forks performed per round (if a bytes s forked that still counts as 8 twfs)
        # extra_twfs for the number of forks performed outside the regular number per round.
        if self.cryptanalysis_type == 'differential':
            # Differential cryptanalysis generally does not analyze three-way forks. See Howard M Heys'
            # "A Tutorial on Linear and Differential Cryptanalysis" [http://www.cs.bc.edu/~straubin/crypto2017/heys.pdf]
            # as to why that is the case
            twf_per_round = 0
            extra_twfs = 0
        elif self.cryptanalysis_type == 'linear':
            twf_per_round = 0
            extra_twfs = 0
        else:
            twf_per_round = 0
            extra_twfs = 0

        # LINEAR TRANSFORMATIONS (LT)
        # Linear transformations are linear function applied to a number of input bits. E.g. AES' MIxColumns action
        # takes 4 bytes as input and gives 4 bytes as output. On the other hand, Gift64 flips bits, which can be seen as
        # the addition of a constant (i.e. 1) to a single bit input.

        # For lt_per_round we want a list of the number of in- and output variables per linear transformation performed.
        # Below as an example, would be a cipher which has
        # - a bit-flip and
        # - a multiplication over two bytes leading to a one byte output
        # performed over the course of a round
        lt_per_round = [(1, 1), (16, 8)]

        # S-BOXES
        # v*w Substitution-Boxes (aka S-Boxes) are mappings with v input bits and w output bits. A (non-linear) mapping
        # s: F_2^v -> F_2^w is then performed.

        # For self.sboxes, we want a list of SBox objects/instances with one entry per S-Box used. We recommend to use
        # the objects/instances call-by-reference as to save computational effort that would be redundant.

        # create a variable storing a dictionary mapping from input to output. Instead of bit-strings to bit-strings, we
        # map integer to integer. The number of input and output bits will be noted when creating an instance.

        # Examples of S-box creation
        sbox_gift_subs = {index: value for index, value in
                          enumerate(
                              [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14])}
        sbox1 = SBox(sbox_gift_subs, 4, 4, self, extract_sun_inequalities=self.extract_sun_inequalities)

        sbox2 = SBox(substitutions={0: 1, 1: 5, 2: 7, 3: 2, 4: 4, 5: 0, 6: 6, 7: 3}, in_bits=3, out_bits=3,
                     cipher_instance=self, extract_sun_inequalities=False)

        self.sboxes = [sbox1, sbox2]

        # OVERWRITES
        # This tool offers overwriting variables with new ones. Overwriting can be split into:
        # - equality overwrites, where for a variables x we just introduce a new (redundant) variable x' and the
        #   constraints x <= x' as well as x' <= x. This is used mostly for achieving nicer structures such as in Gift64
        #   and should according to Sebastian Berndt eb likely removed during the kernelization process (unsure if this
        #   counts as kernelization) of MILP solvers.
        # - independent overwrites, aka non-equality overwrites, which have been introduced for modeling in which a new
        #   variable x' takes over for a variable x but there are no connections between the previous and the new
        #   variable. This can also be used as a (horribly performing) catch-all for operations which are out of scope
        #   of being modeled by us/someone.

        # So far we have not encountered any cipher with independent overwrites, just used them in debugging so this
        # variable will likely stay 0
        non_equality_overwrites = 0

        # This is an example showing how the number of equality overwrites is calculated in Gift64 where we divide the
        # SPN cleanly into layers (S-boxes, permutations, xor+lt) and to do so use overwrite equals for all bits in the
        # xor+lt part which are not xored or flipped (linear transformation of (variable + 1) in F_2). As this number
        # changes depending on which type of cryptanalysis we are bounding -- there are no constraints for xors in
        # linear cryptanalysis and therefore more overwrites happen in that setting -- this is questioned.

        # Furthermore, just after the super.init call previously, we introduced self.overwrite_equals and
        # self.permutation_as_constraints using kwargs. This is in case someone is interested in flexibly creating the
        # different matrices which use and do not use the different optional constraints and variables

        if self.overwrite_equals:
            equality_overwrites = self.plaintext_vars - (xors_per_round + len(lt_per_round))
        else:
            equality_overwrites = 0

        # PERMUTATIONS
        # For permutations, we can, as stated just before, optionally use constraints. Say for example [x0, x1, x2, x3]
        # is permuted to [x1, x3, x0, x2], then we can either go through the effort of keeping track of these (and
        # convolute the matrix) or overwrite [x1, x3, x0, x2] with [x4, x5, x6, x7] and set constraints x1 <= x4 and
        # x4 <= x1, etc.
        if self.permutation_as_constraints:
            permutations = 64
        else:
            permutations = 0

        # key_variable_usage should be set to True if the variables corresponding to the key bits are used in any
        # constraints. Otherwise, it just results in empty columns so in case of doubt set to True.

        # In the following example, key variables are only used in xor constraints and therefore only in differential
        # cryptanalysis bounding.

        if self.cryptanalysis_type == 'differential':
            key_variable_usage = True
        elif self.cryptanalysis_type == 'linear':
            key_variable_usage = False
        else:
            key_variable_usage = True

        # Calling prepare_for_type_of_modeling from the "cipher" super class which simply constructs everything required
        # of the cipher's S-boxes for the chose analysis' bound
        self.prepare_for_type_of_modeling()

        # With all of these values set, we call calculate_vars_and_constraints from the "cipher" super class
        self.calculate_vars_and_constraints(xors_per_round, twf_per_round,
                                            lt_per_round, extra_xors, non_equality_overwrites, equality_overwrites,
                                            permutations=permutations, new_keys_every_round=True,
                                            keys_are_used=key_variable_usage)

        # CONSTRAINT TO AVOID THE TRIVIAL SOLUTION
        # In order to avoid the trivial solution

        # making sure we have at least one active sbox (minimizing active sboxes to zero is possible)
        # TODO: CHECK CORRECTNESS OF SUM OVER S-BOX DUMMY VARIABLES VS. INPUT NEQ ZERO
        sbox_dummy_variables = ["a" + str(i) for i in range(self.number_a_vars)]

        for sbox_dummy in sbox_dummy_variables:
            self.M[self.M.get_shape()[0] - 1, self.V[sbox_dummy]] = 1
        self.M[self.M.get_shape()[0] - 1, self.V['constant']] = -1

        # adding a set to include the matrices of possible convex hull
        self.sbox_inequality_matrices = list()

        self.line = 0
        self.round_number = 1
        return
