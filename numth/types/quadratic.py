#   numth/quadratic.py
#===========================================================
from ..basic import mod_inverse, round_down
from .rational import frac, Rational
#===========================================================

class Quadratic:
    """
    Quadratic number class.

    params
    + real : int (or numerical type)
    + imag : int (or numerical type)
    + root : int (or numerical type)

    represents
    real + imag * sqrt(root)
    """

    def __init__(self, real, imag, root):
        self.signature = (real, imag, root)
        self.components = (real, imag)
        self.real = real
        self.imag = imag
        self.root = root

    #-------------------------

    def __repr__(self):
        if self.root == -1:
            root_disp = ' \u2139'
        elif type(self.root) is int:
            root_disp = ' \u221a{}'.format(self.root)
        else:
            root_disp = ' \u221a({})'.format(self.root)

        representation = ' + '.join(
            ''.join(format(y) for y in x) \
            for x in zip(self.components, ['', root_disp]))

        return representation.replace(' + -', ' - ')\

    #=========================

    def __eq__(self, other):
        if type(other) in [int, float, Rational]:
            return self.real == other and self.imag == 0
        return self.signature == other.signature

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.norm() < other.norm()

    def __gt__(self, other):
        return self.norm() > other.norm()

    def __le__(self, other):
        return not (self > other)

    def __ge__(self, other):
        return not (self < other)

    #=========================

    def component_map(self, function, other=None):
        if other is not None:
            return Quadratic(*map(
                function,
                self.components,
                other.components
            ), self.root)

        return Quadratic(*map(function, self.components), self.root)

    #-------------------------

    def is_compatible(self, other):
        if type(other) is Quadratic and self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        return True

    #=========================

    def norm(self):
        return self.real**2 - self.root * self.imag**2

    #-------------------------

    def conjugate(self):
        return Quadratic(self.real, -self.imag, self.root)

    #-------------------------

    def mod_inverse(self, modulus):
        norm_inverse = mod_inverse(self.norm(), modulus)
        return (self.conjugate() * norm_inverse) % modulus

    #-------------------------

    def inverse(self, modulus=None):
        if modulus is not None:
            return self.mod_inverse(modulus)

        norm = self.norm()
        if abs(norm) == 1:
            norm_inverse = norm
        else:
            norm_inverse = frac(norm).inverse()

        return self.conjugate().component_map(lambda x: x * norm_inverse)

    #=========================

    def to_rational_approx(self, num_digits=None):
        imag_sign = 1 - 2 * (self.imag < 0)
        return frac(self.real) + \
                imag_sign * frac(self.imag**2 * self.root).sqrt(num_digits)

    def __neg__(self):
        return self.component_map(lambda x: -x)

    def __int__(self):
        return int(self.to_rational_approx())

    def floor(self):
        return self.component_map(int)

    def round(self):
        return self.component_map(round_down)

    def __float__(self):
        return float(self.to_rational_approx())

    def decimal(self, num_digits=None):
        return self.to_rational_approx(num_digits).decimal(num_digits)

    #=========================

    def __add__(self, other):
        self.is_compatible(other)
        if type(other) is not Quadratic:
            return Quadratic(self.real + other, self.imag, self.root)

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
        self.is_compatible(other)
        if type(other) is not Quadratic:
            return self.component_map(lambda x: x * other)

        real = (self.real * other.real) + (self.root * self.imag * other.imag)
        imag = (self.real * other.imag) + (self.imag * other.real)
        return Quadratic(real, imag, self.root)

    def __rmul__(self, other):
        return self * other

    #-------------------------

    def __truediv__(self, other):
        if type(other) is not Quadratic:
            return self * frac(other).inverse()

        return self * other.inverse()

    def __rtruediv__(self, other):
        return Quadratic(other, 0, self.root) / self

    #-------------------------

    def __floordiv__(self, other):
        if type(other) is int:
            return self.component_map(lambda x: x // other)

        return (self / other).round()

    def __rfloordiv__(self, other):
        return Quadratic(other, 0, self.root) // self

    #-------------------------

    def __pow__(self, other, modulus=None):
        if other < 0:
            return_val = pow(self.inverse(modulus), -other, modulus)
        elif other == 0:
            return_val = Quadratic(1, 0, self.root)
        elif other == 1:
            return_val = self
        elif other % 2 == 0:
            return_val = pow(self * self, other // 2, modulus)
        else:
            return_val = self * pow(self * self, other // 2, modulus)

        if modulus is not None:
            return return_val % modulus

        return return_val

    #-------------------------
    
    def __mod__(self, other):
        if type(other) is int:
            return self.component_map(lambda x: x % other)

        return self - other * (self // other)

    def __rmod__(self, other):
        return Quadratic(other, 0, self.root) % self

    #=========================

    def canonical(self):
        if self.root != -1:
            raise ValueError('No canonical form given')

        canon = self
        if abs(self.real) < abs(self.imag):
            canon = self * Quadratic(0, 1, -1)
        if self.real == -self.imag:
            canon = self * Quadratic(0, -1, -1)
        if canon.real < 0:
            canon = -canon

        return canon

    #-------------------------

    def gcd(self, other):
        self.is_compatible(other)
        if type(other) is not Quadratic:
            other = Quadratic(other, 0, self.root)

        a, b = self, other
        while b.components != (0, 0):
            a, b = b, a % b

        return a.canonical()

