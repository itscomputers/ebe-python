
#   numth/quaternion.py

from numth.main import jacobi
from numth.quadratic import gaussian_divisor
from numth.rational import frac

from random import randint, shuffle

##############################

def quaternion_divisor(prime):
    if prime == 2 or prime % 4 == 1:
        d = gaussian_divisor(prime)
        r, i, j, k = d.real, d.imag, 0, 0

    elif prime % 8 == 3:
        s = pow(2, (prime+1)//4, prime)
        if 2 * s > prime:
            s = prime - s
        r, i, j, k = Quaternion(s, 1, 1, 0).descent(prime).components

    else:
        t = 2
        a = 5
        while jacobi(a, prime) == 1:
            t += 1
            a = pow(t, 2, prime) + 1
        s = pow(a, (prime+1)//4, prime)
        if 2 * s > prime:
            s = prime - s
        r, i, j, k = Quaternion(s, t, 1, 0).descent(prime).components

    return from_array(sorted([abs(r), abs(i), abs(j), abs(k)], reverse=True))

##############################

def from_array(arr):
    r, i, j, k = arr
    return Quaternion(r, i, j, k)

############################################################
############################################################
#       Quaternion class
############################################################
############################################################

class Quaternion:

    def __init__(self, r, i, j, k):
        self.r = r
        self.i = i
        self.j = j
        self.k = k
        self.components = (r, i, j, k)

    ##########################

    def __repr__(self):
        if self.i == 0 and self.j == 0 and self.k == 0:
            return format(self.r)
        else:
            terms = {'r' : self.r, 'i' : self.i, 'j' : self.j, 'k' : self.k}
            disp = []
            for x in ['r', 'i', 'j', 'k']:
                if terms[x] != 0:
                    if x == 'r':
                        disp.append(str(terms[x]))
                    else:
                        if terms[x] == 1:
                            disp.append(x)
                        elif terms[x] == -1:
                            disp.append('-' + x)
                        else:
                            disp.append('{} {}'.format(terms[x], x))
            disp = ' + '.join(disp)
            disp = disp.replace(' + -', ' - ')
            disp = disp.replace(' 1 ', ' ')
            return disp

    ##########################

    def norm(self):
        return self.r**2 + self.i**2 + self.j**2 + self.k**2

    ##########################

    def inverse(self):
        norm = self.norm()
        if abs(norm) == 1:
            norm_inverse = norm
        else:
            norm_inverse = frac(norm).inverse()
        r = self.r * norm_inverse
        i = self.i * norm_inverse
        j = self.j * norm_inverse
        k = self.k * norm_inverse
        return Quaternion(r, i, j, k)

    ##########################

    def conjugate(self):
        return Quaternion(self.r, -self.i, -self.j, -self.k)

    ##############################

    def descent(self, prime):
        m = self.norm() // prime
        if m == 1:
            return self
        else:
            return ((self.conjugate() * (self % m)) // m).descent(prime)

    ##########################

    def shuffle(self):
        components = list(self.components)
        shuffle(components)
        for i in range(4):
            components[i] *= (1 - 2*randint(0,1))
        return from_array(components)

    ##########################

    def __neg__(self):
        return Quaternion(-self.r, -self.i, -self.j, -self.k)

    ##########################

    def __add__(self, other):
        if not isinstance(other, Quaternion):
            other = Quaternion(other, 0, 0, 0)
        r = self.r + other.r
        i = self.i + other.i
        j = self.j + other.j
        k = self.k + other.k
        return Quaternion(r, i, j, k)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        if not isinstance(other, Quaternion):
            other = Quaternion(other, 0, 0, 0)
        return -other + self

    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        return self - other

    ##########################

    def __mul__(self, other):
        if not isinstance(other, Quaternion):
            other = Quaternion(other, 0, 0, 0)
        r = self.r*other.r - self.i*other.i - self.j*other.j - self.k*other.k
        i = self.r*other.i + self.i*other.r + self.j*other.k - self.k*other.j
        j = self.r*other.j - self.i*other.k + self.j*other.r + self.k*other.i
        k = self.r*other.k + self.i*other.j - self.j*other.i + self.k*other.r
        return Quaternion(r, i, j, k)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    ##########################

    def __truediv__(self, other):
        if not isinstance(other, Quaternion):
            other = Quaternion(other, 0, 0, 0)
        return self * other.inverse()

    def __rtruediv__(self, other):
        return self.inverse() * other

    def __itruediv__(self, other):
        return self / other

    ##########################

    def __floordiv__(self, other):
        if not isinstance(other, Quaternion):
            other = Quaternion(other, 0, 0, 0)
        norm = other.norm()
        new = self * other.conjugate()
        r = new.r // norm
        i = new.i // norm
        j = new.j // norm
        k = new.k // norm
        return Quaternion(r, i, j, k)

    def __rfloordiv__(self, other):
        if not isinstance(other, Quaternion):
            other = Quaternion(other, 0, 0, 0)
        return other // self

    def __ifloordiv__(self, other):
        return self // other

    ##########################

    def __pow__(self, other):
        if other < 0:
            return self**(-other)
        elif other == 0:
            return Quaternion(1,0,0,0)
        elif other == 1:
            return self
        elif other % 2 == 0:
            return (self * self)**(other//2)
        else:
            return self * (self * self)**(other//2)

    def __ipow__(self, other):
        return self**other

    ##########################

    def __mod__(self, other):
        if isinstance(other, Quaternion):
            return self - (self // other) * other
        elif isinstance(other, int):
            r = self.r % other
            i = self.i % other
            j = self.j % other
            k = self.k % other
            return Quaternion(
                r - other * (2*r > other), 
                i - other * (2*i > other), 
                j - other * (2*j > other), 
                k - other * (2*k > other))

    def __rmod__(self, other):
        if not isinstance(other, Quaternion):
            other = Quaternion(other)
        return other % self

    def __imod__(self, other):
        return self % other

    ##########################

    def __eq__(self, other):
        return  self.r == other.r\
            and self.i == other.i\
            and self.j == other.j\
            and self.k == other.k

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
############################################################
#       End
############################################################
############################################################
