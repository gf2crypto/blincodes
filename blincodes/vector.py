"""Module for working with vectors over GF(2)."""


class Vector():
    """Binary vector abstraction."""

    _zerofiller = '-'
    _onefiller = None

    def __init__(self, value=None, length=None):
        """Create new vector of size.

        :param: int `value` - integer representation of bit vector
        :param: int `length` - length of the vector
        """
        self._len = 0
        self._vector = 0
        if length:
            if not isinstance(length, int):
                raise TypeError(
                    'expected `length` is integer, got {}'
                    ''.format(type(length)))
            if length < 0:
                raise ValueError(
                    'expected `length` is non negative number,'
                    'got {} < 0'.format(length))
            self._len = length
        if value:
            if not isinstance(value, int):
                raise TypeError(
                    'expected  `value` is integer, got {}'.format(type(value)))
            if value < 0:
                raise ValueError(
                    'expected `value` is non negative integer, '
                    'got {} < 0'.format(value))
            if length > 0:
                self._vector = value & ((1 << length) - 1)
            else:
                self._vector = value
                self._len = len(bin(self._vector[2:]))

    @property
    def onefiller(self):
        """Return filler of 1's."""
        return self._onefiller

    @onefiller.setter
    def onefiller(self, filler='1'):
        """Set filler of 1's."""
        if not isinstance(filler, str):
            raise TypeError(
                'expected `filler` is string, got {}'.format(type(filler)))
        if len(filler) != 1:
            raise ValueError(
                'expeted the length of `filler` is 1, but '
                'got len(filler) = {}'.format(len(filler)))
        self._onefiller = filler

    @property
    def zerofiller(self):
        """Return filler of 0's."""
        return self._zerofiller

    @zerofiller.setter
    def zerofiller(self, filler='1'):
        """Set filler of 1's."""
        if not isinstance(filler, str):
            raise TypeError(
                'expected `filler` is string, got {}'.format(type(filler)))
        if len(filler) != 1:
            raise ValueError(
                'expeted the length of `filler` is 1, but '
                'got len(filler) = {}'.format(len(filler)))
        self._zerofiller = filler

    def __len__(self):
        """Return length of vector."""
        return self._len

    def from_string(self, value, zerofillers=None, onefillers=None):
        """Return vector from string.

        :param: str `values` - string representation of binary vector;
        :param: list or string `zerofillers` - possible fillers of '0';
        :param: list or string `onefillers` - possible fillers of '1'.

        Example:
        ('110**|0_1', zerofillers=['*', '_'], onefillers='|') ->    110001001
        """
        if not isinstance(value, str):
            raise TypeError(
                'expected `value` is string, got {}'.format(type(value)))
        try:
            try:
                for zero in zerofillers:
                    value = value.replace(zero, '0')
            except TypeError:
                for zero in [zerofillers]:
                    value = value.replace(zero, '0')
        except TypeError:
            raise TypeError(
                'expected zero filler is string, `{}` has type {}'
                ''.format(zero, type(zero)))

        try:
            try:
                for one in onefillers:
                    value = value.replace(one, '1')
            except TypeError:
                for one in [onefillers]:
                    value = value.replace(one, '1')
        except TypeError:
            raise TypeError(
                'expected one filler is string, `{}` has type {}'
                ''.format(one, type(one)))
        try:
            vector = int(value, 2)
        except ValueError:
            raise ValueError(
                'cannot convert string `{}` to binary vector'
                ''.format(value))
        return self.__class__(vector, len(value))

    def from_iterable(self, value, zerofillers=None, onefillers=None):
        """Return vector from string.

        :param: `value` - representation of binary vector as iterable;
        :param: list or string `zerofillers` - possible fillers of '0';
        :param: list or string `onefillers` - possible fillers of '1'.

        Example:
        (('110**|0_1', True, False, 0, 1 ,10, [1, 2] , []),
            zerofillers=['*', '_'], onefillers='|') -> 1100010011001110
        """
        vector = ''
        try:
            for i in value:
                if isinstance(i, str):
                    vector += i
                elif i:
                    vector += '1'
                else:
                    vector += '0'
        except TypeError:
            raise TypeError(
                'expected `value` has any iterable type, got {}'
                ''.format(type(value)))
        return self.from_string(vector,
                                zerofillers=zerofillers,
                                onefillers=onefillers)

    def set_length(self, length):
        """Change length of a vector.

        10011.set_length(7) -> 0010011
        10011.set_length(3) -> 011
        """
        if not isinstance(length, int):
            raise TypeError('expected `length` is integer, not {}'
                            ''.format(type(length)))
        if length < 0:
            raise ValueError('expected `length` is greater than 0, '
                             'but {} < 0'.format(length))
        self._vector = self._vector & ((1 << length) - 1)
        self._len = length
        return self

    def resize(self, delta_length):
        """Change size of vector by 'delta_length'."""
        if not isinstance(delta_length, int):
            raise TypeError(
                'expected `delta_length` is integer, got {}'
                ''.format(type(delta_length)))
        return self.set_length(self._len + delta_length)

    def copy(self):
        """Return copy of vector."""
        return self.__class__(self.value, len(self))

    def __bool__(self):
        """Return True iff len > 0."""
        if self._len == 0:
            return False
        return True

    def __repr__(self):
        """Return representation of Vector class as string."""
        rep = 'Vector(len={}, [{vector}])'
        return rep.format(len(self), vector=str(self))

    def __str__(self):
        """Return representation of Vector as string to print."""
        if not self:
            return ''
        str_vec = bin(self._vector)[2:].zfill(len(self))
        if self._onefiller:
            str_vec = str_vec.replace("1", self._onefiller)
        if self._zerofiller:
            str_vec = str_vec.replace("0", self._zerofiller)
        return str_vec

    def __setitem__(self, index, value):
        """Set item of vector: vector[index] = value."""
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
        """Return vector[index].

        If `index` is integer then function retuns integer 0 or 1.
        If `index` is slice then function returns instance of Vector.

        """
        if isinstance(index, int):
            index = self._len - (index % self._len) - 1
            return int(bool(self._vector & (1 << index)))
        # index is slice
        try:
            vec_len = 0
            vec_value = 0
            for i in range(*index.indices(self._len)):
                vec_value <<= 1
                if self._vector & (1 << (self._len - i - 1)):
                    vec_value ^= 1
                vec_len += 1
        except AttributeError:
            raise TypeError(
                '`index` must be integer or slice, not '
                '`{}`'.format(type(index)))
        if not vec_len:
            return None
        return Vector(value=vec_value, length=vec_len)

    def __eq__(self, other):
        """Return True if self == other, else return False."""
        if not isinstance(other, self.__class__):
            raise ValueError("expected other is `Vector`, not {}"
                             "".format(type(other)))
        return len(self) == len(other) and self._vector == other.value

    def __ne__(self, other):
        """Return True if self != other, else return False."""
        return not self == other

    def __imul__(self, other):
        """Bitwise vector multiplication.

        self = self * other and return self
        """
        if not isinstance(other, self.__class__):
            raise TypeError("expected `Vector` object, not {}"
                            "".format(type(other)))

        self._vector &= other.value
        return self

    def __mul__(self, other):
        """Bitwise vector multiplication.

        return self * other
        """
        mul = self.__class__(self._vector, len(self))
        mul *= other
        return mul

    def __iadd__(self, other):
        """Bitwise vector addition (xor).

        self = self + other and return self
        """
        if not isinstance(other, self.__class__):
            raise TypeError("expected `Vector` object, not {}"
                            "".format(type(other)))

        self._vector = self._vector ^ other.value
        return self

    def __add__(self, other):
        """Bitwise vector addition (xor).

        return self + other
        """
        summa = self.__class__(self._vector, len(self))
        summa += other
        return summa

    def __ilshift__(self, pos):
        """Non cylic left shift of vector by `pos`.

        self <<= pos and return self
        """
        self._vector = (self._vector << pos)
        return self

    def __irshift__(self, pos):
        """Non cylic right shift of vector by `pos`.

        self >>= pos and return self
        """
        self._vector >>= pos
        return self

    def __lshift__(self, pos):
        """Non cylic left shift of vector by `pos`.

        return self << pos
        """
        vec = self.copy()
        vec <<= pos
        return vec

    def __rshift__(self, pos):
        """Non cylic right shift of vector by `pos`.

        return self >> pos
        """
        vec = self.copy()
        vec >>= pos
        return vec

    def to_latex_str(self):
        """Return string representation of vector to insert in LaTeX document.

        Example:
            '0011101' -> '0&0&1&1&1&0&1'
        """
        latex = str(self).replace(
            self.onefiller, '1').replace(
                self.zerofiller, '0').replace(
                    '1', '1&').replace(
                        '0', '0&')
        return latex[:-1] if latex else ''

    @classmethod
    def get_onefiller(cls):
        """Return filler of 1's."""
        return cls._onefiller

    @classmethod
    def set_onefiller(cls, filler='1'):
        """Set filler of 1's."""
        if not isinstance(filler, str):
            raise TypeError(
                'expected `filler` is string, got {}'.format(type(filler)))
        if len(filler) != 1:
            raise ValueError(
                'expeted the length of `filler` is 1, but '
                'got len(filler) = {}'.format(len(filler)))
        cls._onefiller = filler

    @classmethod
    def get_zerofiller(cls):
        """Return filler of 0's."""
        return cls._zerofiller

    @classmethod
    def set_zerofiller(cls, filler='1'):
        """Set filler of 0's."""
        if not isinstance(filler, str):
            raise TypeError(
                'expected `filler` is string, got {}'.format(type(filler)))
        if len(filler) != 1:
            raise ValueError(
                'expeted the length of `filler` is 1, but '
                'got len(filler) = {}'.format(len(filler)))
        cls._zerofiller = filler
