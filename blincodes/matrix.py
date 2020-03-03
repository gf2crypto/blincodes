"""Module for working with matricies over GF(2) field."""

import math
import vector


class Matrix():
    """Binary matrix abstraction."""

    def __init__(self, value=None, ncolumns=0):
        """Create new matrix.

        :param: value - any iterable of integers
        :param: ncolumns - number of columns in the matrix
        """
        if not isinstance(ncolumns, int):
            raise TypeError(
                'expected `ncolumns` is integer, but '
                'got {}'.format(type(ncolumns)))
        if ncolumns < 0:
            raise ValueError(
                'expected `ncolumns` is not less then 0, but '
                '{} < 0'.format(ncolumns))
        self._ncolumns = ncolumns
        if not value:
            value = []
        if self._ncolumns:
            self._matrix = tuple(vector.Vector(i, ncolumns) for i in value)
        else:
            self._matrix = tuple()

    @property
    def nrows(self):
        """Return number of rows."""
        return len(self._matrix)

    @property
    def ncolumns(self):
        """Return number of columns."""
        return self._ncolumns

    @property
    def shapes(self):
        """Return shapes of the matrix: (nrows, ncolumns)."""
        return self.nrows, self.ncolumns

    def to_str(self, zerofillers=None, onefillers=None, numbered=False):
        """Return string representation of matrix."""
        matrix_str = ''
        if self._matrix:
            number_formated = '{{: >{}}}: '.format(
                int(math.log10(self.nrows)) + 1)
            for i, vec in enumerate(self._matrix):
                if numbered:
                    matrix_str += number_formated.format(i)
                matrix_str += vec.to_str(zerofillers, onefillers)
                matrix_str += '\n'
        return matrix_str[:-1]

    def __iter__(self):
        """Iterate over rows of matrix."""
        for vec in self._matrix:
            yield vec

    def __getitem__(self, index):
        """Return row of matrix with index `index`.

        If index is integer then it returns the row with index `index`.
        If index is slice the it returns the Matrix object.
        """
        if isinstance(index, int):
            return self._matrix[index]
        try:
            submatrix = tuple(self._matrix[i].value
                              for i in range(*index.indices(self.nrows)))
        except TypeError:
            raise TypeError(
                'expected `index` is integer or slice not'
                ' {}'.format(type(index)))
        return self.__class__(submatrix, self._ncolumns)

    def __repr__(self):
        """Return string representation of matrix to use in terminal."""
        rep = '{name}(shapes={shapes}, [{{matrix}}])'.format(
            name=self.__class__.__name__,
            shapes=self.shapes
            )
        if not self._matrix:
            return rep.format(matrix='')
        matrix = ''
        if self.nrows <= 3:
            for i, vec in enumerate(self._matrix):
                str_vec = str(vec)
                if len(str_vec) > 8:
                    str_vec = '{first4}...{last4}'.format(
                        first4=str_vec[:4], last4=str_vec[-4:])
                matrix += '{}: {}, '.format(str(i), str_vec)
        else:
            for i, vec in [(0, self._matrix[0]),
                           (1, self._matrix[1]),
                           (self.nrows - 1, self._matrix[-1])]:
                str_vec = str(vec)
                if len(str_vec) > 8:
                    str_vec = '{first4}...{last4}'.format(
                        first4=str_vec[:4], last4=str_vec[-4:])
                if i == 1:
                    matrix += '{}: {},..., '.format(str(i), str_vec)
                else:
                    matrix += '{}: {}, '.format(str(i), str_vec)
        return rep.format(matrix=matrix[:-2])

    def __str__(self):
        """Return string representation of Matrix to print it."""
        return self.to_str()

    def __setitem__(self, index, row):
        """Set the row with index `index` by new `row`."""
        if not isinstance(index, int):
            raise TypeError(
                'excepted `indes` is integer, but got {} '
                ''.format(type(index)))
        if abs(index) >= self.nrows:
            raise IndexError(
                'assignment index out of range,'
                ' expected |index| < {}'.format(self.nrows))
        index = index % self.nrows
        self._matrix = (self._matrix[:index] +
                        (self.__make_row_from_value(row), ) +
                        self._matrix[index + 1:])

    def __eq__(self, other):
        """Return True if self == other."""
        try:
            if self.nrows != other.nrows:
                return False
            for row1, row2 in zip(self, other):
                if row1 != row2:
                    return False
        except (AttributeError, TypeError):
            return False
        return True

    def __ne__(self, other):
        """Return False if self == other."""
        return not self == other

    def __imul__(self, other):
        """Multiply of two matricies.

        self *= other and return self.
        """
        if self.ncolumns != other.nrows:
            raise ValueError(
                'wrong shapes of matricies: the number of '
                'columns of the first matrix must be equal the '
                'number of rows of other matrix, '
                'but {} != {}'.format(self.ncolumns, other.nrows))
        result = []
        for row in self:
            sum_row = vector.Vector(0, other.ncolumns)
            for vec in (other_row for i, other_row in enumerate(other)
                        if row[i]):
                sum_row += vec
            result.append(sum_row)
        self._matrix = tuple(result)
        self._ncolumns = other.ncolumns
        return self

    def __mul__(self, other):
        """Multiply of two matricies.

        return self * other
        """
        if self.ncolumns != other.nrows:
            raise ValueError(
                'wrong shapes of matricies: the number of '
                'columns of the first matrix must be equal the '
                'number of rows of other matrix, '
                'but {} != {}'.format(self.ncolumns, other.nrows))
        result = []
        for row in self:
            sum_row = vector.Vector(0, other.ncolumns)
            for vec in (other_row for i, other_row in enumerate(other)
                        if row[i]):
                sum_row += vec
            result.append(sum_row.value)
        return self.__class__(result, other.ncolumns)

    def __iadd__(self, other):
        """Sum of two matricies.

        self += other and return self.
        """
        result = []
        for row1, row2 in zip(self, other):
            result.append(row1 + row2)
        self._matrix = tuple(result)
        self._ncolumns = max(self.ncolumns, other.ncolumns)
        return self

    def __add__(self, other):
        """Sum of two matricies.

        return self + other
        """
        return self.__class__(
            tuple((row1 + row2).value for row1, row2 in zip(self, other)),
            max(self.ncolumns, other.ncolumns))

    def __ixor__(self, other):
        """Evaluate XOR of two matricies.

        self ^= other and return self.
        """
        self += other
        return self

    def __xor__(self, other):
        """Evaluate XOR of two matricies.

        return self ^ other
        """
        return self + other

    def __ior__(self, other):
        """Evaluate OR of two matricies.

        self |= other and return self.
        """
        result = []
        for row1, row2 in zip(self, other):
            result.append(row1 ^ row2)
        self._matrix = tuple(result)
        self._ncolumns = max(self.ncolumns, other.ncolumns)
        return self

    def __or__(self, other):
        """Evaluate OR of two matricies.

        return self ^ other
        """
        return self.__class__(
            tuple((row1 ^ row2).value for row1, row2 in zip(self, other)),
            max(self.ncolumns, other.ncolumns))

    def __iand__(self, other):
        """Evaluate AND of two matricies.

        self &= other and return self.
        """
        result = []
        for row1, row2 in zip(self, other):
            result.append(row1 & row2)
        self._matrix = tuple(result)
        self._ncolumns = max(self.ncolumns, other.ncolumns)
        return self

    def __and__(self, other):
        """Evaluate AND of two matricies.

        return self & other
        """
        return self.__class__(
            tuple((row1 & row2).value for row1, row2 in zip(self, other)),
            max(self.ncolumns, other.ncolumns))

    def __make_row_from_value(self, value):
        """Make row from value of various type."""
        try:
            value = value.value
            new_row = vector.Vector(value, self._ncolumns)
        except AttributeError:
            if isinstance(value, int):
                new_row = vector.Vector(value, self._ncolumns)
            elif isinstance(value, str):
                new_row = vector.from_string(value)
                new_row.set_length(self._ncolumns)
            else:
                new_row = vector.from_iterable(value)
                new_row.set_length(self._ncolumns)
        return new_row


def from_string(value, zerofillers=None, onefillers=None):
    """Make Matrix object from string `value`."""
    try:
        row_str_list = [lex for lex in value.split(';') if lex != '']
    except AttributeError:
        raise TypeError(
            'expected `value` is string, but got '
            '{}'.format(type(value)))
    return Matrix(
        (vector.from_string(
            row,
            onefillers=onefillers,
            zerofillers=zerofillers).value for row in row_str_list),
        max(len(s) for s in row_str_list))


def from_iterable(value, zerofillers=None, onefillers=None):
    """Make Matrix object from list of iterables `value`."""
    matrix_rows = tuple(
        vector.from_iterable(
            row,
            onefillers=onefillers,
            zerofillers=zerofillers) for row in value)
    return Matrix(
        (row.value for row in matrix_rows),
        max(len(row) for row in matrix_rows))

#     @property
#     def T(self):
#         """
#             Transpose matrix
#         """
#         return self.transpose()

#     @property
#     def Rank(self):
#         """
#             Matrix rank
#         """
#         return self.rank()

#     @property
#     def diagonal_form(self):
#         matrix = list(self.__body)
#         nrows = self.nrows
#         ncols = self.ncols
#         from math import log
#         for i in xrange(nrows):
#             if matrix[i] == 0:
#                 continue
#             else:
#                 li = 1 << int(log(matrix[i], 2))
#             for j in xrange(nrows):
#                 if (matrix[j] & li) and (j != i):
#                     matrix[j] ^= matrix[i]
#         echelonMatrix = btMatrix2()
#         echelonMatrix.__body = matrix
#         echelonMatrix.__nrows = nrows
#         echelonMatrix.__ncols = ncols
#         return echelonMatrix

#     @property
#     def echelon_form(self):
#         matrix = list(self.__body)
#         nrows = self.nrows
#         ncols = self.ncols
#         from math import log
#         for i in xrange(nrows):
#             if matrix[i] == 0:
#                 continue
#             else:
#                 li = 1 << int(log(matrix[i], 2))
#             for j in xrange(i + 1, nrows):
#                 if matrix[j] & li:
#                     matrix[j] ^= matrix[i]
#         echelonMatrix = btMatrix2()
#         echelonMatrix.__body = matrix
#         echelonMatrix.__nrows = nrows
#         echelonMatrix.__ncols = ncols
#         return echelonMatrix

#     @property
#     def dual(self):
#         matrix = list(self.__body)
#         nrows = self.nrows
#         ncols = self.ncols
#         from math import log
#         identMatrix = []
#         for i in xrange(nrows):
#             if matrix[i] == 0:
#                 continue
#             else:
#                 logli = int(log(matrix[i], 2))
#                 li = 1 << logli
#                 identMatrix.append(ncols - logli - 1)
#             for j in xrange(nrows):
#                 if (matrix[j] & li) and (j != i):
#                     matrix[j] ^= matrix[i]
#         tmpM = btMatrix2()
#         tmpbody = sorted(filter(lambda x: x != 0, matrix), reverse=True)
#         for colnum in xrange(ncols):
#             if colnum not in identMatrix:
#                 tmpbody.insert(colnum, 1 << (ncols - colnum - 1))
#         tmpM.__nrows = len(tmpbody)
#         tmpM.__ncols = ncols
#         tmpM.__body = tmpbody
#         tmpM = tmpM.T
#         dualbody = []
#         for colnum in xrange(ncols):
#             if colnum not in identMatrix:
#                 dualbody.append(tmpM.__body[colnum])
#         tmpM.__body = dualbody
#         tmpM.__nrows = len(dualbody)
#         tmpM.__ncols = ncols
#         if tmpM.__nrows == 0 or tmpM.__ncols == 0:
#             tmpM.__ncols, tmpM.__nrows = 0, 0
#         return tmpM

#     def transpose(self):
#         """
#             Return the transpose matrix
#         """
#         transposed = BitMatrix()
#         fstring = '0' + str(self._ncolumns) + 'b'
#         lmat = [format(el, fstring) for el in self._body]
#         new_body = [int(''.join(el), 2) for el in zip(*lmat)]
#         transposed._body = new_body
#         transposed._ncolumns = self._nrows
#         transposed._nrows = self._ncolumns
#         return transposed


#     def getslice(self, start=0, end=-1):
#         pass

#     def rank(self):
#         """Return rank of matrix
#         """
#         matrix = list(self._body)
#         rank = 0
#         for i, row in enumerate(matrix):
#             non_zero_index = 1
#             for j in range(self.ncolumns):
#                 if row & non_zero_index:
#                     rank += 1
#                     break
#                 non_zero_index <<= 1
#             else:
#                 continue
#             for j in range(i + 1, self.nrows):
#                 if matrix[j] & non_zero_index:
#                     matrix[j] ^= row
#         return rank

#     @classmethod
#     def _from_list(cls, row_list=None):
#         """
#             Create matrix from list of integers
#         """
#         matrix = [0, []]
#         if row_list is None:
#             row_list = []
#         for row in row_list:
#             if isinstance(row, int):
#                 len_row = len(bin(row)[:2])
#                 matrix[1].append(row)
#             elif isinstance(row, str):
#                 row = row.replace(' ', '')
#                 for filler in cls.zerofillers:
#                     row = row.replace(filler, '0')
#                 for filler in cls.onefillers:
#                     row = row.replace(filler, '1')
#                 len_row = len(row)
#                 try:
#                     matrix[1].append(int(row, 2))
#                 except TypeError:
#                     continue
#             else:
#                 continue
#             if len_row > matrix[0]:
#                 matrix[0] = len_row

#         return matrix

#     @classmethod
#     def _from_string(cls, string=''):
#         """
#             Create matrix from string
#         """
#         matrix = [0, []]  # nrows, ncolumns, body
#         str_nospaces = string.replace(' ', '')
#         for filler in cls.onefillers:
#             str_nospaces = str_nospaces.replace(filler, '1')
#         for filler in cls.zerofillers:
#             str_nospaces = str_nospaces.replace(filler, '0')
#         str_split = str_nospaces.split(';')
#         for i, row in enumerate(str_split):
#             row_len = len(row)
#             if row_len > matrix[0]:
#                 matrix[0] = row_len
#             if row == '':
#                 matrix[1].append(0)
#             else:
#                 try:
#                     matrix[1].append(int(row, 2))
#                 except ValueError:
#                     raise ValueError('row {}: {} has wrong format'
#                                      ''.format(i, row))

#         return matrix


#     # private class methods
#     @classmethod
#     def __str_to_mat(self, s):
#         '''
#             Convert string to bitmatrix.
#             String format is follow:
#             """
#                 10*--*1
#                 01****1
#                 .........
#             """
#             1 is "1"
#             0 is {0, *, -}
#         '''
#         str_rows = str(s).replace(' ', '').split('\n')
#         import re
#         ncols = 0
#         nrows = 0
#         matrix = []
#         for row in str_rows:
#             if len(row) <= 0:
#                 continue
#             clear_row = ''.join(re.findall(
#                 '[\-01\*]+', row)).replace('-', '0').replace('*', '0')
#             matrix.append(int(clear_row, 2))
#             nrows = nrows + 1
#             if ncols < len(clear_row):
#                 ncols = len(clear_row)
#         return matrix, nrows, ncols  # matrix, nrows, ncols

#     def __getslice(self, start, end):
#         """
#             Suppose that bit matris is one big string, i.e.
#             string = "str1"+"str2"+"str3"+...
#             Function slice return int equals of
#             segment bitmat[start, start+count-1]
#             Example:
#                012345
#             0: 100111
#             1: 110011
#             2: 111001
#             slice(5, 10) = [0,5][1,0][1,2][1,3][1,4][1,5] = 0b111001
#             slice(0, 17) = 0b100111110011111001
#             slice(11,15) = 0b11110

#         """
#         len_of_mat = self.ncols * self.nrows
#         st = int(start) % len_of_mat
#         ed = int(end) % len_of_mat
#         if st > ed:
#             st, ed = ed, st
#             reverse = True
#         else:
#             reverse = False
#         # get coords of slice start
#         st_row = st / self.ncols
#         st_col = st % self.ncols
#         # get coords of end slice
#         ed_row = ed / self.ncols
#         ed_col = ed % self.ncols
#         if st_row == ed_row:
#             intslice = self.__body[st_row] >> (self.ncols - ed_col - 1)
#             intslice = intslice & ((1 << ed_col - st_col + 1) - 1)
#         else:
#             mask = (1 << (self.__ncols - st_col)) - 1
#             intslice = self.__body[st_row] & mask
#             for i in range(st_row + 1, ed_row):
#                 intslice = (intslice << self.ncols) ^ self.__body[i]
#             intslice = (intslice << (ed_col + 1)
#                         ) ^ (self.__body[ed_row] >> (self.ncols - ed_col - 1))
#         len_slice = ed - st + 1
#         if reverse is True:
#             s = bin(intslice)[::-1][:-2]
#             fill_str = ''.join(['0' for i in range(len_slice - len(s))])
#             intslice = int(s + fill_str, 2)
#         return intslice, len_slice

#     @staticmethod
#     def __get_num(el, length):
#         for i in xrange(length):
#             if el & 1:
#                 el >>= 1
#                 yield length - i - 1
#             else:
#                 el >>= 1
#         return


# def toLaTeX(A):
#     lat_str = str(A)
#     lines = lat_str.split('\n')
#     # The last line is size information, therefore we must delete it
#     lat_str = '\n'.join(lines[:-1])
#     lat_str = r'\begin{matrix}' + '\n' + lat_str \
#         + '\n' + r'\end{matrix}' + '\n'
#     lat_str = lat_str.replace(A.onefill, '1&').replace(A.zerofill, '0&')
#     lat_str = lat_str.replace('&\n', r'\\' + '\n')
#     return lat_str


# def main():
#     A = BitMatrix()
#     A.matrix = """
#                     1111111111111111
#                     --------11111111
#                     ----1111----1111
#                     --11--11--11--11
#                     -1-1-1-1-1-1-1-1
#                """
#     B = BitMatrix()
#     B.matrix = """
#                     1*11*
#                     *111*
#                     1*1**
#                     *111*
#                     *11*1
#     """
#     C = BitMatrix()
#     C.matrix = """
#                     1*1***1
#                     *11***1
#                     **11**1
#                     **1*1*1
#                     **1**11
#     """
#     # print C.T
#     # print A.T
#     # print A.echelon_form
#     # print A.diagonal_form
#     # print B
#     # dualA = A.dual
#     # print dualA
#     # tradualA = dualA.T
#     # print tradualA
#     # print A * tradualA
#     # print B
#     # print toLaTeX(B)
#     # C = btMatrix2()
#     # print toLaTeX(C)
#     A1 = BitMatrix(10000, 10000)
#     A1.dual
#     # C = A1.T
#     # print A
#     # print A.rank(columns=[12, 13], rows=(3))
#     # print A1.Rank
#     # print A.rank(columns=(12, 13), rows=[3])
#     # B = A1 + A2
#     # print B * A
#     # A1 * A1
#     # print A1


# # main()

