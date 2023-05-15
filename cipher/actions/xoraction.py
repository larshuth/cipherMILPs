from cipher.actions import CipherAction


class XorAction(CipherAction):
    def __init__(self, inputs, cipher_instance, a_position_to_overwrite=None):
        super().__init__("xor", cipher_instance)
        (self.input_var_1, self.input_var_2) = inputs

        self.output_var = 'x' + str(self.cipher_instance.next['x'])
        self.cipher_instance.next['x'] += 1

        self.dummy_var = 'dx' + str(self.cipher_instance.next['dx'])
        self.cipher_instance.next['dx'] += 1

        self.overwrite = bool(type(a_position_to_overwrite) == int)
        self.a_position_to_overwrite = a_position_to_overwrite
        return

    def run_action(self):
        print(self.type_of_action, self.input_var_1, self.input_var_2)
        # inequalities of xor are
        # (1.) input1 + input2 + output \leq 2*dummy
        # (2.) input1 \leq dummy
        # (3.) input2 \leq dummy
        # (4.) output \leq dummy
        dummy_var_pos_in_matrix = self.cipher_instance.V[self.dummy_var]

        input_output_vars = [self.input_var_1, self.input_var_2, self.output_var]

        # starting with (1.)
        self.set_all_to_value(list_of_variables=input_output_vars, value=1)
        self.cipher_instance.M[self.cipher_instance.line, dummy_var_pos_in_matrix] = -2
        self.cipher_instance.line += 1

        # then (2.), (3.), and (4.)
        self.for_each_var_set_to_value_plus_dummy(
            list_of_variables=input_output_vars, var_value=-1,
            dummy_pos=dummy_var_pos_in_matrix, dum_value=1)

        if self.overwrite:
            self.cipher_instance.A[self.a_position_to_overwrite] = self.output_var
        return
