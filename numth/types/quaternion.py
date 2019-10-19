#   numth/types/quaternion.py
#===========================================================
import numbers
import operator as op

from .rational import frac
from .quadratic import Quadratic
from .quadratic_integer import QuadraticInteger
from .gaussian_integer import GaussianInteger
#===========================================================

class Quaternion(numbers.Number):

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

    def is_same_type(self, other):
        return type(self) is type(other)

    def is_similar_type(self, other):
        return self.is_same_type(other)

    #-------------------------

    @classmethod
    def from_components(self, *components):
        return Quaternion(*components)

    @classmethod
    def from_quadratic(self, quadratic):
        if quadratic.is_complex:
            return self.from_components(*quadratic.components, 0, 0)

        return NotImplemented

    @classmethod
    def from_quadratic_integer(self, quadratic_integer):
        return self.from_quadratic(quadratic_integer)

    @classmethod
    def from_gaussian_integer(self, gaussian_integer):
        return self.from_quadratic_integer(gaussian_integer)

    @property
    def to_quadratic(self):
        if self.is_complex:
            return Quadratic(self.r, self.i, -1)

        return NotImplemented

    @property
    def to_gaussian_integer(self):
        if self.is_complex:
            rounded = self.round
            return GaussianInteger(rounded.r, rounded.i)

        return NotImplemented

    #=========================

    def __pos__(self):
        return self

    def __neg__(self):
        return self.from_components(*map(op.__neg__, self.components))

    @property
    def conjugate(self):
        return self.from_components(self.components[0], *map(op.__neg__, self.components[1:]))

    @property
    def norm(self):
        return sum(map(lambda x: x**2, self.components))

    @property
    def inverse(self):
        norm = self.norm
        return self.from_components(
            *map(lambda x: x / norm, self.conjugate.components)
        )

    @property
    def round(self):
        return self.from_components(
            *map(lambda x: x.round_to_nearest_int, self.components)
        )

    #=========================

    def __eq__(self, other):
        if self.is_similar_type(other):
            return self.components == other.components

        if isinstance(other, Quadratic):
            return other.is_complex \
                and self.is_complex and \
                self.components[:2] == other.components

        if isinstance(other, numbers.Rational):
            return self.is_real and self.r == other

        return NotImplemented

    def __lt__(self, other):
        if self.is_similar_type(other):
            return self.norm < other.norm

        return NotImplemented

    def __gt__(self, other):
        if self.is_similar_type(other):
            return self.norm > other.norm

        return NotImplemented

    def __le__(self, other):
        return not (self > other)

    def __ge__(self, other):
        return not (self < other)

    #=========================

    def _add_int(self, other):
        return self.from_components(self.r + other, *self.components[1:])

    def _add_rational(self, other):
        return self._add_int(other)

    def _add_quadratic(self, other):
        return self._add_same_type(self.from_quadratic(other))

    def _add_quadratic_integer(self, other):
        return self._add_same_type(self.from_quadratic_integer(other))

    def _add_same_type(self, other):
        return self.from_components(
            *map(op.__add__, self.components, other.components)
        )

    def _add_similar_type(self, other):
        return self._add_same_type(other)

    def __add__(self, other):
        if isinstance(other, int):
            return self._add_int(other)

        if isinstance(other, Rational):
            return self._add_rational(other)

        if isinstance(other, QuadraticInteger) and other.is_complex:
            return self._add_quadratic_integer(other)

        if isinstance(other, Quadratic) and other.is_complex:
            return self._add_quadratic(other)

        if self.is_same_type(other):
            return self._add_same_type(other)

        if self.is_similar_type(other):
            return self._add_similar_type(other)

        return NotImplemented

    #=========================

    def __sub__(self, other):
        return self + -other

    #=========================

    def _mul_int(self, other):
        return self.from_components(
            *map(lambda x: x * other, self.components)
        )

    def _mul_rational(self, other):
        return self._mul_int(other)

    def _mul_quadratic(self, other):
        return self._mul_same_type(self.from_quadratic(other))

    def _mul_quadratic_integer(self, other):
        return self._mul_same_type(self.from_quadratic_integer(other))

    def _mul_same_type(self, other):
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

        return self.from_components(*[
            mul_each(index, self.components, quaternion(other).components)
            for index in range(4)
        ])

    def _mul_similar_type(self, other):
        return self._mul_same_type(other)

    def __mul__(self, other):
        if isinstance(other, int):
            return self._mul_int(other)

        if isinstance(other, Rational):
            return self._mul_rational(other)

        if isinstance(other, QuadraticInteger) and other.is_complex:
            return self._mul_quadratic_integer(other)

        if isinstance(other, Quadratic) and other.is_complex:
            return self._mul_quadratic(other)

        if self.is_same_type(other):
            return self._mul_same_type(other)

        if self.is_similar_type(other):
            return self._mul_similar_type(other)

        return NotImplemented

    #=========================

    def _div_int(self, other):
        return self.from_components(
            *map(lambda x: x / other, self.components)
        )

    def _div_rational(self, other):
        return self._div_int(other)

    def _div_quadratic(self, other):
        return self._div_same_type(self.from_quadratic(other))

    def _div_quadratic_integer(self, other):
        return self._div_same_type(self.from_quadratic_integer(other))

    def _div_same_type(self, other):
        return self * other.inverse

    def _div_similar_type(self, other):
        return self._div_same_type(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            return self._div_int(other)

        if isinstance(other, Rational):
            return self._div_rational(other)

        if isinstance(other, QuadraticInteger) and other.is_complex:
            return self._div_quadratic_integer(other)

        if isinstance(other, Quadratic) and other.is_complex:
            return self._div_quadratic(other)

        if self.is_same_type(other):
            return self._div_same_type(other)

        if self.is_similar_type(other):
            return self._div_similar_type(other)

        return NotImplemented

    #=========================

    def _floordiv_int(self, other):
        return self.from_components(
            *map(lambda x: (x / other).round_to_nearest_int, self.components)
        )

    def _floordiv_rational(self, other):
        return self._floordiv_int(other)

    def _floordiv_quadratic(self, other):
        return self._floordiv_same_type(self.from_quadratic(other))

    def _floordiv_quadratic_integer(self, other):
        return self._floordiv_same_type(self.from_quadratic_integer(other))

    def _floordiv_same_type(self, other):
        return (self / other).round

    def _floordiv_similar_type(self, other):
        return self._floordiv_same_type(other)

    def __floordiv__(self, other):
        if isinstance(other, int):
            return self._floordiv_int(other)

        if isinstance(other, Rational):
            return self._floordiv_rational(other)

        if isinstance(other, QuadraticInteger) and other.is_complex:
            return self._floordiv_quadratic_integer(other)

        if isinstance(other, Quadratic) and other.is_complex:
            return self._floordiv_quadratic(other)

        if self.is_same_type(other):
            return self._floordiv_same_type(other)

        if self.is_similar_type(other):
            return self._floordiv_similar_type(other)

    #=========================

    def __mod__(self, other):
        return self - (self // other) * other

    def __rmod__(self, other):
        return other - (other // self) * self

    #=========================

    def __pow__(self, other, modulus=None):
        if not isinstance(other, int):
            raise TypeError('Integre exponent is required')

        if other < 0:
            result = pow(self, -other).inverse
            return result if modulus is None else result % modulus

        if other == 0:
            return self.from_components(1, 0, 0, 0)

        if other == 1:
            return self if modulus is None else self % modulus

        if other % 2 == 0:
            return pow(self * self, other // 2, modulus)

        result = self * pow(self * self, other // 2, modulus)
        return result if modulus is None else result % modulus

    #=========================

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __rmul__(self, other):
        if isinstance(other, numbers.Rational):
            return self * other

        if isinstance(other, Quadratic):
            return Quaternion.from_quadratic(other) * self

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Rational):
            return self.inverse * other

        if isinstance(other, Quadratic):
            return Quaternion.from_quadratic(other) / self

    def __rfloordiv__(self, other):
        if isinstance(other, numbers.Rational):
            return Quaternion(other, 0, 0, 0) // self

        if isinstance(other, Quadratic):
            return Quaternion.from_quadratic(other) // self

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

