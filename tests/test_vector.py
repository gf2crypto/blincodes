"""Unit Tests for module vector."""
import unittest
from blincodes import vector


class GF2VectorTestCase(unittest.TestCase):
    """Testing Vector object."""

    def test_init_default(self):
        """Test init by default values."""
        vec = vector.Vector()
        self.assertEqual(vec.value, 0)
        self.assertEqual(len(vec), 0)
        self.assertEqual(str(vec), '')
        self.assertEqual(repr(vec), 'Vector(len=0, [])')

    def test_init_by_integer(self):
        """Test init by integer."""
        vec = vector.Vector(0b001101, 6)
        self.assertEqual(vec.value, 0b001101)
        self.assertEqual(len(vec), 6)
        self.assertEqual(str(vec), '001101')
        self.assertEqual(repr(vec), 'Vector(len=6, [001101])')

    def test_make_vector_from_iterable(self):
        """Test make vector from any iterable type."""
        vec = vector.from_iterable(
            ('*', 1, '&', 1, 1, '-', '0', '1', 1, 0, '|*1-'),
            onefillers='&|',
            zerofillers='*-')
        self.assertEqual(len(vec), 14)
        self.assertEqual(str(vec), '01111001101010')
        self.assertEqual(repr(vec), 'Vector(len=14, [01111001101010])')

    def test_make_vector_from_string(self):
        """Test make vector from string."""
        vec = vector.from_string(
            '*1&11-0110|*1-',
            onefillers='&|',
            zerofillers='*-')
        self.assertEqual(len(vec), 14)
        self.assertEqual(str(vec), '01111001101010')
        self.assertEqual(repr(vec), 'Vector(len=14, [01111001101010])')

    def test_make_vector_from_support(self):
        """Test make vector from support."""
        vec = vector.from_support(14, (1, 2, 3, 4, 7, 8, 12))
        self.assertEqual(len(vec), 14)
        self.assertEqual(str(vec), '01111001100010')
        self.assertEqual(repr(vec), 'Vector(len=14, [01111001100010])')

    def test_make_vector_from_support_supplement(self):
        """Test make vector from support supplement."""
        vec = vector.from_support_supplement(14, (0, 5, 6, 9, 10, 11, 13))
        self.assertEqual(len(vec), 14)
        self.assertEqual(str(vec), '01111001100010')
        self.assertEqual(repr(vec), 'Vector(len=14, [01111001100010])')

    def test_make_copy(self):
        """Test make copy the Vector object."""
        vec = vector.Vector(0b0111100110, 10)
        vec_copy = vec.copy()
        self.assertEqual(len(vec_copy), 10)
        self.assertEqual(str(vec_copy), '0111100110')
        self.assertEqual(repr(vec_copy), 'Vector(len=10, [0111100110])')

    def test_to_str(self):
        """Test representation as string using various fillers."""
        vec = vector.Vector(0b0111100110, 10)
        self.assertEqual(vec.to_str(zerofiller='-', onefiller='$'),
                         '-$$$$--$$-')

    def test_getitem_setitem(self):
        """Test get item and set item."""
        vec = vector.Vector(0b0111100110, 10)
        self.assertEqual(vec[2], 1)
        self.assertEqual(vec[0], 0)
        self.assertEqual(vec[-1], 0)
        self.assertEqual(vec[-8], 1)
        self.assertEqual(vec[-5], 0)
        self.assertEqual(vec[1:6:2].value, 0b110)
        vec[0] = 1
        vec[1] = 1
        vec[2] = ''
        vec[3] = '0'
        vec[4] = '1'
        vec[5] = 0
        vec[6] = False
        vec[7] = True
        vec[8] = 'UUU'
        vec[9] = -9
        self.assertEqual(vec.value, 0b1100100111)
        vec[-1] = 1
        vec[-2] = ''
        vec[-3] = '0'
        vec[-4] = '1'
        vec[-5] = 0
        vec[-6] = False
        vec[-7] = True
        vec[-8] = 'UUU'
        vec[-9] = -9
        self.assertEqual(vec.value, 0b1111001001)

    def test_eq(self):
        """Test equality of vectors."""
        vec1 = vector.Vector(0b01101, 5)
        vec2 = vector.Vector()
        vec3 = vector.Vector(0b01101, 5)
        self.assertEqual(vec1, vec3)
        self.assertEqual(vec2, vec2)
        self.assertEqual(vec1, vec1)

    def test_not_eq(self):
        """Test not equality of vectors."""
        vec1 = vector.Vector(0b01101, 5)
        vec2 = vector.Vector()
        vec3 = vector.Vector(0b01001, 5)
        self.assertNotEqual(vec1, vec3)
        self.assertNotEqual(vec1, vec2)
        self.assertNotEqual(vec1, vec3)

    def test_add(self):
        """Test v1 + v2."""
        vec1 = vector.Vector(0b01101, 5)
        vec2 = vector.Vector()
        vec3 = vector.Vector(0b00101, 5)
        summ = vector.Vector(0b01000, 5)
        self.assertEqual(vec1 + vec3, summ)
        self.assertEqual(vec1 + vec2, vec1)
        vec1 += vec3
        self.assertEqual(vec1, summ)

    def test_mul(self):
        """Test v1 * v2."""
        vec1 = vector.Vector(0b01101, 5)
        vec2 = vector.Vector()
        vec3 = vector.Vector(0b00101, 5)
        zero = vector.Vector(0, 5)
        mul = vector.Vector(0b00101, 5)
        self.assertEqual(vec1 * vec3, mul)
        self.assertEqual(vec1 * vec2, zero)
        vec1 *= vec3
        self.assertEqual(vec1, mul)

    def test_xor(self):
        """Test v1 ^ v2."""
        vec1 = vector.Vector(0b01101, 5)
        vec2 = vector.Vector()
        vec3 = vector.Vector(0b00101, 5)
        summ = vector.Vector(0b01000, 5)
        self.assertEqual(vec1 ^ vec3, summ)
        self.assertEqual(vec1 ^ vec2, vec1)
        vec1 ^= vec3
        self.assertEqual(vec1, summ)

    def test_and(self):
        """Test v1 & v2."""
        vec1 = vector.Vector(0b01101, 5)
        vec2 = vector.Vector()
        vec3 = vector.Vector(0b00101, 5)
        zero = vector.Vector(0, 5)
        mul = vector.Vector(0b00101, 5)
        self.assertEqual(vec1 & vec3, mul)
        self.assertEqual(vec1 & vec2, zero)
        vec1 &= vec3
        self.assertEqual(vec1, mul)

    def test_or(self):
        """Test v1 | v2."""
        vec1 = vector.Vector(0b01101, 5)
        vec2 = vector.Vector()
        vec3 = vector.Vector(0b00101, 5)
        vec_or = vector.Vector(0b01101, 5)
        self.assertEqual(vec1 | vec3, vec_or)
        self.assertEqual(vec1 | vec2, vec1)
        vec1 |= vec3
        self.assertEqual(vec1, vec_or)

    def test_bitwise_not(self):
        """Test ~v."""
        vec1 = vector.Vector(0b01101, 5)
        vec2 = vector.Vector()
        vec3 = vector.Vector(0b00000, 5)
        self.assertEqual(vec1.bitwise_not().value, 0b10010)
        self.assertEqual(vec2.bitwise_not().value, 0)
        self.assertEqual(vec3.bitwise_not().value, 0b11111)
        self.assertEqual(vector.bitwise_not(vec1).value, 0b01101)
        self.assertEqual(vector.bitwise_not(vec2).value, 0)
        self.assertEqual(vector.bitwise_not(vec3).value, 0)

    def test_set_size_and_resize(self):
        """Test resizing of vector."""
        vec1 = vector.Vector(0b10011, 5)
        vec2 = vector.Vector(0b011, 3)
        vec3 = vector.Vector(0b0010011, 7)
        self.assertEqual(vec2, vec1.copy().set_length(3))
        self.assertEqual(vec3, vec1.copy().set_length(7))
        self.assertEqual(vec2, vec1.copy().resize(-2))
        self.assertEqual(vec3, vec1.copy().resize(2))

    def test_shifting(self):
        """Test vector shift operators."""
        vec1 = vector.Vector(0b10011, 5)
        vec2 = vector.Vector(0b01100, 5)
        vec3 = vector.Vector(0b00100, 5)
        vec4 = vector.Vector(0b00001, 5)
        vec_empty = vector.Vector()
        self.assertEqual(vec2, vec1 << 2)
        self.assertEqual(vec3, vec1 >> 2)
        vec1 <<= 2
        self.assertEqual(vec2, vec1)
        vec1 >>= 3
        self.assertEqual(vec4, vec1)
        self.assertEqual(vec_empty, vec_empty << 10)
        self.assertEqual(vec_empty, vec_empty >> 10)

    def test_hamming_weight(self):
        """Test evaluation ot Hamming weight."""
        vec1 = vector.Vector(0b10011, 5)
        vec2 = vector.Vector(0b01100, 5)
        vec3 = vector.Vector(0b00100, 5)
        vec4 = vector.Vector(0b00000, 5)
        vec5 = vector.Vector()
        self.assertEqual(vec1.hamming_weight, 3)
        self.assertEqual(vec2.hamming_weight, 2)
        self.assertEqual(vec3.hamming_weight, 1)
        self.assertEqual(vec4.hamming_weight, 0)
        self.assertEqual(vec5.hamming_weight, 0)
        self.assertEqual(vector.hamming_distance(vec1, vec2), 5)
        self.assertEqual(vector.hamming_distance(vec1, vec3), 4)
        self.assertEqual(vector.hamming_distance(vec3, vec4), 1)
        self.assertEqual(vector.hamming_distance(vec2, vec3), 1)
        self.assertEqual(vector.hamming_distance(vec2, vec5), 2)

    def test_support(self):
        """Test evaluation ot vector's support."""
        vec1 = vector.Vector(0b10011, 5)
        vec2 = vector.Vector(0b01100, 5)
        vec3 = vector.Vector(0b00100, 5)
        vec4 = vector.Vector(0b00000, 5)
        vec5 = vector.Vector()
        self.assertEqual(vec1.support, [0, 3, 4])
        self.assertEqual(vec2.support, [1, 2])
        self.assertEqual(vec3.support, [2])
        self.assertEqual(vec4.support, [])
        self.assertEqual(vec5.support, [])
        self.assertEqual(list(vec1.iter_support()), [0, 3, 4])
        self.assertEqual(list(vec2.iter_support()), [1, 2])
        self.assertEqual(list(vec3.iter_support()), [2])
        self.assertEqual(list(vec4.iter_support()), [])
        self.assertEqual(list(vec5.iter_support()), [])
        self.assertEqual(vec1.support_supplement, [1, 2])
        self.assertEqual(vec2.support_supplement, [0, 3, 4])
        self.assertEqual(vec3.support_supplement, [0, 1, 3, 4])
        self.assertEqual(vec4.support_supplement, [0, 1, 2, 3, 4])
        self.assertEqual(vec5.support_supplement, [])
        self.assertEqual(list(vec1.iter_support_supplement()), [1, 2])
        self.assertEqual(list(vec2.iter_support_supplement()), [0, 3, 4])
        self.assertEqual(list(vec3.iter_support_supplement()), [0, 1, 3, 4])
        self.assertEqual(list(vec4.iter_support_supplement()), [0, 1, 2, 3, 4])
        self.assertEqual(list(vec5.iter_support_supplement()), [])

    def test_bool(self):
        """Test comparison with None."""
        vec1 = vector.Vector(0b10011, 5)
        vec2 = vector.Vector(0b00000, 5)
        vec3 = vector.Vector()
        self.assertTrue(vec1)
        self.assertTrue(vec2)
        self.assertFalse(vec3)

    def test_concatenate(self):
        """Test concatination of vectors."""
        vec1 = vector.Vector(0b10011, 5)
        vec2 = vector.Vector(0b00000, 5)
        vec3 = vector.Vector()
        self.assertEqual(vec1.concatenate(vec2).value, 0b1001100000)
        self.assertEqual(vec1.concatenate(vec3).value, 0b1001100000)
        self.assertEqual(vector.concatenate(vec1, vec1).value,
                         0b10011000001001100000)
        self.assertEqual(vector.concatenate(vec3, vec1).value, 0b1001100000)

    def test_scalar_product(self):
        """Test scalar product of vectors."""
        vec1 = vector.Vector(0b10011, 5)
        vec2 = vector.Vector(0b00000, 5)
        vec3 = vector.Vector()
        vec4 = vector.Vector(0b00011, 5)
        self.assertEqual(vector.scalar_product(vec1, vec1), 1)
        self.assertEqual(vector.scalar_product(vec1, vec2), 0)
        self.assertEqual(vector.scalar_product(vec1, vec4), 0)
        self.assertEqual(vector.scalar_product(vec1, vec3), 0)
        self.assertEqual(vector.scalar_product(vec3, vec3), 0)
        self.assertEqual(vector.scalar_product(vec4, vec3), 0)

    def test_to_latex_str(self):
        """Test function to_latex_str()."""
        vec1 = vector.Vector(0b01101, 5)
        vec2 = vector.Vector()
        self.assertEqual(vec1.to_latex_str(), '0&1&1&0&1')
        self.assertEqual(vec2.to_latex_str(), '')


if __name__ == "__main__":
    unittest.main()
