#   numth/types/quaternion.py
#===========================================================
import operator as op

from .rational import frac
from .arithmetic_type import ArithmeticType
from .gaussian_integer import GaussianInteger
from .gaussian_rational import GaussianRational
#===========================================================

def add_(a, b):
    return map(op.__add__, a.components, b.components)

def add_constant(a, b):
    return (a.components[0] + b, *a.components[1:])

def _mul_helper(index, a, b):
    sign = [(1, -1, -1, -1),
            (1, 1, 1, -1),
            (1, -1, 1, 1),
            (1, 1, -1, 1)][index]
    b_ind = [(0, 1, 2, 3),
            (1, 0, 3, 2),
            (2, 3, 0, 1),
            (3, 2, 1, 0)][index]
    return sum(map(
        lambda x, y, z: x * y * z,
        sign,
        a.components,
        (b.components[i] for i in b_ind)
    ))

def mul_(a, b):
    return (_mul_helper(index, a, b) for index in range(4))

def mul_constant(a, b):
    return map(lambda x: x * b, a.components)

def truediv_constant(a, b):
    return map(lambda x: x / frac(b), a.components)

def floordiv_(a, b):
    return (a / b).round.components

def floordiv_constant(a, b):
    return map(lambda x: x // b, a.components)

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

    @classmethod
    def from_gaussian_rational(self, gaussian_rational):
        return Quaternion(*gaussian_rational.components, 0, 0)

    @classmethod
    def from_gaussian_integer(self, gaussian_integer):
        return Quaternion(*gaussian_integer.components, 0, 0)

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
        return self.conjugate / frac(self.norm)

    @property
    def round(self):
        return self.__class__(
            *map(lambda x: x.round_prefer_toward_zero, self.components)
        )

    #=========================

    def _add_int(self, other):
        return self.__class__(*add_constant(self, other))

    def _add_Rational(self, other):
        return Quaternion(*add_constant(self, other))

    def _add_Quaternion(self, other):
        return Quaternion(*add_(self, other))

    #=========================

    def _mul_int(self, other):
        return self.__class__(*mul_constant(self, other))

    def _mul_Rational(self, other):
        return Quaternion(*mul_constant(self, other))

    def _mul_Quaternion(self, other):
        return Quaternion(*mul_(self, other))

    def _rmul_int(self, other):
        return self.__class__(*mul_constant(self, other))

    def _rmul_Rational(self, other):
        return Quaternion(*mul_constant(self, other))

    #=========================

    def _truediv_int(self, other):
        return Quaternion(*truediv_constant(self, other))

    def _truediv_rational(self, other):
        return Quaternion(*truediv_constant(self, other))

    def _truediv_Quaternion(self, other):
        return self * other.inverse

    def _rtruediv_int(self, other):
        return Quaternion(other, 0, 0, 0) / self

    def _rtruediv_Rational(self, other):
        return Quaternion(other, 0, 0, 0) / self

    #=========================

    def _floordiv_int(self, other):
        return self.__class__(*floordiv_constant(self, other))

    def _floordiv_Rational(self, other):
        return self.__class__(*floordiv_constant(self, other))

    def _floordiv_Quaternion(self, other):
        return self.__class__(*floordiv_(self, other))

    def _rfloordiv_int(self, other):
        return self.__class__(other, 0, 0, 0) // self

    def _rfloordiv_Rational(self, other):
        return Quaternion(other, 0, 0, 0) // self

    #=========================

    def __mod__(self, other):
        return self - (self // other) * other

    def __rmod__(self, other):
        return other - (other // self) * self

    #=========================

    def _inv_pow_int(self, other):
        return self.__pow__(-other).inverse

    def _zero_pow_int(self, other):
        return self.__class__(1, 0, 0, 0)

