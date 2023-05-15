from cipher.actions import CipherAction


class LinTransformationAction(CipherAction):
    def __init__(self, inputs, cipher_instance, branch_number=2, a_positions_to_overwrite=None):
        super().__init__("lin trans", cipher_instance)
        self.input_list = inputs

        self.output_list = list()
        for i in range(len(self.input_list)):
            self.output_list.append('x' + str(self.cipher_instance.next['x']))
            self.cipher_instance.next['x'] += 1

        self.dummy_var = 'dl' + str(self.cipher_instance.next['dl'])
        self.cipher_instance.next['dl'] += 1

        self.branch_number = branch_number
        self.a_positions_to_overwrite = a_positions_to_overwrite
        print("created", self.type_of_action, self.input_list, self.dummy_var)
        return

    def run_action(self):
        # inequalities of linear transformations are
        # (1.) input1 + input2 + output1 + output2 \leq 3*dummy
        # (2.) input1 \leq dummy
        # (3.) input2 \leq dummy
        # (4.) output1 \leq dummy
        # (5.) output2 \leq dummy
        print("run", self.type_of_action, self.input_list, self.dummy_var)
        dummy_var_pos_in_matrix = self.cipher_instance.V[self.dummy_var]

        all_io_variables = self.input_list + self.output_list
        # starting with (1.)
        self.set_all_to_value(list_of_variables=all_io_variables, value=1)
        self.cipher_instance.M[self.cipher_instance.line, dummy_var_pos_in_matrix] = - self.branch_number
        self.cipher_instance.line += 1

        # then (2.), (3.), (4.), and (5.)
        self.for_each_var_set_to_value_plus_dummy(
            list_of_variables=all_io_variables, var_value=-1,
            dummy_pos=dummy_var_pos_in_matrix, dum_value=self.branch_number)

        if self.a_positions_to_overwrite:
            for index, pos in enumerate(self.a_positions_to_overwrite):
                self.cipher_instance.A[pos] = self.output_list[index]
        return
