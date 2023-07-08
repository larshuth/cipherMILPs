from cipher.action import CipherAction


class ThreeForkedBranchAction(CipherAction):
    def __init__(self, input_var, cipher_instance, a_positions_to_overwrite=(None, None),
                 linear_helper_positions_to_overwrite=(None, None), optional_output_vars=(None, None)):
        super().__init__("twf", cipher_instance)
        self.input_var = input_var

        if optional_output_vars[0] is None:
            self.output_var_1 = 'x' + str(self.cipher_instance.next['x'])
            self.cipher_instance.next['x'] += 1
        else:
            self.output_var_1 = optional_output_vars[0]

        if optional_output_vars[1] is None:
            self.output_var_2 = 'x' + str(self.cipher_instance.next['x'])
            self.cipher_instance.next['x'] += 1
        else:
            self.output_var_2 = optional_output_vars[1]

        self.dummy_var = 'dt' + str(self.cipher_instance.next['dt'])
        self.cipher_instance.next['dt'] += 1
        self.a_positions_to_overwrite = a_positions_to_overwrite
        self.linear_helper_positions_to_overwrite = linear_helper_positions_to_overwrite
        return

    def run_action(self):
        # print(self.type_of_action, self.input_var, self.output_var_1, self.output_var_2)
        # inequalities of xor are
        # (1.) input1 + input2 + output \leq 2*dummy
        # (2.) input1 \leq dummy
        # (3.) input2 \leq dummy
        # (4.) output \leq dummy
        dummy_var_pos_in_matrix = self.cipher_instance.V[self.dummy_var]

        input_output_vars = [self.input_var, self.output_var_1, self.output_var_2]
        # starting with (1.)
        self.set_all_to_value(list_of_variables=input_output_vars, value=1)
        self.cipher_instance.M[self.cipher_instance.line, dummy_var_pos_in_matrix] = -2
        self.cipher_instance.line += 1

        # then (2.), (3.), and (4.)
        self.for_each_var_set_to_value_plus_dummy(
            list_of_variables=input_output_vars, var_value=-1,
            dummy_pos=dummy_var_pos_in_matrix, dum_value=1)

        if self.a_positions_to_overwrite[0] is not None:
            self.cipher_instance.A[self.a_positions_to_overwrite[0]] = self.output_var_1
        if self.a_positions_to_overwrite[1] is not None:
            self.cipher_instance.A[self.a_positions_to_overwrite[1]] = self.output_var_2

        if self.linear_helper_positions_to_overwrite[0] is not None:
            self.cipher_instance.linear_helper[self.linear_helper_positions_to_overwrite[0]] = self.output_var_1
        if self.linear_helper_positions_to_overwrite[1] is not None:
            self.cipher_instance.linear_helper[self.linear_helper_positions_to_overwrite[1]] = self.output_var_2

        return
