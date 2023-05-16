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
        print(self.type_of_action, self.permutation)
        backup = self.cipher_instance.A.copy()
        for i in range(self.cipher_instance.plaintext_vars):
            self.cipher_instance.A[i] = backup[self.permutation[i]]
        return
