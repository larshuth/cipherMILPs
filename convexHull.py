import numpy as np
from sage.all import *
import sage.geometry.polyhedron.base
from scipy.sparse import csr_matrix, lil_matrix
import cipher as cip


def ch_hrep_from_sbox(sbox_instance):
    sbox_instance.build_non_zero_ddt_entries()
    sbox_instance.build_non_zero_ddt_entries_vectors()
    ch_hrep_from_vectors(sbox_instance.vectors)
    return


def ch_hrep_from_vectors(vectors):
    print(sage.geometry.polyhedron.base.Polyhedron(vertices=vectors).Hrepresentation().vector())
    return
