import convexHull
from scipy.sparse import lil_matrix


class CipherAction:
    def __init__(self, type_of_action, cipher_instance):
        self.type_of_action = type_of_action
        self.cipher_instance = cipher_instance
        return

    def set_all_to_value(self, list_of_variables, value, line_var=None, matrix_to_be_set=None):
        if matrix_to_be_set is None:
            matrix_to_be_set = self.cipher_instance.M
        if line_var is None:
            line_var = self.cipher_instance.line

        for var in list_of_variables:
            var_pos_in_matrix = self.cipher_instance.V[var]
            matrix_to_be_set[line_var, var_pos_in_matrix] = value
        return

    def for_each_var_set_to_value_plus_dummy(self, list_of_variables, var_value, dummy_pos, dum_value):
        for var in list_of_variables:
            var_pos_in_matrix = self.cipher_instance.V[var]
            self.cipher_instance.M[self.cipher_instance.line, var_pos_in_matrix] = var_value
            self.cipher_instance.M[self.cipher_instance.line, dummy_pos] = dum_value
            self.cipher_instance.line += 1
        return


class SBoxAction(CipherAction):

    def __init__(self, sbox, input_start, output_start, dummy, cipher_instance):
        super().__init__("sbox", cipher_instance)
        self.sbox = sbox

        self.input_vars = ['x' + str(input_start + i) for i in range(self.sbox.in_bits)]
        self.output_vars = ['x' + str(output_start + i) for i in range(self.sbox.out_bits)]
        self.dummy_var = dummy
        self.dummy_var_pos_in_matrix = self.cipher_instance.V[self.dummy_var]

        # TODO rename vars
        self.qijp_vars = list()
        self.qijlp_vars = list()
        return

    def input_leq_dummy(self):
        self.for_each_var_set_to_value_plus_dummy(self.input_vars, 1, self.dummy_var_pos_in_matrix, -1)
        return

    def sum_over_all_inputs_geq_dummy(self):
        self.set_all_to_value(self.input_vars, -1)
        self.cipher_instance.M[self.cipher_instance.line, self.dummy_var_pos_in_matrix] = 1
        self.cipher_instance.line += 1
        return

    def non_zero_input_implies_non_zero_output(self):
        self.set_all_to_value(self.input_vars, -1)
        self.set_all_to_value(self.output_vars, self.sbox.out_bits)
        self.cipher_instance.line += 1
        return

    def non_zero_output_implies_non_zero_input(self):
        self.set_all_to_value(self.input_vars, self.sbox.out_bits)
        self.set_all_to_value(self.output_vars, -1)
        self.cipher_instance.line += 1
        return

    def branch_number_inequality(self):
        extra_constraint_dummy_var = 'ds' + str(self.cipher_instance.round_number) + str(self.sbox.__name__())[5:]
        extra_constraint_dummy_var_pos_in_matrix = self.cipher_instance.V[extra_constraint_dummy_var]

        # (4.1) sum over inputs + sum over outputs \geq branch * new dummy
        # setting all input vars and output vars to 1
        self.set_all_to_value(self.input_vars, 1)
        self.set_all_to_value(self.output_vars, 1)
        # setting dummy to branch_number
        self.cipher_instance.M[
            self.cipher_instance.line, extra_constraint_dummy_var_pos_in_matrix] = - self.sbox.branch_number
        self.cipher_instance.line += 1

        # (4.2) input \leq new dummy for all inputs
        # for every input var, a new inequality is made with the var \leq dummy
        self.for_each_var_set_to_value_plus_dummy(self.input_vars, -1, extra_constraint_dummy_var_pos_in_matrix, 1)

        # (4.3) output \leq dummy for all outputs
        # for every output var, a new inequality is made with the var \leq dummy
        self.for_each_var_set_to_value_plus_dummy(self.output_vars, -1, extra_constraint_dummy_var_pos_in_matrix, 1)
        return

    def create_convex_hull_matrices(self):
        constant_pos = self.cipher_instance.V["constant"]

        inequalities = convexHull.ch_hrep_from_sbox(self.sbox)
        number_of_inequalities = len(inequalities)
        # we get a string along the self.lines of
        #          -x6 + x7  >=   0
        #               -x7  >=  -1
        #          -x4 + x5  >=   0
        #                x0  >=   0
        # x1 - x3 + x4 - x5  >=  -1
        # as a return value from convexHull.ch_hrep_from_sbox in inequalities

        # adding a new sparse scipy matrix convex_hull_inequality_matrix for the constraints as we cannot count
        # them prior to this even and self.M would otherwise overflow
        convex_hull_inequality_matrix = lil_matrix((number_of_inequalities, self.cipher_instance.number_variables),
                                                   dtype=int)
        convex_hull_inequality_matrix_line = 0

        # split inequalities in a list with one inequality per entry
        for inequality in inequalities:
            try:
                inequality = inequality.replace(' ', '')
                [greater, lesser] = inequality.split(
                    ">=")  # get left part, right part, something along the self.lines of
                # ["         -x4 + x5 ", "  0"]
            except AttributeError:
                continue

            modifier = 1
            # TODO input the actual values into the matrix and not just a 1 for non-zero
            variables_not_zero = set()
            for character in greater:
                if character == "-":
                    modifier = -1
                elif character == "+":
                    modifier = +1
                elif character == "x":
                    continue
                else:  # i.e. the character is number coming after x
                    variables_not_zero |= {int(character)}

            for index, i in enumerate(self.input_vars):
                if index in variables_not_zero:
                    input_var_pos_in_matrix = self.cipher_instance.V[i]
                    convex_hull_inequality_matrix[
                        convex_hull_inequality_matrix_line, input_var_pos_in_matrix] = 1

            for index, i in enumerate(self.output_vars):
                output_var_pos_in_matrix = self.cipher_instance.V[i]
                if index + self.sbox.in_bits in variables_not_zero:
                    convex_hull_inequality_matrix[
                        convex_hull_inequality_matrix_line, output_var_pos_in_matrix] = 1

            value_right_of_inequality = int(lesser)
            convex_hull_inequality_matrix[
                convex_hull_inequality_matrix_line, constant_pos] = value_right_of_inequality
            convex_hull_inequality_matrix_line += 1

        self.cipher_instance.sbox_inequality_matrices.append(convex_hull_inequality_matrix)
        return

    def create_baksi_inequalities(self):
        if not self.sbox.is_bijectiv():
            raise Exception(
                "The 2020 Baksi paper only defines its S-box constraints on bijective s-boxes. Yet this action's s-box is not bijective.")
        # The Baksi paper introduces a new kind of modeling to ensure that the input and output differences of S-boxes
        # are only able to take feasible values in section 4. This model uses the following inequalities:
        # Q_{i,j} represents that this Sbox is active
        # (1.) M*Q_{i,j} \geq sum over inputs + sum over outputs
        # next, variables for each transition probability p are created in Q_{i,j}^p representing that the taken
        # transition is of probability p/2^{input bits}
        # (2.) Q_{i,j} = sum over all Q_{i,j}^p
        # we split this up in 2 inequalities since our matrix strictly represents \geq
        # (2.1) Q_{i,j} \geq sum over all Q_{i,j}^p
        # (2.2) - Q_{i,j} \geq -(sum over all Q_{i,j}^p)

        constant_pos = self.cipher_instance.V["constant"]
        big_m = 2 * self.sbox.in_bits

        self.sbox.build_transitions()

        # TODO find number of inequalities
        MORE = 0
        number_of_inequalities = 3 + 2 * len(self.sbox.probability_transitions) + sum(
            [value for key, value in self.sbox.probability_transitions.items]) + MORE

        sbox_inequality_matrix = lil_matrix((number_of_inequalities, self.cipher_instance.number_variables),
                                            dtype=int)
        sbox_inequality_matrix_line = 0

        # (1.)
        self.set_all_to_value(list_of_variables=self.input_vars, value=-1, line_var=sbox_inequality_matrix_line,
                              matrix_to_be_set=sbox_inequality_matrix)
        self.set_all_to_value(list_of_variables=self.output_vars, value=-1, line_var=sbox_inequality_matrix_line,
                              matrix_to_be_set=sbox_inequality_matrix)
        sbox_inequality_matrix[sbox_inequality_matrix_line, self.dummy_var_pos_in_matrix] = big_m
        sbox_inequality_matrix_line += 1

        # build/find Q_{i,j}^p variables
        self.qijp_vars = list()
        # TODO include Q_{i,j}^p variables in the calculation of the number of variables in cipher classes __init__

        # (2.1)
        self.set_all_to_value(list_of_variables=self.qijp_vars, value=-1, line_var=sbox_inequality_matrix_line,
                              matrix_to_be_set=sbox_inequality_matrix)
        sbox_inequality_matrix[sbox_inequality_matrix_line, self.dummy_var_pos_in_matrix] = 1
        sbox_inequality_matrix_line += 1
        # (2.2)
        self.set_all_to_value(list_of_variables=self.qijp_vars, value=1, line_var=sbox_inequality_matrix_line,
                              matrix_to_be_set=sbox_inequality_matrix)
        sbox_inequality_matrix[sbox_inequality_matrix_line, self.dummy_var_pos_in_matrix] = -1
        sbox_inequality_matrix_line += 1

        # build/find Q_{i,j}^p variables
        self.qijlp_vars = list()
        # TODO include Q_{i,j,l}^p variables in the calculation of the number of variables in cipher classes __init__

        None
        return

    def run_action(self, type_of_modeling="SunEtAl 2013"):
        # inequalities of sbox are
        # (1.) input \leq dummy for all inputs
        # (2.) sum over all inputs \geq dummy
        # (3.) if sbox bijective: sum_{i \in all_inputs}
        # (4.) if the sbox invertible with branch number 2:
        # (4.1) sum over inputs + sum over outputs \geq branch * new dummy
        # (4.2) input \leq new dummy for all inputs
        # (4.3) output \leq dummy for all outputs

        # starting with (1.)
        self.input_leq_dummy()

        # then (2.)
        self.sum_over_all_inputs_geq_dummy()

        # then (3.)
        if self.sbox.is_bijective:
            self.non_zero_input_implies_non_zero_output()
            self.non_zero_output_implies_non_zero_input()
        else:
            self.non_zero_output_implies_non_zero_input()

        # and finally (4.) sbox invertible with branch number 2
        if (not self.sbox.is_invertible) or (not (self.sbox.branch_number <= 2)):
            # TODO expand to be applicable to ciphers with more than 10 sboxes
            self.branch_number_inequality()

        if type_of_modeling == "SunEtAl 2013":
            self.create_convex_hull_matrices()
        elif type_of_modeling == "Baksi 2020":
            self.create_baksi_inequalities()
            pass
        else:
            raise ValueError(
                "Variable type_of_modeling declared incorrectly. Value should be 'SunEtAl 2013' or 'Baksi 2020'.")
        return


class XorAction(CipherAction):
    def __init__(self, inputs, output, dummy, cipher_instance):
        super().__init__("xor", cipher_instance)
        (self.input_var_1, self.input_var_2), self.output_var = inputs, output
        self.dummy_var = dummy
        return

    def run_action(self):
        # inequalities of xor are
        # (1.) input1 + input2 + output \leq 2*dummy
        # (2.) input1 \leq dummy
        # (3.) input2 \leq dummy
        # (4.) output \leq dummy
        dummy_var_pos_in_matrix = self.cipher_instance.V[self.dummy_var]

        # starting with (1.)
        self.set_all_to_value(list_of_variables=[self.input_var_1, self.input_var_2, self.output_var], value=1)
        self.cipher_instance.M[self.cipher_instance.line, dummy_var_pos_in_matrix] = -2
        self.cipher_instance.line += 1

        # then (2.), (3.), and (4.)
        self.for_each_var_set_to_value_plus_dummy(
            list_of_variables=[self.input_var_1, self.input_var_2, self.output_var], var_value=-1,
            dummy_pos=dummy_var_pos_in_matrix, dum_value=1)
        return


class LinTransformationAction(CipherAction):
    def __init__(self, inputs, outputs, dummy, cipher_instance):
        super().__init__("lin trans", cipher_instance)
        (self.input_var_1, self.input_var_2), (self.output_var_1, self.output_var_2) = inputs, outputs
        self.dummy_var = dummy
        return

    def run_action(self):
        # inequalities of linear transformations are
        # (1.) input1 + input2 + output1 + output2 \leq 3*dummy
        # (2.) input1 \leq dummy
        # (3.) input2 \leq dummy
        # (4.) output1 \leq dummy
        # (5.) output2 \leq dummy
        dummy_var_pos_in_matrix = self.cipher_instance.V[self.dummy_var]

        all_io_variables = [self.input_var_1, self.input_var_2, self.output_var_1, self.output_var_2]
        # starting with (1.)
        self.set_all_to_value(list_of_variables=all_io_variables, value=1)
        self.cipher_instance.M[self.cipher_instance.line, dummy_var_pos_in_matrix] = -3
        self.cipher_instance.line += 1

        # then (2.), (3.), (4.), and (5.)
        self.for_each_var_set_to_value_plus_dummy(
            list_of_variables=all_io_variables, var_value=-1,
            dummy_pos=dummy_var_pos_in_matrix, dum_value=1)
        return
