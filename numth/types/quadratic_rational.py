#   numth/types/quadratic_rational.py
#===========================================================
import math
import numbers
import operator

from ..basic import gcd, lcm
from .rational import frac
#===========================================================

class QuadraticRational(numbers.Number):
    """
    Quadratic rational elements.
    """
    def __init__(self, real, imag, denom, root, _normalize=True):
        self._real = int(real)
        self._imag = int(imag)
        self._denom = int(denom)
        self.root = int(root)
        if _normalize:
            d = gcd(real, imag, denom)
            if self._denom < 0:
                d = -d
            self._real //= d
            self._imag //= d
            self._denom //= d

    @property
    def real(self):
        return frac(self._real, self._denom)

    @property
    def imag(self):
        return frac(self._imag, self._denom)

    @property
    def components(self):
        return (self._real, self._imag, self._denom)

    @property
    def signature(self):
        return (*self.components, self.root)

    #=========================

    def __repr__(self):
        if self.root == -1:
            root_disp = ' \u2139'
        else:
            root_disp = ' \u221a{}'.format(self.root)

        representation = '( ' + ' + '.join([
            format(self._real),
            '{}{}'.format(self._imag, root_disp)
        ]) + ' ) / {}'.format(self._denom)

        return representation.replace(' + -', ' - ')

    #=========================

    def is_compatible(self, other):
        return isinstance(other, QuadraticRational) and self.root == other.root

    #=========================

    @property
    def _norm(self):
        return self._real**2 - self.root * self._imag**2

    @property
    def norm(self):
        return frac(self._norm, self._denom**2)

    @property
    def conjugate(self):
        return QuadraticRational(
            self._real,
            -self._imag,
            self._denom,
            self.root,
            _normalize=False
        )

    @property
    def inverse(self):
        return QuadraticRational(
            self._real * self._denom,
            -self._imag * self._denom,
            self._norm,
            self.root
        )

    #=========================

    @classmethod
    def from_real(self, real, root):
        real = frac(real)
        return QuadraticRational(real.numer, 0, real.denom, root, _normalize=False)

    @classmethod
    def from_complex(self, cplx):
        real = frac(cplx.real)
        imag = frac(cplx.imag)
        denom = lcm(real.denom, imag.denom)
        return QuadraticRational(
            real.numer * denom // real.denom,
            imag.numer * denom // imag.denom,
            denom,
            -1,
            _normalize=False
        )

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

        if isinstance(other, numbers.Complex) and self.root == -1:
            return self < QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __gt__(self, other):
        if self.is_compatible(other):
            return self.norm > other.norm

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
        return QuadraticRational(
            -self._real,
            -self._imag,
            self._denom,
            self.root,
            _normalize=False
        )

    #=========================

    def __add__(self, other):
        if self.is_compatible(other):
            real = self._real * other._denom + other._real * self._denom
            imag = self._imag * other._denom + other._imag * self._denom
            denom = self._denom * other._denom
            return QuadraticRational(real, imag, denom, self.root)

        if isinstance(other, int):
            return QuadraticRational(
                self._real + self._denom * other,
                self._imag,
                self._denom,
                self.root,
                _normalize=False
            )

        if isinstance(other, numbers.Real):
            o = frac(other)
            real = self._real * o.denom + self._denom * o.numer
            imag = self._imag * o.denom
            denom = self._denom * o.denom
            return QuadraticRational(real, imag, denom, self.root)


        if isinstance(other, numbers.Complex) and self.root == -1:
            return self + QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __sub__(self, other):
        return self + -other

    #-------------------------

    def __mul__(self, other):
        if self.is_compatible(other):
            real = self._real * other._real \
                    + self._imag * other._imag * self.root
            imag = self._real * other._imag \
                    + self._imag * other._real
            denom = self._denom * other._denom
            return QuadraticRational(real, imag, denom, self.root)

        if isinstance(other, int):
            d = gcd(other, self._denom)
            m = other // d
            real = self._real * m
            imag = self._imag * m
            denom = self._denom // d
            return QuadraticRational(
                self._real * m,
                self._imag * m,
                self._denom // d,
                self.root,
                _normalize=False
            )

        if isinstance(other, numbers.Real):
            o = frac(other)
            d = gcd(o.numer, self._denom)
            m = o.numer // d
            e = gcd(o.denom, self._real, self._imag)
            return QuadraticRational(
                self._real // e * m,
                self._imag // e * m,
                self._denom // d * o.denom // e,
                self.root,
                _normalize=False
            )

        if isinstance(other, numbers.Complex) and self.root == -1:
            return self * QuadraticRational.from_complex(other)

        return NotImplemented

    #-------------------------

    def __truediv__(self, other):
        if self.is_compatible(other):
            return self * other.inverse

        if isinstance(other, numbers.Real):
            return self * (frac(other).inverse())

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

