"""
    Module for working with vectors over GF(2)
"""


class Vector():
    """
        Binary vector abstraction

        _len - length of vector
        _vector - value of vector
    """
    zerofillers = ['*', '-']  # use for represent of zeroes
    onefillers = []   # use for represent of ones

    def __init__(self, value=None, size=0):
        """
            Create new vector of size `size` and init them by `value`
        """
        self._len = 0
        self._vector = 0
        self._zerofiller = '*'
        self._onefiller = '1'
        if size:
            self.set_size(size)
        if value:
            self.value = value

    def __len__(self):
        """return length of vector"""
        return self._len

    @property
    def value(self):
        """
            Return raw value of Vector
        """
        return self._vector

    @value.setter
    def value(self, new_value):
        new_len = self._len
        if not isinstance(new_value, int):
            if not isinstance(new_value, str):
                try:
                    value_str = ''.join([str(x) for x in new_value])
                except TypeError:
                    raise TypeError('expected `value` is integer, string'
                                    ' or any iterable type')
            for one in self.onefillers:
                value_str = value_str.replace(one, '1')
            for zero in self.zerofillers:
                value_str = value_str.replace(zero, '0')
            if not value_str:
                value_int = 0
            else:
                try:
                    value_int = int(value_str, 2)
                except ValueError:
                    raise ValueError('cannot transform value `{}` '
                                     'to binary vector'.format(value_str))
                new_len = len(value_str)
        else:
            value_int = new_value
        self._len = new_len
        self._vector = value_int & max((1 << self._len) - 1, 0)

    @property
    def zerofiller(self):
        """Representer of zeroes
        """
        return self._zerofiller

    @zerofiller.setter
    def zerofiller(self, filler):
        if not isinstance(filler, str):
            raise TypeError("`filler` must be string")
        if len(filler) != 1:
            raise ValueError("`filler` must be only one char")
        self._zerofiller = filler

    @property
    def onefiller(self):
        """Representer of ones
        """
        return self._onefiller

    @onefiller.setter
    def onefiller(self, filler):
        if not isinstance(filler, str):
            raise TypeError("`filler` must be string")
        if len(filler) != 1:
            raise ValueError("`filler` must be only one char, but "
                             "len(filler) == {}".format(len(filler)))
        self._onefiller = filler

    def set_size(self, new_size, shift=True):
        """Change size of vector

        If shift is False:
            10011.set_size(7, False) -> 0010011
            10011.set_size(3, False) -> 011
        if shift is True:
            10011.set_size(7, True) -> 1001100
            10011.set_size(3, True) -> 100
        """
        if not isinstance(new_size, int):
            raise TypeError('expected `new_size` is integer, not {}'
                            ''.format(type(new_size)))
        if new_size < 0:
            raise ValueError('expected `new_size` is greater than 0, '
                             'but {} < 0'.format(new_size))
        if not shift:
            self._vector = self._vector & ((1 << new_size) - 1)
        else:
            if self._len > new_size:
                self._vector = self._vector >> (self._len - new_size)
            else:
                self._vector = self._vector << (new_size - self._len)
        self._len = new_size
        return self

    def resize(self, delta_size, shift=True):
        """Change size of vector by 'delta_size'

        Parameter `shift` has the same meaning as in `setsize` method.
        """
        self.set_size(self._len + delta_size, shift=shift)
        return self

    def copy(self):
        """ Return copy of vector """
        return self.__class__(self.value, len(self))

    def __bool__(self):
        if self._len == 0:
            return False
        return True

    def __repr__(self):
        rep = 'gf2.vector(len={}, [{vector}])'
        return rep.format(len(self), vector=str(self))

    def __str__(self):
        if not self:
            return ''
        str_vec = bin(self._vector)[2:].zfill(len(self))
        if self.onefiller:
            str_vec = str_vec.replace("1", self.onefiller)
        if self.zerofiller:
            str_vec = str_vec.replace("0", self.zerofiller)
        return str_vec

    def __setitem__(self, index, value):
        if not isinstance(index, int):
            raise TypeError("`index` must be integer not "
                            "`{}`".format(type(index)))

        if isinstance(value, str) and value == '0':
            value = False
        else:
            value = bool(value)
        index = self._len - (index % self._len) - 1
        bit = self._vector & (1 << index)
        self._vector ^= bit  # set bit in zero
        if value:
            self._vector ^= (1 << index)  # set value

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("`index` must be integer not "
                            "`{}`".format(type(index)))
        index = self._len - (index % self._len) - 1
        return int(bool(self._vector & (1 << index)))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("expected other is `Vector`, not {}"
                             "".format(type(other)))
        return len(self) == len(other) and self._vector == other.value

    def __ne__(self, other):
        return not self == other

    def __imul__(self, other):
        """vector multiplication
        :param `Vector` other

        return self * other
        """
        if not isinstance(other, self.__class__):
            raise TypeError("expected `Vector` object, not {}"
                            "".format(type(other)))

        self._vector &= other.value
        return self

    def __mul__(self, other):
        mul = self.__class__(self.value, len(self))
        mul *= other
        return mul

    def __iadd__(self, other):
        """sum of two matrices
        :param `Vector` other

        return self + other
        """
        if not isinstance(other, self.__class__):
            raise TypeError("expected `Vector` object, not {}"
                            "".format(type(other)))

        self._vector = self._vector ^ other.value
        return self

    def __add__(self, other):
        summa = self.__class__(self.value, len(self))
        summa += other
        return summa

    def __ilshift__(self, pos):
        self.value = (self._vector << pos)
        return self

    def __irshift__(self, pos):
        self._vector >>= pos
        return self

    def __lshift__(self, pos):
        vec = self.copy()
        vec <<= pos
        return vec

    def __rshift__(self, pos):
        vec = self.copy()
        vec >>= pos
        return vec

    def to_latex_str(self):
        """
            Return string representation of vector to insert in LaTeX document

            Example:
            '0011101' -> '0&0&1&1&1&0&1'
        """
        latex = str(self).replace(
            self.onefiller, '1').replace(
                self.zerofiller, '0').replace(
                    '1', '1&').replace(
                        '0', '0&')
        return latex[:-1] if latex else ''
