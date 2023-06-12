from sage.all import *
import sage.geometry.polyhedron.base


def ch_hrep_and_equations_from_sbox(sbox_instance):
    sbox_instance.build_non_zero_ddt_entries_vectors()
    con_hul_hrep_split_into_lines = ch_hrep_from_vectors(sbox_instance.vectors)
    con_hul_equations_list = ch_equations_list_from_vectors(sbox_instance.vectors)
    return con_hul_hrep_split_into_lines, con_hul_equations_list


def ch_hrep_from_sbox(sbox_instance):
    sbox_instance.build_non_zero_ddt_entries_vectors()
    con_hul_hrep_split_into_lines = ch_hrep_from_vectors(sbox_instance.vectors)
    return con_hul_hrep_split_into_lines


def ch_hrep_from_vectors(vectors):
    con_hul = sage.geometry.polyhedron.base.Polyhedron(vertices=list(vectors))
    con_hul_hrep = con_hul.Hrepresentation_str()
    con_hul_hrep_split_into_lines = con_hul_hrep.split("\n")
    return con_hul_hrep_split_into_lines


def ch_equations_list_from_sbox(sbox_instance):
    sbox_instance.build_non_zero_ddt_entries_vectors()
    con_hul_equations_list = ch_equations_list_from_vectors(sbox_instance.vectors)
    return con_hul_equations_list


def ch_equations_list_from_vectors(vectors):
    con_hul = sage.geometry.polyhedron.base.Polyhedron(vertices=list(vectors))
    con_hul_equations_list = con_hul.equations_list()
    return con_hul_equations_list
