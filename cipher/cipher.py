from scipy.sparse import lil_matrix
from itertools import chain


class Cipher:
    """
    Superclass for better readability in code
    """

    def __init__(self, rounds=1, plaintextsize=1, keysize=0, orientation=1, type_of_modeling='SunEtAl 2013',
                 cryptanalysis_type='differential'):
        self.cryptanalysis_type = cryptanalysis_type

        self.S = [0, 0, 0, 0]
        self.rounds = rounds
        self.orientation = orientation

        self.plaintextsize = plaintextsize
        self.keysize = keysize

        self.sboxes = list()
        self.number_variables = 0

        self.number_x_vars = 0
        self.number_dx_vars = 0
        self.number_dt_vars = 0
        self.number_dl_vars = 0
        self.number_d_vars = self.number_dx_vars + self.number_dt_vars + self.number_dl_vars

        self.number_a_vars = 0
        self.number_ds_vars = 0

        self.number_qijp_vars = 0
        self.number_qijlp_vars = 0

        self.plaintext_vars = int(self.plaintextsize / self.orientation)
        self.key_vars = int(self.keysize / self.orientation)

        self.V = dict()
        self.M = None  # placeholder for completeness

        # list mit den Bits die momentan in der Cipher sind
        self.A = ['x' + str(i) for i in range(self.plaintext_vars)]
        self.K = ['k' + str(i) for i in range(self.key_vars)]

        self.next = {'dx': 0, 'dt': 0, 'dl': 0, 'k': int(self.keysize / self.orientation), 'a': 0, 'ds': 0,
                     'x': int(self.plaintextsize / self.orientation)}

        # so far, this only applies to bit oriented ciphers as we only have multiple modelling approaches for S-boxes
        self.type_of_modeling = type_of_modeling
        if "SunEtAl 2013" in self.type_of_modeling:
            if "Greedy" in self.type_of_modeling:
                self.choice_of_inequalities = 'greedy'
                self.extract_sun_inequalities = True
            else:
                self.choice_of_inequalities = 'all'
                self.extract_sun_inequalities = True
            if "Baksi extension 2020" in self.type_of_modeling:
                self.baksi_extension = True
            else:
               self.baksi_extension = False
        else:
            self.choice_of_inequalities = None
            self.extract_sun_inequalities = False
            self.baksi_extension = False

        return

    def gen_long_constraint(self, action):
        action.run_action()
        return

    def calculate_vars_and_constraints(self, xors_per_round, twf_per_round, lt_per_round, xors_not_in_rounds=0,
                                       overwrites=0, new_keys_every_round=False):
        # with mouha, every round, there are
        #   1 dummy + 1 output per XOR, 1 dummy per self.linear transformation, dummy + 2 output per 3-way fork,
        #   and 1 dummy + v output per w*v sbox
        #   4 inequalities per XOR
        #   2*l + 1 inequalities per self.linear transformation L: F_2^l -> F_2^l
        #   4 per 3-fork branch
        # Das Nicky Paper war byte-oriented (e.g. 32 byte input in Enocoro) während das
        # Sun Paper bit-oriented ist (e.g. 64 bit input in LBlock)
        # with sun, every round there are:
        #   1 + w constraints are necessary for all (w*v)-sboxes
        #   2 more are needed if the sbox is symmetric
        #   w + v + 1 more, redundant if the sbox invertible with branch number 2

        #   determine plaintext vars
        plaintext_vars = self.plaintext_vars
        key_vars = self.key_vars * (self.rounds + 1)  # upper bound in accordance with AES

        xor_dummy_variables_per_round = xors_per_round
        xor_constraints_per_round = 4 * xors_per_round
        xor_new_x_vars_per_round = xors_per_round

        twf_dummy_variables_per_round = twf_per_round
        twf_constraints_per_round = 4 * twf_per_round
        twf_new_x_vars_per_round = 2 * twf_per_round

        #   determine self.linear transformation output vars, dummy vars, and constraints
        lt_dummy_variables_per_round = len(lt_per_round)
        lt_constraints_per_round = 2 * sum(lt_per_round) + len(lt_per_round)
        lt_new_x_vars_per_round = sum(lt_per_round)

        #   determine output vars from overwriting operations such as ColumnMix in AES
        overwrite_new_x_vars_per_round = overwrites

        extra_xor_dummy_variables_per_round = xors_not_in_rounds
        extra_xor_constraints = 4 * xors_not_in_rounds
        extra_xor_new_x_vars = xors_not_in_rounds

        #   determine sbox output vars, dummy vars, and constraints
        if self.orientation == 1:
            sboxes_per_round = len(self.sboxes)

            bijective_sboxes_per_round = sum([int(sbox.is_bijective) for sbox in self.sboxes])
            # the entry for a sbox is 1 iff the sbox is not invertible or its branch number is larger than 2
            extra_constraint_sboxes_per_round = sum(
                [1 ^ int(sbox.is_invertible and sbox.branch_number <= 2) for sbox in self.sboxes])
        else:
            sboxes_per_round = 0
            bijective_sboxes_per_round = 0
            extra_constraint_sboxes_per_round = 0

        sbox_new_x_variables_per_round = sum(sbox.out_bits for sbox in self.sboxes) * bool(sboxes_per_round)
        sbox_dummy_variables_per_round = sboxes_per_round
        sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large = extra_constraint_sboxes_per_round
        sbox_constraints_per_round_following_sun = sboxes_per_round + sum(sbox.in_bits for sbox in self.sboxes) + (
                bijective_sboxes_per_round * 2) + extra_constraint_sboxes_per_round * (
                                                           1 + sum(sbox.out_bits for sbox in self.sboxes) + sum(
                                                       sbox.in_bits for sbox in self.sboxes))

        if self.type_of_modeling == 'Baksi 2020':
            qijp_variables_per_round = sum([len(sbox.set_of_transition_values) for sbox in self.sboxes])
            qijlp_variables_per_round = sum([sum([frequency for _, frequency in sbox.value_frequencies.items()]) for sbox in self.sboxes])
            baksi_variables_per_round = qijp_variables_per_round + qijlp_variables_per_round
        else:
            qijp_variables_per_round = 0
            qijlp_variables_per_round = 0
            baksi_variables_per_round = 0

        # self.M is lil_matrix((#constraints, #variables), dtype=int) with lil_matrix coming from the SciPy package

        number_constraints = ((xor_constraints_per_round +
                               twf_constraints_per_round +
                               sbox_constraints_per_round_following_sun +
                               lt_constraints_per_round) * self.rounds) + extra_xor_constraints + 1
        number_constraints = int(number_constraints)
        print("# Constraints:", number_constraints)

        self.number_variables = (plaintext_vars +
                                 key_vars +
                                 (
                                         xor_new_x_vars_per_round + xor_dummy_variables_per_round +
                                         twf_new_x_vars_per_round + twf_dummy_variables_per_round +
                                         lt_new_x_vars_per_round + lt_dummy_variables_per_round +
                                         sbox_new_x_variables_per_round + sbox_dummy_variables_per_round +
                                         sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large +
                                         overwrite_new_x_vars_per_round + baksi_variables_per_round
                                 ) * self.rounds) + extra_xor_new_x_vars + extra_xor_dummy_variables_per_round + 1
        self.number_variables = int(self.number_variables)
        print("# Variables:", self.number_variables)

        self.M = lil_matrix((number_constraints, self.number_variables), dtype=int)

        # we order M by: x variables (cipher bits), d dummy variables (xor), a dummy variables (bit oriented sboxes),
        # this ordering is self.V = dict of all variables mapping names to entry in self.M
        self.number_x_vars = int(plaintext_vars + extra_xor_new_x_vars + ((
                                                                                  xor_new_x_vars_per_round + twf_new_x_vars_per_round + lt_new_x_vars_per_round + sbox_new_x_variables_per_round + overwrite_new_x_vars_per_round) * self.rounds))
        self.number_dx_vars = xor_dummy_variables_per_round * self.rounds + extra_xor_dummy_variables_per_round
        self.number_dt_vars = twf_dummy_variables_per_round * self.rounds
        self.number_dl_vars = lt_dummy_variables_per_round * self.rounds

        self.number_a_vars = int(sbox_dummy_variables_per_round * self.rounds)
        self.number_ds_vars = int(sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large * self.rounds)

        self.prepare_for_type_of_modeling()

        if self.type_of_modeling == 'Baksi 2020':
            self.number_qijp_vars = qijp_variables_per_round * self.rounds
            self.number_qijlp_vars = qijlp_variables_per_round * self.rounds
        else:
            pass

        self.V = {'x' + str(i): i for i in range(self.number_x_vars)}
        self.V |= {i: 'x' + str(i) for i in range(self.number_x_vars)}

        self.V |= {'dx' + str(i): i + self.number_x_vars for i in range(self.number_dx_vars)}
        self.V |= {i + self.number_x_vars: 'dx' + str(i) for i in range(self.number_dx_vars)}

        self.V |= {'dt' + str(i): i + self.number_x_vars + self.number_dx_vars for i in range(self.number_dt_vars)}
        self.V |= {i + self.number_x_vars: 'dt' + str(i) for i in range(self.number_dt_vars)}

        self.V |= {'dl' + str(i): i + self.number_x_vars + self.number_dx_vars + self.number_dt_vars for i in
                   range(self.number_dl_vars)}
        self.V |= {i + self.number_x_vars: 'dl' + str(i) for i in range(self.number_dl_vars)}

        self.number_d_vars = self.number_dx_vars + self.number_dt_vars + self.number_dl_vars

        self.V |= {'a' + str(i): i + self.number_x_vars + self.number_d_vars for i in range(self.number_a_vars)}
        self.V |= {i + self.number_x_vars + self.number_d_vars: 'a' + str(i) for i in range(self.number_a_vars)}

        list_of_ds_vars = ['ds' + str(i) for i in
                           range(sbox_dummy_variables_per_round_if_not_invertible_or_branch_number_large * self.rounds)]
        self.V |= {var_name: index + self.number_x_vars + self.number_d_vars + self.number_a_vars
                   for index, var_name in enumerate(list_of_ds_vars)}
        self.V |= {index + self.number_x_vars + self.number_d_vars + self.number_a_vars: var_name
                   for index, var_name in enumerate(list_of_ds_vars)}

        self.V |= {'k' + str(i): i + self.number_x_vars + self.number_d_vars + self.number_a_vars + self.number_ds_vars
                   for i in range(self.keysize * ((new_keys_every_round * self.rounds) + 1))}
        self.V |= {i + self.number_x_vars + self.number_d_vars + self.number_a_vars + self.number_ds_vars: 'k' + str(i)
                   for i in range(self.keysize * ((new_keys_every_round * self.rounds) + 1))}

        qijp_vars = list(chain.from_iterable([chain.from_iterable(
            [[(index + (round_number * len(self.sboxes)), p, round_number, sbox) for p in sbox.set_of_transition_values]
             for index, sbox in enumerate(self.sboxes)]) for round_number in range(self.rounds)]))
        qijlp_vars = list(chain.from_iterable([
            [(qijp_var[0], qijp_var[1], qijp_var[2], l) for l in range(qijp_var[3].value_frequencies[qijp_var[1]])] for
            qijp_var in qijp_vars]))

        self.V |= {
            f'a{qijp_var[0]}p{qijp_var[1]}': i + self.number_x_vars + self.number_d_vars + self.number_a_vars + self.number_ds_vars + self.keysize * (
                        (new_keys_every_round * self.rounds) + 1) for i, qijp_var in enumerate(qijp_vars)}
        self.V |= {
            i + self.number_x_vars + self.number_d_vars + self.number_a_vars + self.number_ds_vars + self.keysize * (
                        (new_keys_every_round * self.rounds) + 1): f'a{qijp_var[0]}p{qijp_var[1]}' for i, qijp_var in
            enumerate(qijp_vars)}

        self.V |= {
            f'a{qijlp_var[0]}p{qijlp_var[1]}l{qijlp_var[3]}': i + self.number_x_vars + self.number_d_vars + self.number_a_vars + self.number_ds_vars + self.keysize * (
                        (new_keys_every_round * self.rounds) + 1) + len(qijp_vars) for i, qijlp_var in
            enumerate(qijlp_vars)}
        self.V |= {
            i + self.number_x_vars + self.number_d_vars + self.number_a_vars + self.number_ds_vars + self.keysize * (
                        (new_keys_every_round * self.rounds) + 1) + len(
                qijp_vars): f'a{qijlp_var[0]}p{qijlp_var[1]}l{qijlp_var[3]}' for i, qijlp_var in enumerate(qijlp_vars)}

        self.V['constant'] = self.M.get_shape()[1] - 1
        self.V[self.M.get_shape()[1] - 1] = 'constant'

        return sbox_dummy_variables_per_round

    def prepare_for_type_of_modeling(self):
        if self.cryptanalysis_type == 'differential':
            for sbox in self.sboxes:
                sbox.build_ddt()
                sbox.build_list_of_transition_values_and_frequencies(sbox.ddt)
        elif self.cryptanalysis_type == 'linear':
            for sbox in self.sboxes:
                sbox.build_lat()
                sbox.build_list_of_transition_values_and_frequencies(sbox.lat)
        else:
            pass
        return
