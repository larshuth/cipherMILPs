from cipher.action import CipherAction


class OverwriteAction(CipherAction):
    def __init__(self, input_indices, cipher_instance):
        super().__init__("overwrite", cipher_instance)
        self.input_indices = input_indices
        return

    def run_action(self):
        print(self.type_of_action, self.input_indices)
        for i in self.input_indices:
            new_var = 'x' + str(self.cipher_instance.next['x'])
            self.cipher_instance.A[i] = new_var
            self.cipher_instance.next['x'] += 1
        return
