#   numth/types/quaternion.py
#===========================================================
import operator as op

from .rational import frac
from .arithmetic_type import ArithmeticType
from .quadratic import Quadratic
from .quadratic_integer import QuadraticInteger
from .gaussian_integer import GaussianInteger
#===========================================================

class Quaternion(ArithmeticType):

    def __init__(self, *components):
        self.components = tuple(map(frac, components))

    @property
    def r(self):
        return self.components[0]

    @property
    def i(self):
        return self.components[1]

    @property
    def j(self):
        return self.components[2]

    @property
    def k(self):
        return self.components[3]

    @property
    def is_real(self):
        return set(self.components[1:]) == set([0])

    @property
    def is_complex(self):
        return set(self.components[2:]) == set([0])

    #=========================

    @property
    def _real_disp(self):
        if self.r == 0 and not self.is_real:
            return None
        return format(self.r)

    def _other_disp(self, ch):
        val = eval('self.{}'.format(ch))
        if val == 0:
            return None
        if val == 1:
            return ch
        if val == -1:
            return '-{}'.format(ch)
        return '{} {}'.format(val, ch)

    def __repr__(self):
        displays = filter(
            None.__ne__,
            [
                self._real_disp,
                self._other_disp('i'),
                self._other_disp('j'),
                self._other_disp('k')
            ]
        )
        return ' + '.join(displays).replace(' + -', ' - ')

    #=========================

    def _eq_int(self, other):
        return self.components == (other, 0, 0, 0)

    def _eq_Rational(self, other):
        return self.components == (other, 0, 0, 0)

    def _eq_Quaternion(self, other):
        return self.components == other.components

    #=========================

    def __neg__(self):
        return self.__class__(*map(op.__neg__, self.components))

    @property
    def conjugate(self):
        return self.__class__(self.components[0], *map(op.__neg__, self.components[1:]))

    @property
    def norm(self):
        return sum(map(lambda x: x**2, self.components))

    @property
    def inverse(self):
        norm = frac(self.norm)
        return Quaternion(
            *map(lambda x: x / norm, self.conjugate.components)
        )

    @property
    def round(self):
        return self.__class__(
            *map(lambda x: x.round_to_nearest_int, self.components)
        )

    #=========================

    def _add_int(self, other):
        return self.__class__(self.r + other, *self.components[1:])

    def _add_Rational(self, other):
        return Quaternion(self.r + other, *self.components[1:])

    def _add_Quaternion(self, other):
        return self.__class__(
            *map(op.__add__, self.components, other.components)
        )

    #=========================

    def _mul_int(self, other):
        return self.__class__(
            *map(lambda x: x * other, self.components)
        )

    def _mul_rational(self, other):
        return Quaternion(
            *map(lambda x: x * other, self.components)
        )

    def _mul_components(self, other):
        def mul_each(index, s_cmpt, o_cmpt):
            sign = [(1, -1, -1, -1),
                    (1, 1, 1, -1),
                    (1, -1, 1, 1),
                    (1, 1, -1, 1)][index]
            o_ind = [(0, 1, 2, 3),
                    (1, 0, 3, 2),
                    (2, 3, 0, 1),
                    (3, 2, 1, 0)][index]
            return sum(map(
                lambda x, y, z: x * y * z,
                sign,
                s_cmpt,
                (o_cmpt[i] for i in o_ind)
            ))
        return [
            mul_each(index, self.components, other.components)
            for index in range(4)
        ]

    def _mul_Quaternion(self, other):
        return Quaternion(*self._mul_components(other))

    def _rmul_int(self, other):
        return self.__class__(other, 0, 0, 0) * self

    def _rmul_Rational(self, other):
        return self.__class__(other, 0, 0, 0) * self

    #=========================

    def _truediv_int(self, other):
        return Quaternion(
            *map(lambda x: x / frac(other), self.components)
        )

    def _truediv_rational(self, other):
        return Quaternion(
            *map(lambda x: x / frac(other), self.components)
        )

    def _truediv_Quaternion(self, other):
        return self * other.inverse

    def _rtruediv_int(self, other):
        return Quaternion(other, 0, 0, 0) / self

    def _rtruediv_Rational(self, other):
        return Quaternion(other, 0, 0, 0) / self

    #=========================

    def _floordiv_int(self, other):
        return self.__class__(
            *map(lambda x: x // other, self.components)
        )

    def _floordiv_Rational(self, other):
        return self.__class__(
            *map(lambda x: x // other, self.components)
        )

    def _floordiv_Quaternion(self, other):
        return (self / other).round

    def _rfloordiv_int(self, other):
        return self.__class__(other, 0, 0, 0) // self

    def _rfloordiv_Rational(self, other):
        return self.__class__(other, 0, 0, 0) // self

    #=========================

    def _mod_int(self, other):
        return self.__class__(
            *map(lambda x: x % other, self.components)
        )

    def _mod_Rational(self, other):
        return self.__class__(
            *map(lambda x: x % other, self.components)
        )

    def _mod_Quaternion(self, other):
        return self - (self // other) * other

    def _rmod_int(self, other):
        return Quaternion(other, 0, 0, 0) % self
        return self._reverse('mod', other)

    def _rmod_Rational(self, other):
        return Quaternion(other, 0, 0, 0) % self
        return self._reverse('mod', other)

    #=========================

    def _inv_pow_int(self, other):
        return self.__pow__(-other).inverse

    def _zero_pow_int(self, other):
        return self.__class__(1, 0, 0, 0)

    def _inv_pow_mod_int(self, other, modulus):
        return self.__pow__(-other, modulus).inverse % modulus

    def _zero_pow_mod_int(self, _other, _modulus):
        return self.__class__(1, 0, 0, 0)

#===========================================================
from ..basic import div_with_small_remainder
from .rational import frac, Rational
#===========================================================

def quaternion(number):
    if type(number) in [int, float, Rational]:
        return Quaternion(number, 0, 0, 0)
    if type(number) is Quaternion:
        return number

#=============================

class rQuaternion:
    """
    Quaternion number class.

    params
    + components = (a, b, c, d) : (int, int, int, int)

    represents
    a + b*i + c*j + d*k
    """

    def __init__(self, *components):
        self.components = components
        self.r, self.i, self.j, self.k = components

    #-------------------------

    def __repr__(self):
        representation = ' ' + ' + '.join(
            ''.join(format(y) for y in x) \
            for x in zip(self.components, ['', ' i', ' j', ' k']))

        return representation.replace(' + -', ' - ')\

    #=========================

    def __eq__(self, other):
        return self.components == quaternion(other).components

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.norm() < quaternion(other).norm()

    def __gt__(self, other):
        return self.norm() > quaternion(other).norm()

    def __le__(self, other):
        return not (self > other)

    def __ge__(self, other):
        return not (self < other)

    #=========================

    def component_map(self, function, other=None):
        if other is not None:
            return Quaternion(*map(
                function,
                self.components,
                quaternion(other).components
            ))

        return Quaternion(*map(function, self.components))

    #=========================

    def norm(self):
        return sum(self.component_map(lambda x: x**2).components)

    #-------------------------

    def conjugate(self):
        return Quaternion(self.r, *map(lambda x: -x, self.components[1:]))

    #-------------------------

    def inverse(self):
        norm = self.norm()
        if abs(norm) == 1:
            norm_inverse = norm
        else:
            norm_inverse = frac(norm).inverse

        return self.conjugate().component_map(lambda x: x * norm_inverse)

    #=========================

    def __neg__(self):
        return self.component_map(lambda x: -x)

    #-------------------------

    def round(self):
        return self.component_map(lambda x: int(x + .5))

    #=========================

    def __add__(self, other):
        return self.component_map(lambda x, y: x + y, other)

    def __radd__(self, other):
        return self + other

    #-------------------------

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    #-------------------------

    def __mul__(self, other):
        def mul_each(index, s_comp, o_comp):
            sign = [(1, -1, -1, -1),
                    (1, 1, 1, -1),
                    (1, -1, 1, 1),
                    (1, 1, -1, 1)][index]
            o_ind = [(0, 1, 2, 3),
                    (1, 0, 3, 2),
                    (2, 3, 0, 1),
                    (3, 2, 1, 0)][index]
            return sum(map(
                lambda x, y, z: x * y * z,
                sign,
                s_comp,
                (o_comp[i] for i in o_ind)
            ))

        return Quaternion(*[
            mul_each(index, self.components, quaternion(other).components)
            for index in range(4)
        ])

    def __rmul__(self, other):
        return self * other

    #-------------------------

    def __truediv__(self, other):
        return self * quaternion(other).inverse()

    def __rtruediv__(self, other):
        return self.inverse() * other

    #-------------------------

    def __floordiv__(self, other):
        return (self * quaternion(other).conjugate()).component_map(
                lambda x: x // quaternion(other).norm())

    def __rfloordiv__(self, other):
        return (self.conjugate() * quaternion(other)) // self.norm()

    #-------------------------

    def __pow__(self, other):
        if other < 0:
            return self.inverse()**(-other)
        if other == 0:
            return Quaternion(1, 0, 0, 0)
        if other == 1:
            return self
        if other % 2 == 0:
            return (self * self) ** (other // 2)

        return self * (self * self) ** (other // 2)

    #-------------------------

    def __mod__(self, other):
        if type(other) is int:
            def mod_with_small_remainder(x):
                return div_with_small_remainder(x, other)[1]
            return self.component_map(mod_with_small_remainder)
        return self - (self // other) * other

    def __rmod__(self, other):
        return quaternion(other) % self

