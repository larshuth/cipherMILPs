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
