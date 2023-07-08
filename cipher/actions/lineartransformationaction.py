from cipher.action import CipherAction


class LinTransformationAction(CipherAction):
    """
    A class to perform tasks of overwriting variables and creating inequalities as they would be required by a linear
    transformation in a linear or differential cryptanalysis.

    All of the following examples are taken from the linear transformation perfomred in the first round of a linear
    cryptanalysis on Enocoro-128v2 as seen in Mouha et al. 2011.
    """
    def __init__(self, inputs, cipher_instance, branch_number=2, a_positions_to_overwrite=None) -> None:
        """
        Constructs an instance of LinTranformationAction.

        :param list of str inputs: A list of strings representing the input variables, e.g. ['x34', 'x35']
        :param cipher_instance: The instance of one of the cipher classes found in cipher/differential/ and
                cipher/linear/ that we are operating on
        :param int branch_number: The branch number of the linear transformation that is being performed. These have to be
                calculated by hand by the user (or searched up on the internet) e.g. the branch number of the linear
                transformation in Enocoro-128v2 is 3 according to Mouha et al.
        :param list of int or None a_positions_to_overwrite: Each cipher_instance has an attribute A (list) which notes down the currently
                worked on variables. Give that we describe the output of a linear transformation using a new variable,
                e.g. 'x35' and 'x36' in Mouha et al. Enocoro, we overwrite the positions that 'x34' and 'x35' were saved
                on previously.
        """
        # ensuring self.type_of_action, self.cipher_instance are set and functions set_all_to_value and
        # for_each_var_set_to_value_plus_dummy are inherited
        super().__init__("lin trans", cipher_instance)

        # assigning attributes
        self.input_list = inputs

        self.output_list = list()
        for i in range(len(self.input_list)):
            self.output_list.append('x' + str(self.cipher_instance.next['x']))
            self.cipher_instance.next['x'] += 1

        self.dummy_var = 'dl' + str(self.cipher_instance.next['dl'])
        self.cipher_instance.next['dl'] += 1

        self.branch_number = branch_number
        self.a_positions_to_overwrite = a_positions_to_overwrite
        # print("created", self.type_of_action, self.input_list, self.dummy_var)
        return

    def run_action(self) -> None:
        """
        Generates constraints and substitutes variables in accordance with the Mouha et al. 2011
        inequalities of linear transformations are
        (1.) input1 + input2 + output1 + output2 \\leq 3*dummy
        (2.) input_i \\leq dummy, for all input_i in {input_vars}
        (3.) output_i \\leq dummy, for all output_i in {output_vars}
        """
        # print("run", self.type_of_action, self.input_list, self.dummy_var)
        dummy_var_pos_in_matrix = self.cipher_instance.V[self.dummy_var]

        all_io_variables = self.input_list + self.output_list
        # starting with (1.)
        self.set_all_to_value(list_of_variables=all_io_variables, value=1)
        self.cipher_instance.M[self.cipher_instance.line, dummy_var_pos_in_matrix] = - self.branch_number
        self.cipher_instance.line += 1

        # then (2.) and (3.)
        self.for_each_var_set_to_value_plus_dummy(
            list_of_variables=all_io_variables, var_value=-1,
            dummy_pos=dummy_var_pos_in_matrix, dum_value=self.branch_number)

        if self.a_positions_to_overwrite:
            for index, pos in enumerate(self.a_positions_to_overwrite):
                self.cipher_instance.A[pos] = self.output_list[index]
        return
