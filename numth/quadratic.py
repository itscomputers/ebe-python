
#   numth/quadratic.py

import numth.numth as numth
import numth.rational as rational

############################################################
############################################################
#       Quadratic ring class
############################################################
############################################################

class Quadratic:
    """
    Quadratic integer class.

    Args:   int:            real, imag, root, mod
            str:            ring        'Z'  <- integer
                                        'Q'  <- rational
    
    Return: QuadraticInt:   real + imag * sqrt(root)
    """
    def __init__(self, real, imag, root, ring=None):
        """Initialize quadratic element."""
        if ring is None:
            self.rational = False
            self.mod = None
        if ring == 'Q':
            self.rational = True
            self.mod = None
        elif isinstance(ring, int) and ring > 1:
            self.rational = True
            self.mod = ring
        else:
            raise ValueError('Invalid RING')
        self.real = self.r(real)
        self.imag = self.r(imag)
        self.root = self.r(root)
        self.ring = ring

    ##########################

    def __repr__(self):
        """Print quadratic integer."""
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

    def r(num):
        if self.mod is not None:
            return num % self.mod
        elif self.rational:
            return rational.frac(num)
        else:
            return num

    ##########################

    def norm(self):
        """Norm of quadratic integer."""
        return self.r(self.real**2 - self.root * self.imag**2)

    ##########################

    def conjugate(self):
        """Conjugate of quadratic integer."""
        return Quadratic(self.real, -self.imag, self.root, self.ring)

    ##########################

    def inverse(self):
        """Inverse of quadratic integer."""
        norm = self.r(self.norm())
        norm_inverse = None
        if self.ring is None and norm in [1, -1]:
            norm_inverse = norm.inverse()
        elif self.rational and norm != 0:
            norm_inverse = norm
        elif self.mod and numth.gcd(norm, self.mod) == 1:
            norm_inverse = mod_inverse(norm, self.mod)
        
        if norm_inverse is None:
            raise ValueError('Not invertible')
        
        return self.r(self.conjugate() * norm_inverse)

    ##########################

    def __neg__(self):
        return Quadratic(-self.real, -self.imag, self.root, self.ring)

    ##########################

    def __add__(self, other):
        if isinstance(other, int):
            other = Quadratic(other, 0, self.root, self.ring)
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        new_real = self.real + other.real
        new_imag = self.imag + other.imag
        return QuadraticInt(new_real, new_imag, self.root, self.ring)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        if isinstance(other, int):
            other = Quadratic(other, 0, self.root, self.ring)
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        return -other + self 

    def __rsub__(self, other):
        return other - self

    def __isub__(self, other):
        return self - other

    ##########################

    def __mul__(self, other):
        if isinstance(other, int):
            other = Quadratic(other, 0, self.root, self.ring)
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        new_real = self.real * other.real + self.root * self.imag * other.imag
        new_imag = self.real * other.imag + self.imag * other.real
        return Quadratic(new_real, new_imag, self.root, self.ring)

    def __rmul__(self, other):
        return self * other 
        
    def __imul__(self, other):
        return self * other

    ##########################

    def __truediv__(self, other):
        if self.ring is None:
            if isinstance(other, int):
                other = Quadratic(other, 0, self.root, self.ring)

            if self.root != other.root:
                raise ValueError('Incompatible quadratic integers')
            
            other_norm = other.norm()
            if numth.gcd(self.real, self.imag) % other_norm == 0:
                return (self * other.conjugate()) / other_norm
            raise ValueError('{} not divisible by {}'.format(self, other))

        else:
            if not isinstance(other, Quadratic):
                other = Quadratic(other, 0, self.root, self.ring)
            return self * other.inverse() 

    def __rtruediv__(self, other):
        return Quadratic(other, 0, self.root, self.ring) / self

    def __itruediv__(self, other):
        return self / other

    ##########################

    def __floordiv__(self, other):
        if self.mod:
            return self / other

        if self.rational:
            div = self / other
            new_real = int(div.real)
            new_imag = int(div.imag)
            return Quadratic(new_real, new_imag, self.root, self.ring)

        if isinstance(other, int):
            new_real = self.real // other
            new_imag = self.imag // other
            return Quadratic(new_real, new_imag, self.root, self.ring)

        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        other_norm = other.norm()
        return (self * other.conjugate()) // other_norm

    def __rfloordiv__(self, other):
        return Quadratic(other, 0, self.root, self.ring) // self

    def __ifloordiv__(self, other):
        return self // other

    ##########################

    def __pow__(self, other):
        if other < 0:
            return self.inverse()**other
        elif other == 0:
            return Quadratic(1, 0, self.root, self.ring)
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
            return Quadratic(new_real, new_imag, self.root, self.ring)

    def __rmod__(self, other):
        return QuadraticInt(other, 0, self.root, self.ring) % self

    def __imod__(self, other):
        return self % other

    ##########################

    def __eq__(self, other):
        return      self.real == other.real\
                and self.imag == other.imag\
                and self.root == other.root

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

def quad(real, imag, root, ring):
    """Shortcut for creating instance of Quadratic class."""
    return QuadraticInt(real, imag, root, ring)

############################################################
