
#   numth/quadratic.py

from numth.main import mod_inverse 
from numth.rational import frac, sqrt 

############################################################
############################################################
#       Quadratic ring class
############################################################
############################################################

class Quadratic:
    """
    Quadratic integer class.

    Args:   int:            real, imag, root, mod
    
    Return: Quadratic:   real + imag * sqrt(root)  [optional: % mod]
    """
    def __init__(self, real, imag, root, mod=None):
        """Initialize quadratic element."""
        if (mod is not None) and (isinstance(mod, int) or mod < 2):
            raise ValueError('Invalid modulus')
        self.mod = mod
        self.real = self.r(real)
        self.imag = self.r(imag)
        self.root = self.r(root)

    ##########################

    def __repr__(self):
        """Print quadratic element."""
        if self.root == -1 or (self.mod and self.root == self.mod - 1):
            root_disp = '\u2139'
        else:
            root_disp = '\u221a{}'.format(self.root)
        
        if self.imag == 0:
            return format(self.real)
        elif self.real == 0:
            return '{} {}'.format(self.imag, root_disp)
        elif self.imag < 0:
            return '{} - {} {}'.format(self.real, -self.imag, root_disp)
        else:
            return '{} + {} {}'.format(self.real, self.imag, root_disp)

    ##########################

    def r(self, num):
        if self.mod is not None:
            return num % self.mod
        else:
            return num

    ##########################

    def norm(self):
        """Norm of quadratic element."""
        return self.r(self.real**2 - self.root * self.imag**2)

    ##########################

    def conjugate(self):
        """Conjugate of quadratic element."""
        return Quadratic(self.real, -self.imag, self.root, self.mod)

    ##########################

    def inverse(self):
        """Inverse of quadratic element."""
        norm = self.r(self.norm())
        if self.mod is not None:
            norm_inverse = mod_inverse(norm, self.mod)
        elif abs(norm) == 1:
            norm_inverse = norm
        else:
            norm_inverse = frac(norm).inverse()
        
        new_real = self.real * norm_inverse
        new_imag = -self.imag * norm_inverse
        return Quadratic(new_real, new_imag, self.root, self.mod)

    ##########################

    def __neg__(self):
        return Quadratic(-self.real, -self.imag, self.root, self.mod)

    def __int__(self):
        return int(self.real + self.imag * sqrt(self.root))

    def __float__(self):
        return float(self.real + self.imag * sqrt(self.root))

    def __round__(self):
        f = float(self)
        if f >= 0:
            return int(float(self) + .5)
        else:
            return int(float(self) - .5)

    ##########################

    def __add__(self, other):
        if isinstance(other, int):
            other = Quadratic(other, 0, self.root, self.mod)
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        new_real = self.real + other.real
        new_imag = self.imag + other.imag
        return Quadratic(new_real, new_imag, self.root, self.mod)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        if isinstance(other, int):
            other = Quadratic(other, 0, self.root, self.mod)
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        return -other + self 

    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        return self - other

    ##########################

    def __mul__(self, other):
        if not isinstance(other, Quadratic):
            other = Quadratic(other, 0, self.root, self.mod)
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        new_real = self.real * other.real + self.root * self.imag * other.imag
        new_imag = self.real * other.imag + self.imag * other.real
        return Quadratic(new_real, new_imag, self.root, self.mod)

    def __rmul__(self, other):
        return self * other 
        
    def __imul__(self, other):
        return self * other

    ##########################

    def __truediv__(self, other):
        if not isinstance(other, Quadratic):
            other = Quadratic(other, 0, self.root, self.mod)
        return self * other.inverse() 

    def __rtruediv__(self, other):
        return Quadratic(other, 0, self.root, self.mod) / self

    def __itruediv__(self, other):
        return self / other

    ##########################

    def __floordiv__(self, other):
        if self.mod:
            return self / other
        else:
            new = self / other
            new_real = int(new.real)
            new_imag = int(new.imag)
            return Quadratic(new_real, new_imag, self.root, self.mod)

    def __rfloordiv__(self, other):
        return Quadratic(other, 0, self.root, self.mod) // self

    def __ifloordiv__(self, other):
        return self // other

    ##########################

    def __pow__(self, other):
        if other < 0:
            return self.inverse()**other
        elif other == 0:
            return Quadratic(1, 0, self.root, self.mod)
        elif other == 1:
            return self
        elif other % 2 == 0:
            return (self * self)**(other // 2)
        else:
            return self * (self * self)**(other // 2)

    def __ipow__(self, other):
        return self**other

    ##########################

    def __mod__(self, other):
        if isinstance(other, Quadratic):
            return self - (self // other) * other

        if isinstance(other, int):
            new_real = self.real % other
            new_imag = self.imag % other
            return Quadratic(new_real, new_imag, self.root, self.mod)

    def __rmod__(self, other):
        return QuadraticInt(other, 0, self.root, self.mod) % self

    def __imod__(self, other):
        return self % other

    ##########################

    def __eq__(self, other):
        return      self.real == other.real\
                and self.imag == other.imag\
                and self.root == other.root\
                and self.mod  == other.mod

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.mod:
            raise ValueError('Comparison undefined in modular arithmetic')
        return self.norm() < other.norm()

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        if self.mod:
            raise ValueError('Comparison undefined in modular arithmetic')
        return self.norm() > other.norm()

    def __le__(self, other):
        return not self > other

############################################################

def quad(real, imag, root, mod=None):
    """Shortcut for creating instance of Quadratic class."""
    return Quadratic(real, imag, root, mod)

############################################################
