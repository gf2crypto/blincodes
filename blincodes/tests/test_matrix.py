import unittest
import sys
sys.path.append("../")
from lincodes import gf2


class GF2MatrixTestCase(unittest.TestCase):
    """
        Testing matrix usage
    """

    def test_init_default(self):
        """
            Init by default values
        """
        vector = gf2.vector.Vector()
        self.assertEqual(len(vector), 0)
        self.assertEqual(str(vector), '')
        self.assertEqual(repr(vector), 'gf2.vector(len=0, [])')

    def test_init_by_integer(self):
        """
            Init by integer
        """
        vector = gf2.vector.Vector(size=10)
        self.assertEqual(len(vector), 10)
        self.assertEqual(str(vector), '**********')
        self.assertEqual(repr(vector), 'gf2.vector(len=10, [**********])')

    def test_init_by_iterable(self):
        """
            Init by any iterable type
        """
        vector = gf2.vector.Vector(
            ('*', 1, '1', 1, 1, '-', '0', '1', 1, 0, '0*1-'))
        self.assertEqual(len(vector), 14)
        self.assertEqual(str(vector), '*1111**11***1*')
        self.assertEqual(repr(vector), 'gf2.vector(len=14, [*1111**11***1*])')

#     def test_init_by_negative(self):
#         """
#             Init matrix by negative dimensions
#         """
#         matrix = BitMatrix(-2, -1)
#         self.assertEqual(matrix.nrows, 0)
#         self.assertEqual(matrix.ncolumns, 0)
#         matrix = BitMatrix(2, -1)
#         self.assertEqual(matrix.nrows, 0)
#         self.assertEqual(matrix.ncolumns, 0)
#         matrix = BitMatrix(-2, 2)
#         self.assertEqual(matrix.nrows, 0)
#         self.assertEqual(matrix.ncolumns, 0)


# class RepresentTestCase(unittest.TestCase):
#     """
#         Testing representation of matrix
#     """

#     def test_represent_default(self):
#         """
#             Represent default matrix
#         """
#         matrix = BitMatrix()
#         rep = ("(0x0)")
#         self.assertEqual(str(matrix), rep)

#     def test_represent(self):
#         """
#             Testing representation of typical matrix
#         """
#         matrix = BitMatrix(3, 10)
#         rep = ("**********\n"
#                "**********\n"
#                "**********\n"
#                "(3x10)")
#         self.assertEqual(str(matrix), rep)


# class InitByStringTestCase(unittest.TestCase):
#     """
#         Testing init matrix from string
#     """

#     def test_init_from_string(self):
#         """
#             Init from string
#         """
#         matrix = BitMatrix(
#             "1 1 1 1 1 1 1 1;"
#             "* * * * 1 1 1 1;"
#             "- -110011;"
#             "0 1 0 1 0 1 0 1;"
#             "11-*;"
#             )
#         rep = ("11111111\n"
#                "****1111\n"
#                "**11**11\n"
#                "*1*1*1*1\n"
#                "****11**\n"
#                "********\n"
#                "(6x8)")
#         self.assertEqual(str(matrix), rep)

#     def test_init_from_string_resize(self):
#         """
#             Init from string and resize
#         """
#         matrix = BitMatrix(
#             "1 1 1 1 1 1 1 1;"
#             "* * * * 1 1 1 1;"
#             "- -110011;"
#             "0 1 0 1 0 1 0 1;"
#             "11-*;",
#             10
#             )
#         rep = ("**11111111\n"
#                "******1111\n"
#                "****11**11\n"
#                "***1*1*1*1\n"
#                "******11**\n"
#                "**********\n"
#                "(6x10)")
#         self.assertEqual(str(matrix), rep)


# class InitByListTestCase(unittest.TestCase):
#     """
#         Testing init matrix from list
#     """

#     def test_init_from_string(self):
#         """
#             Init from list
#         """
#         matrix = BitMatrix([
#             0b11111111,
#             "* * * * 1 1 1 1",
#             "- -110011",
#             "0 1 0 1 0 1 0 1",
#             0b00001100,
#             0
#             ])
#         rep = ("11111111\n"
#                "****1111\n"
#                "**11**11\n"
#                "*1*1*1*1\n"
#                "****11**\n"
#                "********\n"
#                "(6x8)")
#         self.assertEqual(str(matrix), rep)

#     def test_init_from_list_resize(self):
#         """
#             Init from list and resize
#         """
#         matrix = BitMatrix([
#             0b11111111,
#             "* * * * 1 1 1 1",
#             "- -110011",
#             "0 1 0 1 0 1 0 1",
#             0b00001100,
#             0
#             ], 10)
#         rep = ("**11111111\n"
#                "******1111\n"
#                "****11**11\n"
#                "***1*1*1*1\n"
#                "******11**\n"
#                "**********\n"
#                "(6x10)")
#         self.assertEqual(str(matrix), rep)


# class SetitemTestCase(unittest.TestCase):

#     def test_setitem(self):
#         m = BitMatrix(4, 8)
#         m[0] = "11111111"
#         m[1] = "00001111"
#         m[2] = "**11**11"
#         m[3] = 0b01010101
#         rep = ("11111111\n"
#                "****1111\n"
#                "**11**11\n"
#                "*1*1*1*1\n"
#                "(4x8)")
#         self.assertEqual(str(m), rep)

#     def test_setitem_negative_index(self):
#         m = BitMatrix(2, 6)
#         m[0] = "110011"
#         m[-1] = "010101"
#         rep = ("11**11\n"
#                "*1*1*1\n"
#                "(2x6)")
#         self.assertEqual(str(m), rep)

#     def test_setitem_short(self):
#         m = BitMatrix(1, 8)
#         m[0] = "**11"
#         rep = "******11\n(1x8)"
#         self.assertEqual(str(m), rep)

#     def test_setitem_wide(self):
#         m = BitMatrix(1, 8)
#         self.assertRaises(ValueError, m.__setitem__,
#                           0, "**11**11**")
#         self.assertRaises(ValueError, m.__setitem__,
#                           0, 0b100110011)

#     def test_setitem_index_error(self):
#         m = BitMatrix(3, 5)
#         self.assertRaises(IndexError, m.__setitem__, 3, 0b11)
#         self.assertRaises(TypeError, m.__setitem__, "1", 0b11)


# class ChangeFillersTestCase(unittest.TestCase):
#     def setUp(self):
#         self.bm = BitMatrix(4, 8)
#         self.bm[0] = "11111111"
#         self.bm[1] = "****1111"
#         self.bm[2] = "**11**11"
#         self.bm[3] = "*1*1*1*1"
#         self.rep = ("11111111\n"
#                     "****1111\n"
#                     "**11**11\n"
#                     "*1*1*1*1\n"
#                     "(4x8)")

#     def test_change_zero_filler(self):
#         self.bm.zerofiller = "-"
#         self.assertEqual(str(self.bm), self.rep.replace("*", "-"))

#     def test_change_ones_filler(self):
#         self.bm.onefiller = "-"
#         self.assertEqual(str(self.bm), self.rep.replace("1", "-"))

#     def test_incorrect_fillers(self):
#         self.assertRaises(TypeError, self.bm.__setattr__,
#                           "onefiller", 1)
#         self.assertRaises(TypeError, self.bm.__setattr__,
#                           "zerofiller", 1)
#         self.assertRaises(ValueError, self.bm.__setattr__,
#                           "onefiller", "12")
#         self.assertRaises(ValueError, self.bm.__setattr__,
#                           "zerofiller", "12")
#         self.assertRaises(ValueError, self.bm.__setattr__,
#                           "onefiller", "")
#         self.assertRaises(ValueError, self.bm.__setattr__,
#                           "zerofiller", "")


# class ResizeDimensionsTestCase(unittest.TestCase):
#     def test_resize_rows(self):
#         m = BitMatrix(2, 5)
#         m.nrows = 5
#         rep = ("*****\n"
#                "*****\n"
#                "*****\n"
#                "*****\n"
#                "*****\n"
#                "(5x5)")
#         self.assertEqual(str(m), rep)

#     def test_resize_rows_to_zero(self):
#         m = BitMatrix(2, 5)
#         m.nrows = 0
#         rep = ("(0x0)")
#         self.assertEqual(str(m), rep)

#     def test_resize_rows_exceptions(self):
#         m = BitMatrix()
#         self.assertRaises(TypeError, m.__setattr__, "nrows", "1")
#         self.assertRaises(TypeError, m.__setattr__, "nrows", [])
#         self.assertRaises(TypeError, m.__setattr__, "nrows", ())
#         self.assertRaises(TypeError, m.__setattr__, "nrows", 12.1)
#         self.assertRaises(ValueError, m.__setattr__, "nrows", -1)

#     def test_resize_columns(self):
#         m = BitMatrix(5, 1)
#         m.ncolumns = 5
#         rep = ("*****\n"
#                "*****\n"
#                "*****\n"
#                "*****\n"
#                "*****\n"
#                "(5x5)")
#         self.assertEqual(str(m), rep)

#     def test_resize_columns_to_zero(self):
#         m = BitMatrix(2, 5)
#         m.ncolumns = 0
#         rep = ("(0x0)")
#         self.assertEqual(str(m), rep)

#     def test_resize_columns_exceptions(self):
#         m = BitMatrix()
#         self.assertRaises(TypeError, m.__setattr__, "ncolumns", "1")
#         self.assertRaises(TypeError, m.__setattr__, "ncolumns", [])
#         self.assertRaises(TypeError, m.__setattr__, "ncolumns", ())
#         self.assertRaises(TypeError, m.__setattr__, "ncolumns", 12.1)
#         self.assertRaises(ValueError, m.__setattr__, "ncolumns", -1)


# class RankTestCase(unittest.TestCase):
#     def test_default_matrix(self):
#         m = BitMatrix()
#         self.assertEqual(m.rank(), 0)

#     def test_zero_matrix(self):
#         m = BitMatrix(20, 20)
#         self.assertEqual(m.rank(), 0)

#     def test_diagonal_matrix(self):
#         m = BitMatrix(10, 10)
#         m[0] = "1111111111"
#         m[1] = "0111111111"
#         m[2] = "0011111111"
#         m[3] = "0001111111"
#         m[4] = "0000111111"
#         m[5] = "0000011111"
#         m[6] = "0000001111"
#         m[7] = "0000000111"
#         m[8] = "0000000011"
#         m[9] = "0000000001"
#         self.assertEqual(m.rank(), 10)

#     def test_square_matrix(self):
#         m = BitMatrix(10, 10)
#         m[0] = "1111111111"
#         m[1] = "0111111111"
#         m[2] = "1011111111"
#         m[3] = "0101111111"
#         m[4] = "1010111111"
#         m[5] = "0101011111"
#         m[6] = "0010101111"
#         m[7] = "0101010111"
#         m[8] = "0000101011"
#         m[9] = "0100010101"
#         self.assertEqual(m.rank(), 10)

#     def test_rm_matrix(self):
#         m = BitMatrix(4, 8)
#         m[0] = "11111111"
#         m[1] = "00001111"
#         m[2] = "00110011"
#         m[3] = "01010101"
#         self.assertEqual(m.rank(), 4)

#     def test_many_rows_matrix(self):
#         m = BitMatrix(8, 4)
#         m[0] = "1111"
#         m[1] = "1110"
#         m[2] = "1101"
#         m[3] = "1100"
#         m[4] = "1111"
#         m[5] = "1010"
#         m[6] = "1001"
#         m[7] = "1000"
#         self.assertEqual(m.rank(), 4)


# class TransposeTestCase(unittest.TestCase):
#     def test_default(self):
#         m = BitMatrix()
#         t = m.T
#         self.assertTrue(isinstance(t, BitMatrix))
#         self.assertEqual(str(t), "(0x0)")

#     def test_zero_columns(self):
#         m = BitMatrix(5, 0)
#         t = m.T
#         self.assertEqual(str(t), "(0x0)")

#     def test_zero_rows(self):
#         m = BitMatrix(0, 5)
#         t = m.T
#         self.assertEqual(str(t), "(0x0)")

#     def test_rm_matrix(self):
#         m = BitMatrix(4, 8)
#         m[0] = "11111111"
#         m[1] = "00001111"
#         m[2] = "00110011"
#         m[3] = "01010101"
#         rep_t = ("1***\n"
#                  "1**1\n"
#                  "1*1*\n"
#                  "1*11\n"
#                  "11**\n"
#                  "11*1\n"
#                  "111*\n"
#                  "1111\n"
#                  "(8x4)")
#         rep = ("11111111\n"
#                "****1111\n"
#                "**11**11\n"
#                "*1*1*1*1\n"
#                "(4x8)")
#         t = m.T
#         self.assertEqual(str(t), rep_t)
#         m = t.T
#         self.assertEqual(str(m), rep)


# class ComparisonTestCase(unittest.TestCase):
#     def test_compare_default(self):
#         m1 = BitMatrix()
#         m2 = BitMatrix()
#         self.assertEqual(m1, m2)

#     def test_compare(self):
#         m1 = BitMatrix(4, 8)
#         m1[0] = "11111111"
#         m1[1] = "00001111"
#         m1[2] = "00110011"
#         m1[3] = "01010101"
#         m2 = BitMatrix(4, 8)
#         m2[0] = "11111111"
#         m2[1] = "00001111"
#         m2[2] = "00110011"
#         m2[3] = "01010101"
#         m3 = BitMatrix(4, 8)
#         m3[0] = "11111111"
#         m3[1] = "10001111"
#         m3[2] = "00110011"
#         m3[3] = "01010101"
#         self.assertEqual(m1, m2)
#         self.assertNotEqual(m1, m3)

#     def test_compare_with_zero(self):
#         m1 = BitMatrix(5, 10)
#         self.assertEqual(m1, 0)
#         m2 = BitMatrix()
#         self.assertEqual(m2, 0)
#         m3 = BitMatrix(5, 10)
#         self.assertEqual(m1, m3)


# class SumTestCase(unittest.TestCase):
#     """
#         Testing sum of two matricies
#     """
#     def test_sum_defaults(self):
#         """
#             Test sum of defaults matricies
#         """
#         mat1 = BitMatrix()
#         mat2 = BitMatrix()
#         mat_sum = mat1 + mat2
#         self.assertEqual("(0x0)", str(mat_sum))

#     def test_sum(self):
#         """
#             Test sum of matricies
#         """
#         mat1 = BitMatrix(
#             "11111111;"
#             "----1111;"
#             "--11--11;"
#             "-1-1-1-1"
#             )
#         mat2 = BitMatrix(
#             "11111111;"
#             "----1111;"
#             "--11--11;"
#             "-1-1-1-1"
#             )
#         mat_sum = mat1 + mat2 + mat1
#         self.assertEqual(str(mat2), str(mat_sum))

#     def test_sum_wrong_dimensions(self):
#         """
#             Test raise exceptions if dimensions of matricies are different
#         """
#         mat1 = BitMatrix(3, 10)
#         mat2 = BitMatrix(3, 11)
#         mat3 = BitMatrix(4, 10)
#         mat4 = BitMatrix(4, 11)
#         self.assertRaises(ValueError, mat1.__add__, mat2)
#         self.assertRaises(ValueError, mat1.__add__, mat3)
#         self.assertRaises(ValueError, mat1.__add__, mat4)


if __name__ == "__main__":
    unittest.main()