
#   numth/quadratic.py

import numth.numth as numth

############################################################
############################################################
#       Quadratic integer class
############################################################
############################################################

class QuadraticInteger:
    """
    Quadratic integer class.

    Args:   int:                real, imag, root
    
    Return: QuadraticInteger:   real + imag * sqrt(root)
    """
    def __init__(self, real, imag, root):
        """Initialize quadratic integer."""
        self.real = real
        self.imag = imag
        self.root = root
    
    ##########################

    def __repr__(self):
        """Print quadratic integer."""
        return '{} + {} \u221A{}'.format(self.real, self.imag, self.root)

    ##########################

    def norm(self):
        """Norm of quadratic integer."""
        return self.real**2 - self.root * self.imag**2

    ##########################

    def conjugate(self):
        """Conjugate of quadratic integer."""
        return QuadraticInteger(self.real, -self.imag, self.root)

    ##########################

    def inverse(self):
        """Inverse of quadratic integer."""
        norm = self.norm()
        if norm == 1:
            return self.conjugate()
        elif norm == -1:
            return -self.conjugate()
        else:
            raise ValueError('Not invertible')

    ##########################

    def __neg__(self):
        return QuadraticInteger(-self.real, -self.imag, self.root)

    def __abs__(self):
        return self.norm()

    ##########################

    def __add__(self, other):
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        return QuadraticInteger(
                self.real + other.real, self.imag + other.imag, self.root )

    def __radd__(self, other):
        return self + QuadraticInteger(other, 0, self.root)

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        return QuadraticInteger(
                self.real - other.real, self.imag - other.imag, self.root )

    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        return self - other

    ##########################

    def __mul__(self, other):
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        new_real = self.real * other.real + self.root * self.imag * other.imag
        new_imag = self.real * other.imag + self.imag * other.real
        return QuadraticInteger(new_real, new_imag, self.root)

    def __rmul__(self, other):
        return QuadraticInteger(
                self.real * other, self.imag * other, self.root )
        
    def __imul__(self, other):
        return self * other

    ##########################

    def __truediv__(self, other):
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        other_norm = other.norm()
        if numth.gcd(self.real, self.imag) % other_norm != 0:
            raise ValueError('{} not divisible by {}'.format(self, other))
        return (self * other.conjugate()) / other_norm

    def __rtruediv__(self, other):
        return QuadraticInteger(
                self.real // other, self.imag // other, self.root )

    def __itruediv__(self, other):
        return self / other

    ##########################

    def __floordiv__(self, other):
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        other_norm = other.norm()
        return (self * other.conjugate()) / other_norm

    def __rfloordiv__(self, other):
        return self / other

    def __ifloordiv__(self, other):
        return self // other

    ##########################

    def __pow__(self, other):
        if other < 0:
            return self.inverse()**other
        elif other == 0:
            return QuadraticInteger(1, 0, self.root)
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
        return self - (self // other) * other

    def __rmod__(self, other):
        return QuadraticInteger(
                self.real % other, self.imag % other, self.root )

    def __imod__(self, other):
        return self % other

    ##########################

    def __eq__(self, other):
        return self.real == other.real\
                and self.imag == other.imag\
                and self.root == other.root

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.norm() < other.norm()

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        return self.norm() > other.norm()

    def __le__(self, other):
        return not self > other

############################################################

def quad(real, imag, root):
    """Shortcut for creating instance of QuadraticInteger class."""
    return QuadraticInteger(real, imag, root)
