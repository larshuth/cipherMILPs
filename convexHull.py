import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
import cipher as cip
from sage.geometry.polyhedron.base import Polyhedron_base


def sbox_modeling_as_vectors(sbox):
    """
    Function calculating the vector representation of a given S-Box as described in "Automatic Security Evaluation and
    (Related-key) Differential Chrarcteristic Search: Application to SIMON, PRESENT, LBlock, DES(L) and Other
    Bit-oriented Block Ciphers" by Sun et at. 2013

    @param sbox:
            tuple with
                input size (#bits) and
                dictionary from input to output (both as int)
    @return:
        returns list of NumPy vectors (bool values)
    """
    Polyhedron_base(vertices=sbox).Hrepresentation_str(style="<=")

    return False

def