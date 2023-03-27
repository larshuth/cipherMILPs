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
                    hamming_weight_input_diff = sum([1 if ((2**i & input_diff) > 0) else 0 for i in range(self.in_bits)])
                    hamming_weight_output_diff = sum([1 if ((2**i & output_diff) > 0) else 0 for i in range(self.out_bits)])
                    current_hamming_weight = hamming_weight_input_diff + hamming_weight_output_diff
                    minimal_hamming_weight = min(minimal_hamming_weight, current_hamming_weight)
        return minimal_hamming_weight

    def __init__(self, substitutions, in_bits, out_bits):
        self.substitutions, self.in_bits, self.out_bits = substitutions, in_bits, out_bits

        self.is_invertible = self.determine_invertibility()
        self.is_bijective = self.determine_bijectivity()
        self.branch_number = self.determine_branch_number()

        self.ddt_built = False
        self.ddt = list()

        self.non_zero_ddt_entries_built = False
        self.non_zero_ddt_entries = set()

        self.differential_properties_built = False
        self.differential_properties = set()

        self.vectors = set()
        return

    def build_ddt(self):
        if self.ddt_built:
            return

        self.ddt = [[0] * self.out_bits] * self.in_bits
        self.non_zero_ddt_entries = set()
        for in_val_1, out_val_1 in self.substitutions.items():
            for in_val_2, out_val_2 in self.substitutions.items():
                in_val_xorwise_diff = in_val_1 ^ in_val_2
                out_val_xorwise_diff = out_val_1 ^ out_val_2
                self.ddt[in_val_xorwise_diff][out_val_xorwise_diff] += 1
                self.non_zero_ddt_entries |= {(in_val_xorwise_diff, out_val_xorwise_diff)}
        self.non_zero_ddt_entries_built = True
        self.ddt_built = True
        return

    def build_non_zero_ddt_entries_vectors(self):
        if self.non_zero_ddt_entries_built:
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
