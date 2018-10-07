
#   numth/polynomial.py

import itertools
import re
import numth.numth as numth

############################################################
############################################################
#       Polynomial class
############################################################
############################################################

class Polynomial:
    """
    Polynomial class with integer coefficients.

    Args:   tuple/list/int:     coeffs
            (int, ):            *rest

    Example:    for polynomial 1 + 2*x + 3*x^3, can use
                Polynomial(1,2,0,3) or 
                Polynomial((1,2,0,3)) or
                Polynomial([1,2,0,3])
    """
    def __init__(self, coeff, *rest):
        """Initialize polynomial."""
        if isinstance(coeff, tuple):
            self.coeffs = coeff
        elif isinstance(coeff, list):
            self.coeffs = tuple(coeff)
        else:
            self.coeffs = tuple([coeff] + list(rest))
        
        while (len(self.coeffs) > 1) and (self.coeffs[-1] == 0):
            self.coeffs = self.coeffs[:-1]
        
        if self.coeffs == (0,):
            self.deg = -1
        else:
            self.deg = len(self.coeffs) - 1
        
        if self.coeffs[-1] in [1, -1]:
            self.monic = True
        else:
            self.monic = False

    ##########################

    def __repr__(self):
        """Print polynomial."""
        if self.deg < 1:
            return format(self.coeffs[0])
        else:
            def term(coeff, power):
                if coeff == 0:
                    c, p = '', ''
                elif power == 0:
                    c, p = format(coeff), ''
                else:
                    if coeff == 1:
                        c = ''
                    elif coeff == -1:
                        c = '-'
                    else:
                        c = format(coeff)
                    if power == 1:
                        p = 'x'
                    else:
                        p = 'x^{}'.format(power)
                
                return '{} {}'.format(c, p)
            
            lowest_power = 0
            coeffs = self.coeffs
            while coeffs[0] == 0:
                lowest_power += 1
                coeffs = coeffs[1:]
            powers = itertools.count(lowest_power)
            result = ' + '.join(map(term, coeffs, powers))
            result = re.sub(' +', ' ', result)
            while '+ +' in result:
                result = re.sub('\+ \+', '+', result)
            result = re.sub('\+ \-', '- ', result)
            result = re.sub(' +', ' ', result)

            return result.strip()

    ##########################

    def eval(self, val):
        """
        Evaluate polynomial.

        Args:   int:    val
        
        Note:   val could actually be any type that supports arithmetic
        """
        powers = itertools.count(0)
        return sum(map(lambda c, p: c*v**p, self.coeffs, powers))

    ##########################

    def mod_eval(self, val, mod):
        """Soon deprecated"""
        def term(coeff, power):
            return (coeff * pow(val, power, mod)) % mod
        powers = itertools.count(0)
        return sum(map(term, self.coeffs, powers))
    
    ##########################

    def deriv(self, order=None):
        """
        Derivative of polyomial.

        Args:   int:        order     order of derivative to evaluate

        Return: Polynomial: derivative
        """
        if order == 0:
            return self
        if self.deg == 0:
            return Polynomial(0)

        powers = itertools.count(1)
        coeffs = self.coeffs[1:]
        diff = tuple(map(lambda c, p: c*p, coeffs, powers))

        if (order is None) or order == 1:
            return Polynomial(diff)
        else:
            return Polynomial(diff).deriv(order - 1)

    ##########################

    def gcd(self, other):
        """
        Greatest common divisor with another polynomial.

        Args:   Polynomial: other

        Return: Polynomial: largest degree polyn dividing self and other
        """
        if self.deg == -1 and other.deg == -1:
            raise ValueError('gcd(0,0) is undefined')
        if other.deg == -1:
            return abs(self)
        elif other.deg == 0:
            return 1
        else:
            return other.gcd(self % other)

    ##########################

    def __neg__(self):
        return Polynomial( tuple(map(lambda x: -x, self.coeffs)) )

    def __abs__(self):
        if self.coeffs[-1] < 0:
            return -self
        else:
            return self

    ##########################

    def __add__(self, other):
        if isinstance(other, int):
            other = Polynomial(other)
        self_other = list(itertools.zip_longest(
            self.coeffs, other.coeffs, fillvalue=0))
        return Polynomial( tuple(map(sum, self_other)) )

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        if isinstance(other, int):
            other = Polynomial(other)
        return -other + self

    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        return self - other

    ##########################

    def __mul__(self, other):
        if isinstance(other, int):
            other = Polynomial(other)
        def term(power):
            coeff = 0
            for i in range(min(power, self.deg) + 1):
                j = power - i
                if j < other.deg + 1:
                    coeff += self.coeffs[i] * other.coeffs[j]
            return coeff
        new_deg = self.deg + other.deg
        return Polynomial( tuple(term(i) for i in range(new_deg + 1)) )

    def __rmult__(self, other):
        return self * other

    def __imult__(self, other):
        return self * other

    ##########################

    def __floordiv__(self, other):
        if isinstance(other, int):
            other = Polynomial(other)
        if not other.monic:
            raise ValueError('Can only divide by monic polynomials')
        if self < other:
            return Polynomial(0)
        n = self
        d = other
        q = []
        while d <= n:
            coeff = n.coeffs[-1]
            power = n.deg - d.deg
            q = [coeff] + q
            new_coeffs = tuple([0] * power + [coeff])
            n = n - d * Polynomial(new_coeffs)
        return Polynomial( tuple(q) )

    def __rfloordiv__(self, other):
        if is isinstance(other, int):
            other = Polynomial(other)
        return other // self

    def __ifloordiv__(self, other):
        return self // other

    ##########################

    def __pow__(self, other):
        if other == 0:
            return Polynomial(1)
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
        """Maybe change this first case."""
        if isinstance(other, int):
            return Polynomial( tuple(map(lambda x: x % other, self.coeffs)) )
        else:
            return self - (self // other) * other

    def __imod__(self, other):
        return self % other

    ##########################

    def __eq__(self, other):
        return abs(self).coeffs == abs(other).coeffs

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.deg < other.deg

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        return self.deg > other.deg

    def __le__(self, other):
        return not self > other

############################################################

def polyn(*coeffs):
    """Shortcut for creating instance of Polynomial class."""
    return Polynomial(*coeffs)

############################################################
