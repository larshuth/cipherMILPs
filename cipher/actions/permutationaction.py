from cipher.action import CipherAction


class PermutationAction(CipherAction):
    """
        A class to perform tasks of permuting some of the lists in instances of our cipher classes. Why did I not simply
        make them into a function in the cipher superclass? Next question please!
        """

    def __init__(self, permutation, cipher_instance):
        super().__init__("permutation", cipher_instance)
        # watch that the list says what should be replaced by what, i.e. if the original is [a,b,c,d] and after that it
        # says [b,d,a,c] then the permutation list is [1,3,0,2]
        self.permutation = permutation
        return

    def run_action(self):
        def apply_permutation(backup):
            for i in range(self.cipher_instance.plaintext_vars):
                self.cipher_instance.A[i] = backup[self.permutation[i]]
            return

        def increment_and_return_prev_val_as_string(var='x'):
            self.cipher_instance.next[var] += 1
            return str(self.cipher_instance.next[var] - 1)

        backup = self.cipher_instance.A.copy()

        try:
            if self.cipher_instance.permutation_as_constraints:
                self.cipher_instance.A = ['x' + increment_and_return_prev_val_as_string() for _ in
                                          range(len(self.cipher_instance.A))]

                for pos, val in enumerate(self.permutation):
                    old_var = backup[pos]
                    new_var = self.cipher_instance.A[val]

                    self.set_all_to_value([old_var], value=1)
                    self.set_all_to_value([new_var], value=-1)
                    self.cipher_instance.line += 1
                    self.set_all_to_value([new_var], value=1)
                    self.set_all_to_value([old_var], value=-1)
                    self.cipher_instance.line += 1
            else:
                apply_permutation(backup)
        except:
            apply_permutation(backup)
        return
