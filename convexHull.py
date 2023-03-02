import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
import cipher as cip
from sage.geometry.polyhedron.base import Polyhedron_base


# poly_test = Polyhedron ( vertices = myPoints )
# for v in poly_test . inequality_generator ():
#   print v


def ch_hrep_from_sbox(sbox_instance):
    sbox_instance.build_non_zero_ddt_entries()
    sbox_instance.build_non_zero_ddt_entries_vectors()
    ch_hrep_from_vectors(sbox_instance.vectors)
    return


def ch_hrep_from_vectors(vectors):
    for line in Polyhedron_base(vertices=vectors).Hrepresentation_str(style="<="):
        print(line)
    # in case it doesnt work try code from the top
    return
