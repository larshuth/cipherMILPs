from cipher.action import CipherAction


class OverwriteAction(CipherAction):
    """
    A class to perform tasks of overwriting variables if required.
    Never required so far, was created due to a misunderstanding.
    """
    def __init__(self, input_indices, cipher_instance, equality=False):
        super().__init__("overwrite", cipher_instance)
        self.input_indices = input_indices
        self.equality = equality
        return

    def run_action(self):
        # print(self.type_of_action, self.input_indices)
        for i in self.input_indices:
            old_var = self.cipher_instance.A[i]
            new_var = 'x' + str(self.cipher_instance.next['x'])
            self.cipher_instance.A[i] = new_var
            self.cipher_instance.next['x'] += 1
            if self.equality:
                self.set_all_to_value([old_var], value=1)
                self.set_all_to_value([new_var], value=-1)
                self.cipher_instance.line += 1
                self.set_all_to_value([new_var], value=1)
                self.set_all_to_value([old_var], value=-1)
                self.cipher_instance.line += 1
        return
