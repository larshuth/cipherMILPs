from sage.all import *
import sage.geometry.polyhedron.base


def ch_hrep_from_sbox(sbox_instance):
    sbox_instance.build_non_zero_ddt_entries_vectors()
    con_hul_hrep_split_into_lines = ch_hrep_from_vectors(sbox_instance.vectors)
    return con_hul_hrep_split_into_lines


def ch_hrep_from_vectors(vectors):
    con_hul_hrep = sage.geometry.polyhedron.base.Polyhedron(vertices=list(vectors)).Hrepresentation_str()
    con_hul_hrep_split_into_lines = con_hul_hrep.split("\n")
    return con_hul_hrep_split_into_lines
