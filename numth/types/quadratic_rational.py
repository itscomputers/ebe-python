#   numth/types/quadratic_rational.py
#===========================================================
import math
import numbers
import operator

from .rational import frac
#===========================================================

class QuadraticRational(numbers.Number):
    """
    Quadratic rational elements.
    """
    def __init__(self, real, imag, root):
        self.real = frac(real)
        self.imag = frac(imag)
        self.root = frac(root)

    #=========================

    def __repr__(self):
        if self.root == -1:
            root_disp = ' \u2139'
        elif self.root.denom == 1:
            root_disp = ' \u221a{}'.format(self.root)
        else:
            root_disp = ' \u221a({})'.format(self.root)

        representation = ' + '.join(
            ''.join(format(y) for y in x) \
            for x in zip(self.components, ('', root_disp))
        )

        return representation.replace(' + -', ' - ')
    
    #=========================

    def component_map(self, function, other=None):
        if other is None:
            return QuadraticRational(*map(function, self.components), self.root)
        return QuadraticRational(
            *map(function, self.components, other.components),
            self.root
        )

    #-------------------------

    def is_compatible(self, other):
        return isinstance(other, QuadraticRational) and self.root == other.root

    #=========================

    @property
    def signature(self):
        return (self.real, self.imag, self.root)

    @property
    def components(self):
        return (self.real, self.imag)

    @property
    def norm(self):
        return self.real**2 - self.root * self.imag**2

    @property
    def conjugate(self):
        return QuadraticRational(self.real, -self.imag, self.root)

    @property
    def inverse(self):
        return self.conjugate.component_map(self.norm.inverse().__mul__)

    #=========================

    @classmethod
    def from_real(self, real, root):
        return QuadraticRational(frac(real), 0, root)

    @classmethod
    def from_complex(self, cplx):
        return QuadraticRational(frac(cplx.real), frac(cplx.imag), -1)

    #=========================

    def __eq__(self, other):
        if isinstance(other, QuadraticRational):
            return self.signature == other.signature

        if isinstance(other, numbers.Real):
            return self.imag == 0 and self.real == other

        if isinstance(other, numbers.Complex) and self.root == -1:
            return self == QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __lt__(self, other):
        if self.is_compatible(other):
            return self.norm < other.norm

        if isinstance(other, numbers.Real):
            return self < QuadraticRational.from_real(other, self.root)

        if isinstance(other, numbers.Complex) and self.root == -1:
            return self < QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __gt__(self, other):
        if self.is_compatible(other):
            return self.norm > other.norm

        if isinstance(other, numbers.Real):
            return self > QuadraticRational.from_real(other, self.root)

        if isinstance(other, numbers.Complex) and self.root == -1:
            return self > QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __le__(self, other):
       return not (self > other)

    #-------------------------

    def __ge__(self, other):
       return not (self < other)

    #=========================

    def __pos__(self):
        return self

    def __neg__(self):
        return self.component_map(operator.__neg__)

    #=========================

    def __add__(self, other):
        if self.is_compatible(other):
            return self.component_map(operator.__add__, other)

        if isinstance(other, numbers.Real):
            return QuadraticRational(self.real + frac(other), self.imag, self.root)

        if isinstance(other, numbers.Complex) and self.root == -1:
            return self + QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __sub__(self, other):
        return self + -other

    #-------------------------

    def __mul__(self, other):
        if self.is_compatible(other):
            real = (self.real * other.real) + (self.imag * other.imag * self.root)
            imag = (self.real * other.imag) + (self.imag * other.real)
            return QuadraticRational(real, imag, self.root)

        if isinstance(other, numbers.Real):
            return self.component_map(frac(other).__mul__)

        if isinstance(other, numbers.Complex) and self.root == -1:
            return self + QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __truediv__(self, other):
        if self.is_compatible(other):
            return self * other.inverse

        if isinstance(other, numbers.Real):
            return self.component_map(frac(other).__rtruediv__)

        if isinstance(other, numbers.Complex) and self.root == 1:
            return self / QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __floordiv__(self, other):
        if self.is_compatible(other):
            return (self / other).component_map(math.__floor__)

        if isinstance(other, numbers.Real):
            return self.component_map(frac(other).__rfloordiv__)

        if isinstance(other, numbers.Complex) and self.root == -1:
            return self // QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return self.inverse * other

