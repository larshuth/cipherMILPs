import math


class SBox:
    def determine_invertibility(self):
        set_of_values = set()
        for key, value in self.substitutions.items():
            if value in set_of_values:
                return False
            else:
                set_of_values |= {value}
        return True

    def determine_bijectivity(self):
        if (self.in_bits == self.out_bits) and self.is_invertible:
            return True
        return False

    def determine_branch_number(self):
        # the branch number is defined as the
        minimal_hamming_weight = self.in_bits + self.out_bits
        for input_1 in range(2 ** self.in_bits - 1):
            for input_2 in range(2 ** self.out_bits - 1):
                input_diff = input_1 ^ input_2
                output_1 = self.substitutions[input_1]
                output_2 = self.substitutions[input_2]
                output_diff = output_1 ^ output_2
                if (input_diff * output_diff) > 0:
                    hamming_weight_input_diff = sum(
                        [1 if ((2 ** i & input_diff) > 0) else 0 for i in range(self.in_bits)])
                    hamming_weight_output_diff = sum(
                        [1 if ((2 ** i & output_diff) > 0) else 0 for i in range(self.out_bits)])
                    current_hamming_weight = hamming_weight_input_diff + hamming_weight_output_diff
                    minimal_hamming_weight = min(minimal_hamming_weight, current_hamming_weight)
        return minimal_hamming_weight

    def check_subs_match_bits(self):
        key_set = set(key for key, value in self.substitutions.items())
        value_set = set(value for key, value in self.substitutions.items())

        expected_in_words = 2 ** self.in_bits
        expected_out_words = 2 ** self.out_bits
        actual_number_in_words = len(self.substitutions)
        actual_number_out_words = len(value_set)

        expected_max_key = 2 ** self.in_bits - 1
        expected_max_value = 2 ** self.out_bits - 1

        actual_max_key = max(key_set)
        actual_max_value = max(value_set)

        if actual_number_in_words != expected_in_words:
            raise Exception('Number of substitutions defined not feasible with declared number of in_bits')
        elif actual_number_out_words != expected_out_words:
            raise Exception('Number of substitutions defined not feasible with declared number of in_bits')
        elif actual_max_value > expected_max_value:
            raise Exception(
                'At least one value in substitution cannot feasibly be represented with declared number of out_bits')
        elif actual_max_key > expected_max_key:
            raise Exception(
                'At least one key in substitution cannot feasibly be represented with declared number of in_bits')
        else:
            return

    def __init__(self, substitutions, in_bits, out_bits):
        self.substitutions, self.in_bits, self.out_bits = substitutions, in_bits, out_bits

        self.check_subs_match_bits()

        self.is_invertible = self.determine_invertibility()
        self.is_bijective = self.determine_bijectivity()
        self.branch_number = self.determine_branch_number()

        self.ddt_built = False
        self.ddt = list()

        self.non_zero_ddt_entries_built = False
        self.non_zero_ddt_entries = set()

        self.differential_properties_built = False
        self.differential_properties = set()

        self.non_zero_ddt_entries_vectors_built = False
        self.vectors = set()

        self.dummy_vars_for_bit_oriented_modeling_all = 1
        self.dummy_vars_for_bit_oriented_modeling_sbox_dependent = 1 ^ int(
            self.is_invertible and self.branch_number <= 2)
        self.dummy_vars_for_bit_oriented_modeling = self.dummy_vars_for_bit_oriented_modeling_all + self.dummy_vars_for_bit_oriented_modeling_sbox_dependent

        self.transitions_built = False
        self.probability_transitions = dict()
        return

    def build_ddt(self):
        if self.ddt_built:
            return

        self.ddt = [[0].copy() * (2 ** self.out_bits) for i in range(2 ** self.in_bits)]

        self.non_zero_ddt_entries = set()
        for in_val_1, out_val_1 in self.substitutions.items():
            for in_val_2, out_val_2 in self.substitutions.items():
                in_val_xorwise_diff = in_val_1 ^ in_val_2
                out_val_xorwise_diff = out_val_1 ^ out_val_2
                try:
                    self.ddt[in_val_xorwise_diff][out_val_xorwise_diff] += 1
                except:
                    print(in_val_xorwise_diff, out_val_xorwise_diff, self.in_bits, self.out_bits)

                self.non_zero_ddt_entries |= {(in_val_xorwise_diff, out_val_xorwise_diff)}
        self.non_zero_ddt_entries_built = True
        self.ddt_built = True
        return

    def build_non_zero_ddt_entries_vectors(self):
        if self.non_zero_ddt_entries_vectors_built:
            return

        if not self.non_zero_ddt_entries_built:
            self.build_ddt()

        self.vectors = set()
        for x, y in (self.non_zero_ddt_entries ^ {(0, 0)}):
            vector = list()
            for i in range(0, self.in_bits):
                if 2 ** i >= x:
                    vector.append(1)
                    x -= 2 ** i
                else:
                    vector.append(0)

            for i in range(0, self.out_bits):
                if 2 ** i >= y:
                    vector.append(1)
                    y -= 2 ** i
                else:
                    vector.append(0)
            self.vectors |= {tuple(vector.copy())}
        return

    def build_differential_patterns_input_to_output(self):
        differential_properties_i2o = set()
        max_value_for_output = 2 ** self.out_bits - 1

        # collecting/recording differential properties from input to output like the example
        # (i) 1001→***0: If the input difference of the S-box is 0x9 = 1001, then the least significant bit of the
        # output difference must be 0
        # from the Sun et al. 2013 paper
        for input_xorwise_diff, distribution in enumerate(self.ddt):
            # set reoccurrences to the equivalent of 1^n (e.g. 1111 for a 4x5 SBox)
            reoccurring_1s = max_value_for_output
            reoccurring_0s = max_value_for_output
            for output_xorwise_diff, occurrences in enumerate(distribution):
                if occurrences > 0:
                    reoccurring_1s &= output_xorwise_diff
                    reoccurring_0s &= (max_value_for_output - output_xorwise_diff)
            if reoccurring_0s or reoccurring_1s:
                differential_properties_i2o |= {('i2o', input_xorwise_diff, reoccurring_0s, reoccurring_1s)}
        return differential_properties_i2o

    def build_differential_patterns_output_to_input(self):
        differential_properties_o2i = set()
        max_value_for_input = 2 ** self.in_bits - 1

        # collecting/recording differential properties from output to input like the example
        # (iii) ***1→0001 and ***1→0100: If the output difference of the S-box is 0x1 = 0001 or 0x4 = 0100, then
        # the least significant bit of the input difference must be 1
        # from the Sun et al. 2013 paper
        for output_xorwise_diff in range(max_value_for_input):
            # set reoccurrences to the equivalent of 1^n (e.g. 1111 for a 4x5 SBox)
            reoccurring_1s = max_value_for_input
            reoccurring_0s = max_value_for_input
            for input_xorwise_diff, distribution in enumerate(self.ddt):
                occurrences = distribution[output_xorwise_diff]
                if occurrences > 0:
                    reoccurring_1s &= input_xorwise_diff
                    reoccurring_0s &= (max_value_for_input - input_xorwise_diff)
            if reoccurring_0s or reoccurring_1s:
                self.differential_properties |= {('o2i', output_xorwise_diff, reoccurring_0s, reoccurring_1s)}

        return differential_properties_o2i

    def build_differential_patterns(self):
        # make sure ddt has been built and can be called upon
        if self.differential_properties_built:
            return

        if not self.ddt_built:
            self.build_ddt()

        differential_properties_i2o = self.build_differential_patterns_input_to_output()
        self.differential_properties |= differential_properties_i2o

        differential_properties_o2i = self.build_differential_patterns_input_to_output()
        self.differential_properties |= differential_properties_o2i

        return

    def build_lat(self):
        return

    def build_transitions(self):
        if self.transitions_built:
            return
        for i in range(max(self.in_bits, self.out_bits)):
            self.probability_transitions[1] = 0
        set_not_to_remove = set()
        for in_diff, out_diff in self.non_zero_ddt_entries:
            probability = self.ddt[in_diff][out_diff]
            self.probability_transitions[probability] += 1
            set_not_to_remove |= {probability}
        for key in self.probability_transitions:
            if key not in set_not_to_remove:
                self.probability_transitions.pop(key)
        self.probability_transitions.pop(16)
        self.transitions_built = True
        return
