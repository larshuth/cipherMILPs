class Sbox:
    def __init__(self, substitutions, in_bits, out_bits):
        self.substitutions, self.in_bits, self.out_bits = substitutions, in_bits, out_bits
        self.non_zero_ddt_entries_built = False
        self.non_zero_ddt_entries = set()
        self.vectors = set()
        return

    def build_ddt(self):
        return

    def build_non_zero_ddt_entries(self):
        self.non_zero_ddt_entries = set()
        for in_val_1, out_val_1 in self.substitutions.items():
            for in_val_2, out_val_2 in self.substitutions.items():
                self.non_zero_ddt_entries |= {(in_val_1 ^ in_val_2, out_val_1 ^ out_val_2)}
        self.non_zero_ddt_entries_built = True
        return

    def build_non_zero_ddt_entries_vectors(self):
        self.vectors = set()
        for x, y in (self.non_zero_ddt_entries ^ {(0, 0)}):
            vector = list()
            for i in range(0, self.in_bits):
                if 2 ** i >= x:
                    vector.append(1)
                    x -= 2 ** i
                else:
                    vector.append(0)

            for i in range(0, self.out_bits):
                if 2 ** i >= y:
                    vector.append(1)
                    y -= 2 ** i
                else:
                    vector.append(0)
            self.vectors |= {tuple(vector.copy())}
        return

    def build_lat(self):
        return
