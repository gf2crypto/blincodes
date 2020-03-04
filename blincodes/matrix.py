"""Module for working with matricies over GF(2) field."""

from random import randint
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

    @property
    def rank(self):
        """Evaluate the rank of the matrix."""
        matrix_rows = tuple(self.copy())
        rank_value = 0
        for i, row in enumerate(matrix_rows):
            for j in range(self.ncolumns):
                if row[j]:
                    rank_value += 1
                    break
            else:
                continue
            for row2 in (v for k, v in enumerate(matrix_rows)
                         if k > i and matrix_rows[k][j]):
                row2 += row
        return rank_value

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

    def to_latex_str(self):
        """Return representation of matrix as LaTeX string."""
        return '\\\\\n'.join(tuple(row.to_latex_str() for row in self))

    def copy(self):
        """Make copy of the matrix."""
        return Matrix(
            (row.value for row in self),
            self.ncolumns)

    def submatrix(self, columns=None):
        """Return matrix contained in columns."""
        if not columns:
            return self
        sub_matr = []
        for row in self:
            value = 0
            for i in columns:
                value <<= 1
                if row[i]:
                    value ^= 1
            sub_matr.append(value)
        return Matrix(sub_matr, len(columns))

    def transpose(self):
        """Return trasposition of matrix."""
        return Matrix(
            (int(''.join(el), 2)
             for el in zip(*(str(row) for row in self))),
            self.nrows)

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


def zero(nrows, ncolumns=None):
    """Return (nrows x ncolumns)-matrix of zeores."""
    if not ncolumns:
        ncolumns = nrows
    return Matrix([0] * nrows, ncolumns)


def identity(nrows, ncolumns=None):
    """Return (nrows x ncolumns) identity matrix."""
    if not ncolumns:
        ncolumns = nrows
    return Matrix(
        (1 << (ncolumns - i - 1) for i in range(nrows)),
        ncolumns)


def random(nrows, ncolumns=None, max_rank=False):
    """Return random matrix."""
    if not ncolumns:
        ncolumns = nrows
    matrix = Matrix(
        (randint(1, (1 << ncolumns) - 1) for _ in range(nrows)),
        ncolumns)
    if max_rank:
        while matrix.rank != min(nrows, ncolumns):
            matrix = Matrix(
                (randint(1, (1 << ncolumns) - 1) for _ in range(nrows)),
                ncolumns)
    return matrix




#     @property
#     def T(self):
#         """
#             Transpose matrix
#         """
#         return self.transpose()

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
