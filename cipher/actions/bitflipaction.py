from cipher.action import CipherAction

class BitFlipAction(CipherAction):
    """
    A class to perform tasks of overwriting variables and creating inequalities as they would be required by a bit-flip
    in a linear or differential cryptanalysis.
    """
    def __init__(self, inputs, cipher_instance, a_positions_to_overwrite=None) -> None:
        """
        Constructs an instance of BitFlipAction.

        :param list of str inputs: A list of strings representing the input variables, e.g. ['x34', 'x35']
        :param cipher_instance: The instance of one of the cipher classes found in cipher/differential/ and
                cipher/linear/ that we are operating on
        :param list of int or None a_positions_to_overwrite: Each cipher_instance has an attribute A (list) which notes down the currently
                worked on variables. Give that we describe the output of a linear transformation using a new variable,
                e.g. 'x35' and 'x36' in Mouha et al. Enocoro, we overwrite the positions that 'x34' and 'x35' were saved
                on previously.
        """

        # ensuring self.type_of_action, self.cipher_instance are set and functions set_all_to_value and
        # for_each_var_set_to_value_plus_dummy are inherited
        super().__init__("bitflip", cipher_instance)

        # assigning attributes
        self.input_list = inputs

        self.output_list = list()
        for i in range(len(self.input_list)):
            self.output_list.append('x' + str(self.cipher_instance.next['x']))
            self.cipher_instance.next['x'] += 1

        self.a_positions_to_overwrite = a_positions_to_overwrite
        return

    def run_action(self) -> None:
        """
        Generates constraints and substitutes variables such that for input variables x_1, ..., x_n the output
        variables y_1, ..., y_n are set to x_i = not y_i for all i in {1, ..., n}.

        (1.) x_i \\geq 1 - y_i  ==> x_i + y_i - 1 \\geq 0
        (2.) x_i \\leq 1 - y_i  ==> - x_i - y_i + 1 \\geq 0

        Which holds
        """
        map_input_to_output = zip(self.input_list, self.output_list)
        # for all input-output-pairs apply (1.) and (2.)
        for in_bit, out_bit in map_input_to_output:
            # (1.)
            in_bit_pos = self.cipher_instance.V[in_bit]
            out_bit_pos = self.cipher_instance.V[out_bit]
            constant_pos = self.cipher_instance.V['constant']
            self.cipher_instance.M[self.cipher_instance.line, in_bit_pos] = 1
            self.cipher_instance.M[self.cipher_instance.line, out_bit_pos] = 1
            self.cipher_instance.M[self.cipher_instance.line, constant_pos] = - 1
            self.cipher_instance.line += 1
            # (2.)
            self.cipher_instance.M[self.cipher_instance.line, in_bit_pos] = -1
            self.cipher_instance.M[self.cipher_instance.line, out_bit_pos] = -1
            self.cipher_instance.M[self.cipher_instance.line, constant_pos] = 1
            self.cipher_instance.line += 1

        if self.a_positions_to_overwrite:
            for index, pos in enumerate(self.a_positions_to_overwrite):
                self.cipher_instance.A[pos] = self.output_list[index]
        return map_input_to_output
