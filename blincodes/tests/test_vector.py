"""
    Unit Tests for module lincodes.gf2.vector
"""
import unittest
import sys
sys.path.append("../")
from lincodes import gf2


class GF2VectorTestCase(unittest.TestCase):
    """
        Testing Vector object
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

    # @unittest.skip
    def test_make_copy(self):
        """
            Test copying the Vector
        """
        vector = gf2.vector.Vector(['*1111**11*'])
        vec_copy = gf2.vector.Vector(vector.value, len(vector))
        self.assertEqual(len(vector), 10)
        self.assertEqual(str(vec_copy), '*1111**11*')
        self.assertEqual(repr(vec_copy), 'gf2.vector(len=10, [*1111**11*])')

    # @unittest.skip
    def test_changing_fillers(self):
        """
            Test changing the fillers
        """
        vector = gf2.vector.Vector(['*1111**11*'])
        vector.onefiller = '$'
        vector.zerofiller = '-'
        self.assertEqual(str(vector), '-$$$$--$$-')
        self.assertEqual(repr(vector), 'gf2.vector(len=10, [-$$$$--$$-])')

        gf2.vector.Vector.onefillers.append('$')
        gf2.vector.Vector.zerofillers.append('|')
        vector = gf2.vector.Vector(['|$$$$||$$|'])

        self.assertEqual(str(vector), '*1111**11*')
        self.assertEqual(repr(vector), 'gf2.vector(len=10, [*1111**11*])')

    # @unittest.skip
    def test_getitem_setitem(self):
        """
            Test get item and set item
        """
        vector = gf2.vector.Vector(['*1111**111'])
        self.assertEqual(vector[2], 1)
        self.assertEqual(vector[0], 0)
        self.assertEqual(vector[-1], 1)
        self.assertEqual(vector[-8], 1)
        self.assertEqual(vector[-5], 0)
        vector[0] = 1
        vector[1] = 1
        vector[2] = ''
        vector[3] = '0'
        vector[4] = '1'
        vector[5] = 0
        vector[6] = False
        vector[7] = True
        vector[8] = 'UUU'
        vector[9] = -9
        self.assertEqual(str(vector), '11**1**111')
        self.assertEqual(repr(vector), 'gf2.vector(len=10, [11**1**111])')
        vector[-1] = 1
        vector[-2] = ''
        vector[-3] = '0'
        vector[-4] = '1'
        vector[-5] = 0
        vector[-6] = False
        vector[-7] = True
        vector[-8] = 'UUU'
        vector[-9] = -9
        self.assertEqual(str(vector), '1111**1**1')
        self.assertEqual(repr(vector), 'gf2.vector(len=10, [1111**1**1])')

    # @unittest.skip
    def test_eq(self):
        """
            Test equality of vectors
        """
        vec1 = gf2.vector.Vector([0, 1, 1, 0, 1])
        vec2 = gf2.vector.Vector()
        vec3 = gf2.vector.Vector([0, 1, 1, 0, 1])
        self.assertEqual(vec1, vec3)
        self.assertEqual(vec2, vec2)
        self.assertEqual(vec1, vec1)

    # @unittest.skip
    def test_not_eq(self):
        """
            Test not equality of vectors
        """
        vec1 = gf2.vector.Vector([0, 1, 1, 0, 1])
        vec2 = gf2.vector.Vector()
        vec3 = gf2.vector.Vector([0, 0, 1, 0, 1])
        self.assertNotEqual(vec1, vec3)
        self.assertNotEqual(vec1, vec2)
        self.assertNotEqual(vec1, vec3)

    # @unittest.skip
    def test_add(self):
        """
            Test v1 + v2
        """
        vec1 = gf2.vector.Vector([0, 1, 1, 0, 1])
        vec2 = gf2.vector.Vector()
        vec3 = gf2.vector.Vector([0, 0, 1, 0, 1])
        summ = gf2.vector.Vector([0, 1, 0, 0, 0])
        self.assertEqual(vec1 + vec3, summ)
        self.assertEqual(vec1 + vec2, vec1)
        vec1 += vec3
        self.assertEqual(vec1, summ)

    # @unittest.skip
    def test_mul(self):
        """
            Test v1 * v2
        """
        vec1 = gf2.vector.Vector([0, 1, 1, 0, 1])
        vec2 = gf2.vector.Vector()
        vec3 = gf2.vector.Vector([0, 0, 1, 0, 1])
        zero = gf2.vector.Vector(size=5)
        mul = gf2.vector.Vector([0, 0, 1, 0, 1])
        self.assertEqual(vec1 * vec3, mul)
        self.assertEqual(vec1 * vec2, zero)
        vec1 *= vec3
        self.assertEqual(vec1, mul)

    # @unittest.skip
    def test_set_size_and_resize(self):
        """
            Test resizing of vector
        """
        vec1 = gf2.vector.Vector([1, 0, 0, 1, 1])
        vec2 = gf2.vector.Vector([0, 1, 1])
        vec3 = gf2.vector.Vector([0, 0, 1, 0, 0, 1, 1])
        vec4 = gf2.vector.Vector([1, 0, 0])
        vec5 = gf2.vector.Vector([1, 0, 0, 1, 1, 0, 0])
        self.assertEqual(vec2, vec1.copy().set_size(3, False))
        self.assertEqual(vec3, vec1.copy().set_size(7, False))
        self.assertEqual(vec4, vec1.copy().set_size(3, True))
        self.assertEqual(vec5, vec1.copy().set_size(7, True))
        self.assertEqual(vec2, vec1.copy().resize(-2, False))
        self.assertEqual(vec3, vec1.copy().resize(2, False))
        self.assertEqual(vec4, vec1.copy().resize(-2, True))
        self.assertEqual(vec5, vec1.copy().resize(2, True))

    # @unittest.skip
    def test_shifting(self):
        """
            Test vector shift operators
        """
        vec1 = gf2.vector.Vector([1, 0, 0, 1, 1])
        vec2 = gf2.vector.Vector([0, 1, 1, 0, 0])
        vec3 = gf2.vector.Vector([0, 0, 1, 0, 0])
        vec4 = gf2.vector.Vector([0, 0, 0, 0, 1])
        vec_empty = gf2.vector.Vector()
        self.assertEqual(vec2, vec1 << 2)
        self.assertEqual(vec3, vec1 >> 2)
        vec1 <<= 2
        self.assertEqual(vec2, vec1)
        vec1 >>= 3
        self.assertEqual(vec4, vec1)
        self.assertEqual(vec_empty, vec_empty << 10)
        self.assertEqual(vec_empty, vec_empty >> 10)

    # @unittest.skip
    def test_to_latex_str(self):
        """
            Test v.to_latex_str()
        """
        vec1 = gf2.vector.Vector([0, 1, 1, 0, 1])
        vec2 = gf2.vector.Vector()
        self.assertEqual(vec1.to_latex_str(), '0&1&1&0&1')
        self.assertEqual(vec2.to_latex_str(), '')


if __name__ == "__main__":
    unittest.main()