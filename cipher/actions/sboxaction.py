from scipy.sparse import lil_matrix

import convexHull
from cipher.action import CipherAction


class SBoxAction(CipherAction):
    """
    A class to perform tasks of overwriting variables and creating inequalities as they would be required by a S-box.
    Quite a few methods are introduced in this part since we are implementing a few different approaches to how the
    inequalities which represent S-boxes and make sure e.g. that no impossible transitions are allowed.
    """
    def __init__(self, sbox, input_vars, cipher_instance, first_a_position_to_overwrite=None, optional_output_vars=None) -> None:
        """
        Constructs an instance of SBoxAction.

        :param Type[SBox] sbox: instance of class SBox representing the S-box we are currently working on
        :param list of str input_vars: List including all the string names of all input variables that are input for the
                previously defined S-box. For bit-oriented, list goes from variable representing the most significant
                bit to the one representing the least significant bit. For word oriented, it is a list with just the
                string representing the variable of all the input bits.
        :param Cipher cipher_instance:The instance of one of the cipher classes found in cipher/differential/ and
                cipher/linear/ that we are operating on.
        :param int first_a_position_to_overwrite: index of the first element in cipher_instance.A to be overwritten,
                i.e. first position where we the save the names of the variable representing the output of the sbox
        :param list of (str or None) or None optional_output_vars: Optional output variables are used if we are
                interested in not getting just any new x variables in accordance with cipher_instance.next['x'] but
                instead want specific outputs. Either None if not no prefered output variables or list with None in
                positions we are not interested in and string like 'x123' in the i-th position if we want the i-th bit to
                be represented by this specific variable. optional_output_vars is arranged like input_vars
        """
        # ensuring self.type_of_action, self.cipher_instance are set and functions set_all_to_value and
        # for_each_var_set_to_value_plus_dummy are inherited

        super().__init__("sbox", cipher_instance)

        # assigning attributes
        self.sbox = sbox

        self.input_vars = input_vars

        # setting those output variables that have not been specified in optional_output_vars
        if optional_output_vars is None:
            self.output_vars = ['x' + str(self.cipher_instance.next['x'] + i) for i in range(self.sbox.out_bits)]
            self.cipher_instance.next['x'] += self.sbox.out_bits
        else:
            self.output_vars = [None for _ in range(self.sbox.out_bits)]
            for i in range(self.sbox.out_bits):
                if optional_output_vars[i] is None:
                    self.output_vars[i] = 'x' + str(self.cipher_instance.next['x'])
                    self.cipher_instance.next['x'] += 1
                else:
                    self.output_vars[i] = optional_output_vars[i]

        self.dummy_var = 'a' + str(self.cipher_instance.next['a'])
        self.cipher_instance.next['a'] += 1

        self.dummy_var_pos_in_matrix = self.cipher_instance.V[self.dummy_var]

        # variables for the approach to S-box modelling described in Baksi 2020.
        # TODO rename vars
        self.qijp_vars = list()
        self.qijlp_vars = list()

        self.overwrite_position = first_a_position_to_overwrite
        return

    def input_leq_dummy(self) -> None:
        """
        Writing inequality input_i \\leq dummy variable for each variable input_i in self.input_vars.
        Increments the line number such that it points to an empty line after this function finishes.
        """
        self.for_each_var_set_to_value_plus_dummy(self.input_vars, 1, self.dummy_var_pos_in_matrix, -1)
        return

    def sum_over_all_inputs_geq_dummy(self) -> None:
        """
        Writing inequality to cipher_instance.M equaling that the sum over all variables in self.input_vars is greater
        or equal to the dummy variable.
        Increments the line number such that it points to an empty line after this function finishes.
        """
        self.set_all_to_value(self.input_vars, -1)
        self.cipher_instance.M[self.cipher_instance.line, self.dummy_var_pos_in_matrix] = 1
        self.cipher_instance.line += 1
        return

    def non_zero_input_implies_non_zero_output(self) -> None:
        """
        Writing inequality to cipher_instance.M equaling that if at least one input variable is 1 then at least one
        output variable is 1 as well.
        Increments the line number such that it points to an empty line after this function finishes.
        """
        self.set_all_to_value(self.input_vars, -1)
        self.set_all_to_value(self.output_vars, self.sbox.out_bits)
        self.cipher_instance.line += 1
        return

    def non_zero_output_implies_non_zero_input(self) -> None:
        """
        Writing inequality to cipher_instance.M equaling that if at least one output variable is 1 then at least one
        input variable is 1 as well.
        Increments the line number such that it points to an empty line after this function finishes.
        """
        self.set_all_to_value(self.input_vars, self.sbox.out_bits)
        self.set_all_to_value(self.output_vars, -1)
        self.cipher_instance.line += 1
        return

    def branch_number_inequality(self) -> None:
        """
        Sun et al. 2013 introduces constraints which become necessary if (the branch number of is larger than 2) or (the
        S-box is not bijective). These are redundant with proper modelling of feasible S-box transitions, but I assume
        they make the process faster by excluding a large amount of impossible transitions without the inclusion of more
        specific constraints/inequalities.

        The introduced constraints are
        (4.1) sum over inputs + sum over outputs \\geq branch * new dummy
        (4.2) input \\leq new dummy for all inputs
        (4.3) output \\leq dummy for all outputs
        Numbering of constraints is in accordance with the run_action method
        """
        extra_constraint_dummy_var = 'ds' + str(self.cipher_instance.next['ds'])
        self.cipher_instance.next['ds'] += 1

        extra_constraint_dummy_var_pos_in_matrix = self.cipher_instance.V[extra_constraint_dummy_var]

        # (4.1)
        # setting all input vars and output vars to 1
        self.set_all_to_value(self.input_vars, 1)
        self.set_all_to_value(self.output_vars, 1)
        # setting dummy to branch_number
        self.cipher_instance.M[
            self.cipher_instance.line, extra_constraint_dummy_var_pos_in_matrix] = - self.sbox.branch_number
        self.cipher_instance.line += 1

        # (4.2)
        # for every input var, a new inequality is made with the var \leq dummy
        self.for_each_var_set_to_value_plus_dummy(self.input_vars, -1, extra_constraint_dummy_var_pos_in_matrix, 1)

        # (4.3)
        # for every output var, a new inequality is made with the var \leq dummy
        self.for_each_var_set_to_value_plus_dummy(self.output_vars, -1, extra_constraint_dummy_var_pos_in_matrix, 1)
        return

    def create_convex_hull_matrices(self, choice_of_inequalities='all', baksi_extension=True) -> None:
        constant_pos = self.cipher_instance.V["constant"]

        inequalities = convexHull.ch_hrep_from_sbox(self.sbox)
        print(inequalities)
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
        if choice_of_inequalities == 'all':
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
                        variables_not_zero |= {modifier * int(character)}

                for index, i in enumerate(self.input_vars):
                    if index in variables_not_zero:
                        input_var_pos_in_matrix = self.cipher_instance.V[i]
                        convex_hull_inequality_matrix[convex_hull_inequality_matrix_line, input_var_pos_in_matrix] = 1
                    elif -index in variables_not_zero:
                        input_var_pos_in_matrix = self.cipher_instance.V[i]
                        convex_hull_inequality_matrix[convex_hull_inequality_matrix_line, input_var_pos_in_matrix] = -1

                for index, i in enumerate(self.output_vars):
                    if index + self.sbox.in_bits in variables_not_zero:
                        input_var_pos_in_matrix = self.cipher_instance.V[i]
                        convex_hull_inequality_matrix[convex_hull_inequality_matrix_line, input_var_pos_in_matrix] = 1
                    elif -(index + self.sbox.in_bits) in variables_not_zero:
                        input_var_pos_in_matrix = self.cipher_instance.V[i]
                        convex_hull_inequality_matrix[convex_hull_inequality_matrix_line, input_var_pos_in_matrix] = -1

                value_right_of_inequality = -int(lesser)
                convex_hull_inequality_matrix[convex_hull_inequality_matrix_line, constant_pos] = value_right_of_inequality
                convex_hull_inequality_matrix_line += 1
        elif choice_of_inequalities == 'greedy':
            # TODO: calculate excluded points and include inequalities by the amount of points they exclude until no
            #  more impossible transitions can be excluded by the inequalities
            pass

        if baksi_extension:
            pass

        self.cipher_instance.sbox_inequality_matrices.append(convex_hull_inequality_matrix)
        return

    def create_baksi_inequalities(self) -> None:
        if not self.sbox.is_bijective:
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

        return

    def run_action(self, type_of_modeling="SunEtAl 2013") -> None:
        """
        Substitutes variables in the cipher instance such that the input variables are replaced and not mistakenly used
        further on in the cryptanalysis process.

        Generate constraints to cipher_instance.M in accordance with Sun et al. 2013 which are
        (1.) input \\leq dummy for all inputs
        (2.) sum over all inputs \\geq dummy
        (3.) if S-box bijective: sum_{i \\in all_inputs}
        (4.) if the S-box invertible with branch number 2:
        (4.1) sum over inputs + sum over outputs \\geq branch * new dummy
        (4.2) input \\leq new dummy for all inputs
        (4.3) output \\leq dummy for all outputs

        :param str type_of_modeling: Either 'SunEtAl 2013', 'Baksi 2020' or 'Boura 2020'

        Disclaimer: Baksi and Boura are yet to be implemented
        """

        print(self.type_of_action, self.input_vars)

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
            self.branch_number_inequality()

        if type_of_modeling == "SunEtAl 2013":
            self.create_convex_hull_matrices()
        elif type_of_modeling == "Baksi 2020":
            self.create_baksi_inequalities()
            pass
        else:
            raise ValueError(
                "Variable type_of_modeling declared incorrectly. Value should be 'SunEtAl 2013' or 'Baksi 2020'.")

        if type(self.overwrite_position) == int:
            for i in range(self.sbox.in_bits):
                self.cipher_instance.A[self.overwrite_position + i] = self.output_vars[i]
        return
