from scipy.sparse import lil_matrix
import re
from itertools import chain
import convexHull
from cipher.action import CipherAction


class SBoxAction(CipherAction):
    """
    A class to perform tasks of overwriting variables and creating inequalities as they would be required by a S-box.
    Quite a few methods are introduced in this part since we are implementing a few different approaches to how the
    inequalities which represent S-boxes and make sure e.g. that no impossible transitions are allowed.
    """

    def __init__(self, sbox, input_vars, cipher_instance, first_a_position_to_overwrite=None,
                 optional_output_vars=None) -> None:
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
        :param list [str | None] | None optional_output_vars: Optional output variables are used if we are
                interested in not getting just any new x variables in accordance with cipher_instance.next['x'] but
                instead want specific outputs. Either None if not no prefered output variables or list with None in
                positions we are not interested in and string like 'x123' in the i-th position if we want the i-th bit to
                be represented by this specific variable. optional_output_vars is arranged like input_vars
        :param str type_of_modeling: Either 'SunEtAl 2013', 'Baksi 2020' or 'Boura 2020'
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

    def inequality_to_constraint_matrix(self, inequality: tuple[list[int], int, set[int]], convex_hull_inequality_matrix, convex_hull_inequality_matrix_line, constant_pos):
        multipliers, value_right_of_inequality, _ = inequality
        for index, val in enumerate(multipliers):
            if (index < self.sbox.in_bits) and (val != 0):
                # here we check strictly smaller since the variable numbers start at 0
                variable_name_for_key = self.input_vars[index - 1]
                var_pos_in_matrix = self.cipher_instance.V[variable_name_for_key]
                convex_hull_inequality_matrix[convex_hull_inequality_matrix_line, var_pos_in_matrix] = val
            elif val != 0:
                variable_name_for_key = self.output_vars[index - self.sbox.in_bits - 1]
                var_pos_in_matrix = self.cipher_instance.V[variable_name_for_key]
                convex_hull_inequality_matrix[convex_hull_inequality_matrix_line, var_pos_in_matrix] = val
        convex_hull_inequality_matrix[
            convex_hull_inequality_matrix_line, constant_pos] = value_right_of_inequality
        convex_hull_inequality_matrix_line += 1
        return convex_hull_inequality_matrix_line

    def create_convex_hull_matrices(self, choice_of_inequalities='all', baksi_extension=True) -> None:
        """
        Sun et al. 2013 introduces the concept of applying a convex hull over a set of vectors representing the feasible
        transitions of an S-box in order to generate constraints which should only be fulfilled iff the (variables
        representing the) input and output bits have taken values of a feasible transition.

        :param str choice_of_inequalities: "all" or "greedy" to decide which of the convex hull constraints are included
                in our matrix
        :param bool baksi_extension: deciding whether to use the extension introduced in Basksi 2020
        """
        constant_pos = self.cipher_instance.V["constant"]

        inequalities_readable = self.sbox.feasible_transition_inequalities_sun_2013_extracted.copy()
        # adding a new sparse scipy matrix convex_hull_inequality_matrix for the constraints as we cannot count
        # them prior to this even and self.M would otherwise overflow
        convex_hull_inequality_matrix = lil_matrix((len(inequalities_readable), self.cipher_instance.number_variables),
                                                   dtype=int)
        convex_hull_inequality_matrix_line = 0

        # either we are going to include all constraints in the
        if choice_of_inequalities == 'all':
            for inequality in inequalities_readable:
                convex_hull_inequality_matrix_line = self.inequality_to_constraint_matrix(inequality, convex_hull_inequality_matrix, convex_hull_inequality_matrix_line, constant_pos)
        # or just greedily choose those which include the most
        elif choice_of_inequalities == 'greedy':
            if inequalities_readable == list():
                raise Exception(
                    "the 'extract_sun_inequalities' argument has not been set in the construction of the currently " +
                    "worked on S-box. Therefore, since we have not calculated the impossible transitions, we cannot " +
                    "perform a greedy choice on them.")
            still_impossible_transitions_left = True
            while still_impossible_transitions_left:
                print(len(inequalities_readable))
                still_impossible_transitions_left = False
                max_inequal = (list(), 0, set())
                for inequality in inequalities_readable:
                    if len(inequality[2]) > len(max_inequal[2]):
                        max_inequal = inequality
                convex_hull_inequality_matrix_line = self.inequality_to_constraint_matrix(max_inequal, convex_hull_inequality_matrix, convex_hull_inequality_matrix_line, constant_pos)

                if max_inequal in inequalities_readable:
                    print('Should be in there')
                else:
                    print(inequalities_readable)
                    print(max_inequal)
                inequalities_readable.remove(max_inequal)
                # finally we remove the impossible transitions which have been removed by adding max_inequal from the
                # remaining inequalities such that we can always greedily choose the inequality, which removes as many
                # impossible transitions as possible, as the next constraint
                for inequality in inequalities_readable:
                    inequality[2] = inequality[2] - max_inequal[2]
                    if len(inequality[2]) > 0:
                        still_impossible_transitions_left = True

        if baksi_extension:
            # Baksi suggests that adding equality constraints provided by the sage API and not only inequality
            # constraints "will likely not appear"

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
        #
        # for each p transition do
        # (3.)

        constant_pos = self.cipher_instance.V["constant"]
        big_m = 2 * self.sbox.in_bits
        qijp_vars = [self.dummy_var + f'p{p}' for p in self.sbox.set_of_transition_values]

        # TODO find number of inequalities
        number_of_inequalities = 1 + 2 + (2 * len(qijp_vars)) + sum([len(table_column) for table_column, value in self.sbox.dict_value_to_list_of_transition.items()])

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

        # (3.)
        extract_p = lambda qijp_var: int(qijp_var[len(self.dummy_var):])

        for qijp_var in qijp_vars:
            p = extract_p(qijp_var)
            qijlp_vars = {qijp_var + f'l{l}': transition for l, transition in enumerate(self.sbox.dict_value_to_list_of_transition[p])}
            list_of_qijlp_vars = list(qijlp_vars)
            print(qijlp_vars)

            self.set_all_to_value(list_of_variables=list_of_qijlp_vars, value=1, line_var=sbox_inequality_matrix_line,
                                  matrix_to_be_set=sbox_inequality_matrix)
            sbox_inequality_matrix[sbox_inequality_matrix_line, self.cipher_instance.V[qijp_var]] = -1
            sbox_inequality_matrix_line += 1

            self.set_all_to_value(list_of_variables=list_of_qijlp_vars, value=-1, line_var=sbox_inequality_matrix_line,
                                  matrix_to_be_set=sbox_inequality_matrix)
            sbox_inequality_matrix[sbox_inequality_matrix_line, self.cipher_instance.V[qijp_var]] = 1
            sbox_inequality_matrix_line += 1
            for qijlp_var, transition in qijlp_vars.items():
                # extract bit representation from transition
                bitwise_input_diff = [1 if (((2 ** i) & transition[0]) > 0) else 0 for i in range(self.sbox.in_bits - 1, -1, -1)]
                bitwise_output_diff = [1 if (((2 ** i) & transition[1]) > 0) else 0 for i in range(self.sbox.in_bits - 1, -1, -1)]

                # sum up bits which would be 1 for constant
                sum_of_all_bits = sum(bitwise_input_diff) + sum(bitwise_output_diff)
                sbox_inequality_matrix[sbox_inequality_matrix_line, constant_pos] = sum_of_all_bits

                # set all value: variables for bits which should be 0 to -1
                # set all value: variables for bits which should be 1 to 1
                plus_vars = list()
                minus_vars = list()
                for index, in_bit in enumerate(bitwise_input_diff):
                    if in_bit:
                        minus_vars.append(self.input_vars[index])
                    else:
                        plus_vars.append(self.input_vars[index])
                for index, out_bit in enumerate(bitwise_output_diff):
                    if out_bit:
                        minus_vars.append(self.output_vars[index])
                    else:
                        plus_vars.append(self.output_vars[index])

                self.set_all_to_value(list_of_variables=minus_vars, value=-1, line_var=sbox_inequality_matrix_line,
                                      matrix_to_be_set=sbox_inequality_matrix)
                self.set_all_to_value(list_of_variables=plus_vars, value=+1, line_var=sbox_inequality_matrix_line,
                                      matrix_to_be_set=sbox_inequality_matrix)
                # the next one, I do not entirely understand
                # it would be 0 iff the transition we look at is chosen
                # the comparison with the big M leads to
                sbox_inequality_matrix[sbox_inequality_matrix_line, self.cipher_instance.V[qijlp_var]] = big_m
                sbox_inequality_matrix_line += 1

        return

    def run_action(self) -> None:
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

        if self.cipher_instance.type_of_modeling == "SunEtAl 2013":
            self.create_convex_hull_matrices(choice_of_inequalities='all', baksi_extension=False)
        elif self.cipher_instance.type_of_modeling == "SunEtAl 2013 Greedy":
            self.create_convex_hull_matrices(choice_of_inequalities='greedy', baksi_extension=False)
        elif self.cipher_instance.type_of_modeling == "SunEtAl with 2013 Baksi extension 2020":
            self.create_convex_hull_matrices(choice_of_inequalities='all', baksi_extension=True)
        elif self.cipher_instance.type_of_modeling == "SunEtAl 2013 with Baksi extension 2020 Greedy":
            self.create_convex_hull_matrices(choice_of_inequalities='greedy', baksi_extension=True)
        elif self.cipher_instance.type_of_modeling == "Baksi 2020":
            self.create_baksi_inequalities()
            pass
        else:
            raise ValueError(
                "Variable type_of_modeling declared incorrectly. Value should be one of those listed in the docstring.")

        if type(self.overwrite_position) == int:
            for i in range(self.sbox.in_bits):
                self.cipher_instance.A[self.overwrite_position + i] = self.output_vars[i]
        return
