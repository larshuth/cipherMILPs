import math

import numpy as np
from itertools import chain
import convexHull
import re
import pickle


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

    def __init__(self, substitutions, in_bits, out_bits, cipher_instance=None, extract_sun_inequalities=False):
        self.cipher_instance = cipher_instance

        self.substitutions, self.in_bits, self.out_bits = substitutions, in_bits, out_bits

        self.check_subs_match_bits()

        self.is_invertible = self.determine_invertibility()
        self.is_bijective = self.determine_bijectivity()
        self.branch_number = self.determine_branch_number()

        self.ddt_built = False
        self.ddt = list()

        self.lat_built = False
        self.lat = list()

        self.non_zero_ddt_entries_built = False
        self.non_zero_ddt_entries = set()

        self.dict_of_transitions_i2o = dict()
        self.dict_of_transitions_o2i = dict()

        self.differential_properties_built = False
        self.differential_properties = set()

        self.non_zero_ddt_entries_vectors_built = False
        self.non_zero_linear_mask_vectors_built = False
        self.vectors = set()
        self.impossible_transitions = set()

        self.dummy_vars_for_bit_oriented_modeling_all = 1
        self.dummy_vars_for_bit_oriented_modeling_sbox_dependent = 1 ^ int(
            self.is_invertible and self.branch_number <= 2)
        self.dummy_vars_for_bit_oriented_modeling = self.dummy_vars_for_bit_oriented_modeling_all + self.dummy_vars_for_bit_oriented_modeling_sbox_dependent

        self.transitions_built = False
        self.probability_transitions = dict()

        if extract_sun_inequalities:
            self.feasible_transition_inequalities_sun_2013 = self.retrieve_inequalities()
            self.feasible_transition_inequalities_sun_2013_extracted = self.find_impossible_transitions_for_each_sun_2013_inequality(
                extract_sun_inequalities=extract_sun_inequalities)
        else:
            self.feasible_transition_inequalities_sun_2013 = list()
            self.feasible_transition_inequalities_sun_2013_extracted = list()

        self.transition_values_and_frequencies_built = False
        self.set_of_transition_values = set()
        self.value_frequencies = dict()
        self.dict_value_to_list_of_transition = dict()
        return

    def retrieve_inequalities(self):
        if self.cipher_instance.cryptanalysis_type:
            filename = ''.join([hex(value)[2:] for key, value in self.substitutions.items()]) + self.cipher_instance.cryptanalysis_type
            try:
                file = open(f'{filename}.pkl', 'rb')
                inequalities = pickle.load(file)
                file.close()
            except:
                inequalities = convexHull.ch_hrep_from_sbox(self)
                file = open(f'{filename}.pkl', 'wb')
                pickle.dump(inequalities, file)
                file.close()
        else:
            inequalities = convexHull.ch_hrep_from_sbox(self)

        return inequalities

    def build_ddt(self):
        if self.ddt_built:
            return

        self.ddt = [[0].copy() * (2 ** self.out_bits) for i in range(2 ** self.in_bits)]
        self.non_zero_ddt_entries = set()
        self.dict_of_transitions_i2o = {i: set() for i in range(2 ** self.in_bits)}
        self.dict_of_transitions_o2i = {i: set() for i in range(2 ** self.in_bits)}

        for in_val_1, out_val_1 in self.substitutions.items():
            for in_val_2, out_val_2 in self.substitutions.items():
                in_val_xorwise_diff = in_val_1 ^ in_val_2
                out_val_xorwise_diff = out_val_1 ^ out_val_2
                try:
                    self.ddt[in_val_xorwise_diff][out_val_xorwise_diff] += 1
                except:
                    print(in_val_xorwise_diff, out_val_xorwise_diff, self.in_bits, self.out_bits)
                    raise Exception('This one prior did not work')
                self.dict_of_transitions_i2o[in_val_xorwise_diff].add(out_val_xorwise_diff)
                self.dict_of_transitions_o2i[out_val_xorwise_diff].add(in_val_xorwise_diff)
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
        for x, y in self.non_zero_ddt_entries:
            vector_in = [1 if (((2 ** i) & x) > 0) else 0 for i in range(self.in_bits - 1, -1, -1)]
            vector_out = [1 if (((2 ** i) & y) > 0) else 0 for i in range(self.out_bits - 1, -1, -1)]

            self.vectors |= {tuple(vector_in.copy() + vector_out.copy())}
        print(self.vectors)
        all_transitions = set(tuple([1 if (((2 ** i) & counter) > 0) else 0 for i in
                                     range((self.in_bits + self.out_bits) - 1, -1, -1)]) for counter in
                              range(2 ** (self.in_bits + self.out_bits)))
        self.impossible_transitions = all_transitions - self.vectors
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
            if (reoccurring_0s or reoccurring_1s) and (input_xorwise_diff != 0):
                differential_properties_i2o |= {('i2o', input_xorwise_diff, reoccurring_0s, reoccurring_1s)}
        return differential_properties_i2o

    def build_differential_patterns_output_to_input(self):
        differential_properties_o2i = set()
        max_value_for_output = 2 ** self.out_bits - 1

        # collecting/recording differential properties from output to input like the example
        # (iii) ***1→0001 and ***1→0100: If the output difference of the S-box is 0x1 = 0001 or 0x4 = 0100, then
        # the least significant bit of the input difference must be 1
        # from the Sun et al. 2013 paper
        for output_xorwise_diff in range(max_value_for_output + 1):
            # set reoccurrences to the equivalent of 1^n (e.g. 1111 for a 4x5 SBox)
            reoccurring_1s = max_value_for_output
            reoccurring_0s = max_value_for_output
            for input_xorwise_diff, distribution in enumerate(self.ddt):
                occurrences = distribution[output_xorwise_diff]
                if occurrences > 0:
                    reoccurring_1s &= input_xorwise_diff
                    reoccurring_0s &= (max_value_for_output - input_xorwise_diff)
            if (reoccurring_0s or reoccurring_1s) and (output_xorwise_diff != 0):
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

        differential_properties_o2i = self.build_differential_patterns_output_to_input()
        self.differential_properties |= differential_properties_o2i

        return

    def build_lat(self):
        if self.lat_built:
            return

        self.lat = [[0].copy() * (2 ** self.out_bits) for i in range(2 ** self.in_bits)]

        hamming_weight = lambda x: sum(
            [1 if ((2 ** i & x) > 0) else 0 for i in range(max(self.in_bits, self.out_bits))])

        for input_mask in range(2 ** self.in_bits):
            for output_mask in range(2 ** self.out_bits):
                sum_for_mask_combination = 0
                for in_val, out_val in self.substitutions.items():
                    input_sum = hamming_weight(input_mask & in_val) % 2
                    output_sum = hamming_weight(output_mask & out_val) % 2
                    sum_for_mask_combination += int(input_sum == output_sum)
                try:
                    self.lat[input_mask][output_mask] = - int(((2 ** self.in_bits) / 2) - sum_for_mask_combination)
                except:
                    print(input_mask, output_mask, self.in_bits, self.out_bits)
                    raise Exception('This one prior did not work')
        self.lat_built = True
        return

    def build_non_zero_linear_mask_transition_vectors(self):
        if self.non_zero_linear_mask_vectors_built:
            return

        int_of_vector = lambda x: sum([(2 ** (len(x) - index - 1)) * bit for index, bit in enumerate(x)])
        vector_of_int = lambda value, length: [1 if ((2 ** i & value) > 0) else 0 for i in range(length - 1, -1, -1)]

        self.vectors = set()
        for x, y in self.substitutions.items():
            vector_in = vector_of_int(x, self.in_bits)
            vector_out = vector_of_int(y, self.out_bits)

            self.vectors |= {tuple(vector_in.copy() + vector_out.copy())}

        all_transitions = set(tuple(vector_of_int(i, self.in_bits + self.out_bits)) for i in
                              range(2 ** (self.in_bits + self.out_bits)))

        self.impossible_transitions = all_transitions - self.vectors
        return

    def build_non_zero_transition_vectors(self):
        if self.cipher_instance.cryptanalysis_type == "linear":
            self.build_non_zero_ddt_entries_vectors()
        elif self.cipher_instance.cryptanalysis_type == "differential":
            self.build_non_zero_linear_mask_transition_vectors()
        else:
            raise Exception(
                f'Type of cryptanalysis  of {self.cipher_instance} has not been set to one of the proper types "linear" of "differential"')
        return

    def calculate_multipliers(self, greater, lesser, split_into_variables, find_variable_multiplier, find_variable_name,
                              extract_sun_inequalities=False, invert_greater=False):
        multipliers = [0 for _ in range(self.in_bits + self.out_bits)]
        if invert_greater:
            inverter = -1
        else:
            inverter = 1

        # first we split our inequality into a list of its variables. E.g. using the findall() method on
        # 'x1 - x3 + x4 - x5  ' yields ['x1 ', '- x3 ', '+ x4 ', '- x5 ']
        greater = greater.replace('*', '')
        list_of_all_variables = split_into_variables.findall(greater)

        # then we take each of the variables and
        for variable_string in list_of_all_variables:
            # first remove the spaces
            variable_string = variable_string.replace(' ', '')
            # determine whether we are dealing with a '+ a x123' or '- a x123'
            if variable_string[0] == '-':
                modifier = -1
            elif variable_string[0] == '+':
                modifier = +1
            else:
                variable_string = '+' + variable_string
                modifier = +1
            # we shortly remove the variable name (except for x) after removing all of th
            multiplication_factor_search = find_variable_multiplier.findall(variable_string[1:])

            if multiplication_factor_search[0] != 'x':
                multiplication_factor = int(multiplication_factor_search[0][:-1])
            else:
                multiplication_factor = 1
            variable_name = int(find_variable_name.findall(variable_string)[0][1:])
            multipliers[variable_name] = (inverter * modifier * multiplication_factor)

        constant = inverter * int(lesser)

        # At this point, I would like to say that I do not condone people being excluded from transitioning.
        # Trans rights are human rights!
        impossible_transitions_as_int = set()

        if extract_sun_inequalities:
            multipliers_vector = np.array(multipliers)
            for i in range(2 ** (self.in_bits + self.out_bits)):
                x = np.unpackbits(np.array([i], dtype=np.uint8), count=(self.in_bits + self.out_bits),
                                  bitorder='little')
                inequality_result = np.dot(multipliers_vector, x)
                if inequality_result < constant:
                    impossible_transitions_as_int.add(i)
        return multipliers, constant, impossible_transitions_as_int

    def find_impossible_transitions_for_each_sun_2013_inequality(self, extract_sun_inequalities=False) -> list[
        list[list[int], int, set[int]]]:
        # we prepare all the inequalities but in another format in inequalities_readable
        inequalities_readable = list()

        # we define the following before going into the loop as to not be redundant in the compiling for them
        # first we split our inequality into a list of its variables. E.g. using the findall() method on
        # 'x1 - x3 + x4 - x5  ' will return ['x1 ', '- x3 ', '+ x4 ', '- x5 ']
        split_into_variables = re.compile('[+-]* *[0-9]*x[0-9]+ ')

        # on '+34x4'[1:] find_variable_multiplier will return '34x'
        find_variable_multiplier = re.compile('^[0-9]*x')
        # on '+34x4' find_variable_name will return 'x4'
        find_variable_name = re.compile('x[0-9]+$')

        # split inequalities in a list with one inequality per entry
        for index, inequality in enumerate(self.feasible_transition_inequalities_sun_2013):
            try:
                [greater, lesser] = inequality.split(">=")
                # get left part, right part, something along the self.lines of
                # ["         -x4 + x5 ", "  0"]
                multipliers, constant, impossible_transitions_as_int = self.calculate_multipliers(greater, lesser,
                                                                                                  split_into_variables,
                                                                                                  find_variable_multiplier,
                                                                                                  find_variable_name,
                                                                                                  extract_sun_inequalities)
                inequalities_readable.append([multipliers, - constant, impossible_transitions_as_int])
            except ValueError:
                try:
                    [greater, lesser] = inequality.split("==")
                    # get left part, right part, something along the self.lines of
                    # ["         -x4 + x5 ", "  0"]
                    # for a == b we'd have both a >= b and b >= a
                    multipliers, constant, impossible_transitions_as_int = self.calculate_multipliers(greater, lesser,
                                                                                                      split_into_variables,
                                                                                                      find_variable_multiplier,
                                                                                                      find_variable_name,
                                                                                                      extract_sun_inequalities)
                    inequalities_readable.append([multipliers, - constant, impossible_transitions_as_int])

                    multipliers, constant, impossible_transitions_as_int = self.calculate_multipliers(greater, lesser,
                                                                                                      split_into_variables,
                                                                                                      find_variable_multiplier,
                                                                                                      find_variable_name,
                                                                                                      extract_sun_inequalities,
                                                                                                      invert_greater=True)

                    inequalities_readable.append([multipliers, - constant, impossible_transitions_as_int])

                except ValueError as a:
                    print('Non-matching inequality:', inequality)
                    raise AttributeError(a)

        return inequalities_readable

    def build_list_of_transition_values_and_frequencies(self):
        if self.transition_values_and_frequencies_built:
            return

        if self.cipher_instance.cryptanalysis_type == "linear":
            self.build_lat()
            reference_table = self.lat
            reference_value_for_no_occurence = -8
        elif self.cipher_instance.cryptanalysis_type == "differential":
            self.build_ddt()
            reference_table = self.ddt
            reference_value_for_no_occurence = 0
        else:
            raise Exception(
                f'Type of cryptanalysis  of {self.cipher_instance} has not been set to one of the proper types "linear" of "differential"')

        list_of_transition_values = list(chain.from_iterable(reference_table))
        self.set_of_transition_values = set(list_of_transition_values) - {reference_value_for_no_occurence}
        self.value_frequencies = {value: list_of_transition_values.count(value) for value in
                                  self.set_of_transition_values}
        self.dict_value_to_list_of_transition = {val: list() for val in self.set_of_transition_values}
        set_of_included = set()
        for input_diff, sub_reference_table in enumerate(reference_table):
            for output_diff, value in enumerate(sub_reference_table):
                if (value != reference_value_for_no_occurence) and ((input_diff, output_diff) not in set_of_included):
                    self.dict_value_to_list_of_transition[value].append((input_diff, output_diff))
                    set_of_included.add((input_diff, output_diff))
        self.transition_values_and_frequencies_built = True
        return
