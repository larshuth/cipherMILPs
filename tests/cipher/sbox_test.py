import unittest
from cipher.sbox import SBox
from cipher.differential.gift import Gift64
from cipher.actions.sboxaction import SBoxAction


class SBoxTest(unittest.TestCase):
    def test_branch_number(self):
        # testing branch number using the PRESENT SBox which is 3 accoridng to
        # https://crypto.stackexchange.com/questions/61075/number-of-active-s-boxes
        present_substitutions = {index: value for index, value in
                                 enumerate([12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2])}
        testbox = SBox(present_substitutions, 4, 4, None)
        self.assertEqual(3, testbox.branch_number)
        return

    def test_ddt(self):
        # testing using the S-box from the example in Sofia's bachelor thesis
        test_substitutions = {index: value for index, value in
                              enumerate([2, 5, 3, 1, 7, 0, 4, 6])}

        expected_ddt = [[8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0, 4], [0, 2, 0, 2, 2, 0, 2, 0],
                        [0, 2, 0, 2, 2, 0, 2, 0], [0, 0, 0, 0, 0, 4, 0, 4], [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 2, 0, 2, 2, 0, 2, 0], [0, 2, 0, 2, 2, 0, 2, 0]]

        testbox = SBox(test_substitutions, 3, 3, None)
        testbox.build_ddt()

        self.assertEqual(expected_ddt, testbox.ddt)
        return

    def test_find_impossible_transitions_for_each_sun_2013_inequality(self):
        present_substitutions = {index: value for index, value in
                                 enumerate([12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2])}
        testbox = SBox(present_substitutions, 4, 4, None)

        # we overwrite the inequalities as to have less work
        testbox.feasible_transition_inequalities_sun_2013 = ["-8*x2 + x1 >= 13"]

        # here, all the transitions should be impossible as (no matter what the other variables look like) x1 and x2
        # cannot be greater or equal than 13
        inequalities_readable = testbox.find_impossible_transitions_for_each_sun_2013_inequality(
            extract_sun_inequalities=True)

        self.assertEqual([([0, 1, -8, 0, 0, 0, 0, 0], -13,
                           {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                            25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
                            48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                            71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
                            94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112,
                            113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130,
                            131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148,
                            149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166,
                            167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184,
                            185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202,
                            203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220,
                            221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238,
                            239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255})],
                         inequalities_readable)

        testbox.feasible_transition_inequalities_sun_2013 = ["            x0 >=  0 "]

        # here, all the transitions should be feasible as (no matter what the other variables look like) x0
        # will always be greater or equal than 0
        inequalities_readable = testbox.find_impossible_transitions_for_each_sun_2013_inequality(
            extract_sun_inequalities=True)
        self.assertEqual(inequalities_readable, [([1, 0, 0, 0, 0, 0, 0, 0], 0, set())])

        testbox.feasible_transition_inequalities_sun_2013 = ["    x2 - 2*x1 >= 0"]

        # here, we have a mix of feasible and impossible transitions
        # given x2 - 2x1 >= 0, those transitions where x1 = 1 should all be impossible
        # since we transform x2 - 2x1 to [0, -2, 1, 0, 0, 0, 0, 0], all integer like [*, 1, *, *, , *, *, *, *], i.e.
        # all those whose binary sum (is that a correct term?) includes 2  should be found here
        inequalities_readable = testbox.find_impossible_transitions_for_each_sun_2013_inequality(
            extract_sun_inequalities=True)
        self.assertEqual([([0, -2, 1, 0, 0, 0, 0, 0], 0,
                           {2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31, 34, 35, 38, 39, 42, 43, 46, 47,
                            50, 51, 54, 55, 58, 59, 62, 63, 66, 67, 70, 71, 74, 75, 78, 79, 82, 83, 86, 87, 90, 91, 94,
                            95, 98, 99, 102, 103, 106, 107, 110, 111, 114, 115, 118, 119, 122, 123, 126, 127, 130, 131,
                            134, 135, 138, 139, 142, 143, 146, 147, 150, 151, 154, 155, 158, 159, 162, 163, 166, 167,
                            170, 171, 174, 175, 178, 179, 182, 183, 186, 187, 190, 191, 194, 195, 198, 199, 202, 203,
                            206, 207, 210, 211, 214, 215, 218, 219, 222, 223, 226, 227, 230, 231, 234, 235, 238, 239,
                            242, 243, 246, 247, 250, 251, 254, 255})], inequalities_readable)
        return

    def test_convex_hull_baksi_appendix_a(self):
        substitutions = {index: value for index, value in
                         enumerate([4, 0, 1, 3, 2, 5, 6, 7, 14, 8, 10, 9, 12, 13, 11, 15])}
        testbox = SBox(substitutions, 4, 4, None, extract_sun_inequalities=True)
        testbox.build_non_zero_ddt_entries_vectors()

        non_zero_transitions_baksi = {(12, 10), (3, 7), (5, 4), (4, 6), (5, 1), (14, 13), (9, 8), (2, 2), (11, 14),
                                      (13, 11), (11, 11), (13, 8), (7, 4), (6, 2), (7, 1), (15, 14), (4, 2), (12, 12),
                                      (5, 6), (3, 6), (5, 3), (14, 15), (8, 11), (8, 8), (2, 4), (1, 2), (2, 1),
                                      (10, 14), (11, 13), (13, 10), (6, 4), (7, 3), (3, 2), (4, 1), (12, 14), (14, 8),
                                      (5, 5), (0, 0), (9, 12), (11, 9), (8, 10), (1, 4), (2, 3), (13, 12), (15, 9),
                                      (6, 6), (7, 5), (6, 3), (15, 15), (3, 1), (12, 13), (9, 14), (10, 9), (1, 6),
                                      (2, 5), (1, 3), (10, 15), (13, 14), (15, 11), (7, 7), (6, 5), (4, 5), (3, 3),
                                      (14, 12), (8, 14), (10, 11), (11, 10), (2, 7), (13, 13), (6, 7), (7, 6), (12, 8),
                                      (3, 5), (5, 2), (4, 4), (4, 7), (14, 14), (9, 9), (1, 1), (9, 15), (8, 13),
                                      (10, 10), (1, 7), (13, 9), (13, 15), (15, 12)}
        self.assertEqual(non_zero_transitions_baksi, testbox.non_zero_ddt_entries)

        expected_convex_hull_inequalities = ['-x1>=-1', '-x4>=-1', '-x2>=-1', '-x3>=-1', '-x5>=-1', '-x6>=-1',
                                             '-x7>=-1', 'x1-2x2-x3+x4+2x5+3x6+3x7>=0', '-x1-x2-x4+x5-x6+x7>=-3',
                                             '-x1-x2-x3+x5+x7>=-2', '3x1+3x2+3x3+2x4-x5-x6-x7>=0', 'x6>=0',
                                             'x1-2x2-x3+x5+2x6+2x7>=-1', '-x1-x2+x3+x5+x6-x7>=-2',
                                             '2x1-x2+x3-2x4-x5+2x6+x7>=-2', '-x1+x2-x3+x4-x5-x6-x7>=-4',
                                             'x1+x2-x3-x4+x5-x6>=-2', 'x5>=0', 'x1-x2-x3+x4+x5+2x6+2x7>=0', 'x3>=0',
                                             'x1+x2+x3-x5-x6-x7>=-2', 'x1+x2+x3+x4-x6>=0', 'x2+x3-x4+x5+x6-x7>=-1',
                                             'x1+x2+x3-x5+x6+x7>=0', 'x1+x2+x3+x5+x6-x7>=0', 'x1+x2+x4-x5+x6-x7>=-1',
                                             'x1+x2+x3+x4-x7>=0', 'x2+x3+x4+x5-x6-x7>=-1', '-x2-x3+x5+x6+x7>=-1',
                                             '2x1+x2+2x3+2x4-x5-x6+x7>=0', 'x1>=0', '2x1+2x2+x3+2x4-x5+x6-x7>=0',
                                             'x1+2x2+2x3+2x4+x5-x6-x7>=0', 'x1+x2+x3+x4-x5>=0', 'x7>=0',
                                             '-x3+x4+x5+x6+x7>=0', 'x1+x2-x3-x5+x6-x7>=-2', 'x1-x2+x3-x4-x5+x6>=-2',
                                             '-x1+x3-x4+x5-x7>=-2', 'x1+x3+x4-x5-x6+x7>=-1', 'x1-x2-x4+x6+x7>=-1',
                                             'x1-x2-x3+x6+x7>=-1', 'x2>=0', '-x1+x2+x3-x4-x6-x7>=-3',
                                             '-x1+x2+x3+x5-x6-x7>=-2', 'x1-x2+x5+x6+x7>=0', '-x2-x3+x4+2x5+2x6+2x7>=0',
                                             '-x1-x2+x3-x4+x5-x6>=-3', '-x1-x2-x3+2x4+3x5+2x6+3x7>=0', 'x4>=0',
                                             'x2+x3-x4-x5-x6-x7>=-3', '-x1+x4+x5+x6+x7>=0',
                                             '-x1-x2+x3+2x4+2x5+2x6+x7>=0', '-x1-x2+x3+x4+x5+x6>=-1',
                                             '-x2+x4+x5+x6+x7>=0', '-2x1+x2+2x3-x4+x5-x6-2x7>=-4',
                                             'x1+x3-x4-x5+x6+x7>=-1', 'x1-x2-x3-x4-x5-x6-x7>=-5',
                                             '-x1-x2-x3-x4-x5+x6-x7>=-5']
        actual_convex_hull_inequalities = list(testbox.feasible_transition_inequalities_sun_2013).copy()
        to_be_removed = set()
        for index, inequality in enumerate(actual_convex_hull_inequalities):
            if '==' in inequality:
                to_be_removed.add(inequality)
            else:
                actual_convex_hull_inequalities[index] = inequality.replace(' ', '').replace('*', '')

        for remover in to_be_removed:
            actual_convex_hull_inequalities.remove(remover)

        expected_convex_hull_inequalities.sort()
        actual_convex_hull_inequalities.sort()

        self.assertEqual(expected_convex_hull_inequalities, actual_convex_hull_inequalities)
        return

    def test_build_list_of_transition_values_and_frequencies(self):
        # sbox from Baksi 2020 section 4.1
        # expected values are read from table 2
        substitutions = {index: value for index, value in
                         enumerate([4, 0, 1, 3, 2, 5, 6, 7, 14, 8, 10, 9, 12, 13, 11, 15])}
        testbox = SBox(substitutions, 4, 4, None, extract_sun_inequalities=True)
        testbox.build_ddt()
        testbox.build_list_of_transition_values_and_frequencies(testbox.ddt)

        expected_set_of_transition_values = {2, 4, 6, 16}
        self.assertEqual(expected_set_of_transition_values, testbox.set_of_transition_values)

        expected_value_frequencies = {16: 1, 2: 57, 4: 21, 6: 7}
        self.assertEqual(expected_value_frequencies, testbox.value_frequencies)

        expected_dict_value_to_list_of_transition = {
            2: [(1, 2), (1, 3), (1, 6), (1, 7), (2, 1), (2, 3), (2, 5), (2, 7), (3, 1), (3, 2), (3, 5), (3, 6), (4, 1),
                (4, 2), (4, 4), (4, 7), (5, 1), (5, 3), (5, 4), (5, 6), (6, 2), (6, 3), (6, 4), (6, 5), (7, 4), (7, 5),
                (7, 6), (7, 7), (8, 11), (8, 13), (8, 14), (9, 8), (9, 14), (9, 15), (10, 11), (10, 14), (10, 15),
                (11, 9), (11, 10), (11, 14), (12, 8), (12, 10), (12, 14), (13, 8), (13, 9), (13, 10), (13, 11),
                (13, 12), (13, 13), (13, 14), (13, 15), (14, 12), (14, 13), (14, 14), (15, 9), (15, 12), (15, 14)],
            4: [(1, 1), (1, 4), (2, 2), (2, 4), (3, 3), (3, 7), (4, 5), (4, 6), (5, 2), (5, 5), (6, 6), (6, 7), (7, 1),
                (7, 3), (8, 10), (9, 12), (10, 9), (11, 11), (12, 13), (14, 8), (15, 15)],
            6: [(8, 8), (9, 9), (10, 10), (11, 13), (12, 12), (14, 15), (15, 11)],
            16: [(0, 0)]}
        self.assertEqual(expected_dict_value_to_list_of_transition, testbox.dict_value_to_list_of_transition)
        return

    def test_sun_logical_condition_modeling(self):
        # using the present sbox since that one was used in Sun et al. 2013
        present_substitutions = {index: value for index, value in
                                 enumerate([12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2])}
        testbox = SBox(present_substitutions, 4, 4, None)
        testcipher = Gift64(model_as_bit_oriented=True)
        testaction = SBoxAction(sbox=testbox, input_vars=['x0', 'x1', 'x2', 'x3'], cipher_instance=testcipher,
                                first_a_position_to_overwrite=0)

        expected_logical_condition_modeling = [([1, 0, 0, 1], ['*', '*', '*', 0]), ([0, 0, 0, 1], ['*', '*', '*', 1]),
                                               ([1, 0, 0, 0], ['*', '*', '*', 1]), (['*', '*', '*', 1], [0, 0, 0, 1]),
                                               (['*', '*', '*', 1], [0, 1, 0, 0]), (['*', '*', '*', 0], [0, 1, 0, 1])]
        actual_logical_condition_modeling = testaction.sun_logical_condition_modeling()

        expected_logical_condition_modeling_sortable = [([str(c) for c in x], [str(c) for c in y]) for x, y in expected_logical_condition_modeling]
        actual_logical_condition_modeling_sortable = [([str(c) for c in x], [str(c) for c in y]) for x, y in actual_logical_condition_modeling]

        expected_logical_condition_modeling_sortable.sort()
        actual_logical_condition_modeling_sortable.sort()

        self.assertEqual(expected_logical_condition_modeling_sortable, actual_logical_condition_modeling_sortable)
        return

    def test_lat(self):
        # testing using the S-box from the example in Sofia's bachelor thesis
        test_substitutions = {index: value for index, value in
                              enumerate([2, 5, 3, 1, 7, 0, 4, 6])}

        expected_lat = [[4, 0, 0, 0, 0, 0, 0, 0],     [0, 0, -2, +2, 0, 0, -2, -2], [0, 0, 0, 0, 0, +4, 0, 0],
                        [0, 0, -2, -2, 0, 0, +2, -2], [0, -2, 0, -2, +2, 0, -2, 0], [0, +2, -2, 0, +2, 0, 0, +2],
                        [0, +2, 0, -2, -2, 0, -2, 0], [0, +2, +2, 0, +2, 0, 0, -2]]

        testbox = SBox(test_substitutions, 3, 3, None)
        testbox.build_lat()

        self.assertEqual(expected_lat, testbox.lat)
        return


if __name__ == '__main__':
    unittest.main()
