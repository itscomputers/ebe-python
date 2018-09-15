
#   ~/itscomputers/rational_numbers.py

import number_theory as nt
import approximation as apx
import modular as mod
import primality as pr

############################################################    

class Rational:

    def __init__(self, numerator, denominator):
        d = nt.gcd(numerator, denominator)
        self.numerator = numerator // d
        self.denominator = denominator // d
        if self.denominator == 0:
            raise ValueError('Attempt to divide by zero')

    def __repr__(self):
        self.simplify()
        if self.denominator == 1:
            return '{}'.format(self.numerator)
        else:
            return '{}/{}'.format(\
                self.numerator,\
                self.denominator )

    ##########################

    def simplify(self):
        if self.numerator * self.denominator < 0:
            sgn = -1
        else:
            sgn = 1
        d = nt.gcd(self.numerator, self.denominator)
        self.numerator = sgn * abs(self.numerator) // d
        self.denominator = abs(self.denominator) // d
        return self

    def inverse(self):
        if self.numerator == 0:
            raise ValueError('Attempt to divide by zero')
        return Rational( self.denominator, self.numerator )

    ##########################

    def __add__(self, other):
        try:
            other = frac(other)
        except TypeError as e:
            return e
        d = nt.gcd(self.denominator, self.numerator)
        self_scalar = other.denominator // d
        other_scalar = self.denominator // d
        new_numerator =\
                self.numerator * self_scalar +\
                other.numerator * other_scalar
        new_denominator = (self.denominator // d) * other.denominator
        return Rational( new_numerator, new_denominator ).simplify()

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        try:
            other = frac(other)
        except TypeError as e:
            return e
        return self + Rational(-other.numerator, other.denominator)

    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        return self - other

    ##########################

    def __mul__(self, other):
        try:
            other = frac(other)
        except TypeError as e:
            return e
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator
        return Rational( new_numerator, new_denominator ).simplify()

    def __rmul__ (self, other):
        return self * other

    def __imul__(self, other):
        return self * other
    
    ##########################

    def __truediv__(self, other):
        if other.numerator == 0:
            raise ValueError('Attempt to divide by zero')
        try:
            other = frac(other)
        except TypeError as e:
            return e
        return self * other.inverse()

    def __rtruediv__(self, other):
        return self.inverse() * other

    def __itruediv__(self, other):
        return self / other

    ##########################

    def __neg__(self):
        return Rational( -self.numerator, self.denominator )

    def __abs__(self):
        return Rational( abs(self.numerator), self.denominator )

    ##########################

    def __pow__(self, other):
        if other == 0:
            if self.numerator == 0:
                raise ValueError('0**0 is undefined')
            else:
                return 1
        elif other > 0:
            return Rational( self.numerator**other, self.denominator**other )
        else:
            return Rational( self.denominator**-other, self.numerator**-other )

    def __ipow__(self, other):
        return self**other

    ##########################

    def __mod__(self, other):
        if nt.gcd(self.denominator, other) != 1:
            raise ValueError('Undefined')
        else:
            inv_denom = mod.inverse(self.denominator, other)
            return (self.numerator * inv_denom) % other

    def __imod__(self, other):
        return self % other

    ##########################

    def __eq__(self, other):
        try:
            other = frac(other)
        except TypeError as e:
            return e
        return (self.numerator * other.denominator) ==\
                (self.denominator * other.numerator)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        try:
            other = frac(other)
        except TypeError as e:
            return e
        return (self.numerator * other.denominator) <\
                (self.denominator * other.numerator)

    def __ge__(self, other):
        return not (self < other)

    def __gt__(self, other):
        try:
            other = frac(other)
        except TypeError as e:
            return e
        return (self.numerator * other.denominator) >\
                (self.denominator * other.numerator)

    def __le__(self, other):
        return not (self > other)

    ##########################

    def __int__(self):
        return self.numerator // self.denominator

    def __float__(self):
        return self.numerator / self.denominator

    def __round__(self):
        return int(self + .5)

    ##########################

    def decimal(self, num_digits=None):
        whole = self.numerator // self.denominator
        if num_digits == 0:
            return whole
        remainder = self.numerator % self.denominator
        frac = '.'
        if num_digits == None:
            num_digits = 20
        while len(frac) < num_digits:
            remainder *= 10
            next_digit = remainder // self.denominator
            frac += str(next_digit)
            remainder %= self.denominator
        remainder *= 10
        next_digit = remainder // self.denominator
        remainder %= self.denominator
        if 2*remainder >= self.denominator:
            next_digit += 1
        frac += str(next_digit)
        return str(whole) + frac

############################################################

def int_to_rational( integer ):
    return Rational(integer, 1)

def float_to_rational( fl ):
    whole, frac = str(fl).split('.')
    return Rational( int(whole + frac), 10**len(frac) )

def frac_to_rational( frac ):
    numerator, denominator = frac.split('/')
    return Rational( int(numerator), int(denominator) )

def repeating_decimal_to_rational( initial, repeat ):
    period = len(str(repeat))
    if '.' not in str(initial):
        displacement = 0
    else:
        displacement = len(str(initial).split('.')[-1])
    first = Rational(repeat, 10**(displacement + period))
    one_minus_r = int_to_rational(1) - Rational(1, 10**period)
    return float_to_rational(initial) + (first / one_minus_r)

def str_to_rational( string ):
    try:
        return frac_to_rational( string )
    except:
        pass
    try:
        return repeating_decimal_to_rational( string )
    except:
        pass
    try:
        return frac( float(str) )
    except:
        pass
    try:
        return frac( int(str) )
    except Exception as e:
        return e

def frac( a, b=None ):
    if b:
        return Rational(a, b)
    elif isinstance(a, Rational):
        return a
    elif isinstance(a, int):
        return int_to_rational( a )
    elif isinstance(a, float):
        return float_to_rational( a )
    elif isinstance(a, str):
        return str_to_rational( a )
    else:
        raise ValueError('Cannot convert to rational number')

############################################################

class Quadratic:

    def __init__(self, re, im, rt, ring=None, mod=None):
        if ring == None:
            self.re = re
            self.im = im
            self.rt = rt
            self.ring = ring
            self.mod = mod
        elif ring == 'Q':
            self.re = frac(re)
            self.im = frac(im)
            self.rt = frac(rt)
            self.ring = ring
            self.mod = mod
        elif ring == 'Mod':
            self.re = Mod(re, mod)
            self.im = Mod(im, mod)
            self.rt = Mod(rt, mod)
            self.ring = ring
            self.mod = mod

    def __repr__(self):
        if self.rt == -1:
            rt_disp = '\u2139'
        else:
            rt_disp = '\u221a' + str(self.rt)
        if self.im == 0:
            return '{}'.format(self.re)
        elif self.re == 0:
            return '{}'.format(self.im) + rt_disp
        elif self.im == 1:
            return '{} + '.format(self.re) + rt_disp
        elif self.im < 0:
            if self.im == -1:
                return '{} - '.format(self.re) + rt_disp
            else:
                return '{} - {} '.format(self.re, -self.im) + rt_disp
        else:
            return '{} + {} '.format(self.re, self.im) + rt_disp

    ##########################

    def conj(self):
        return Quadratic(\
                self.re,
                -self.im,
                self.rt,
                self.ring,
                self.mod    )

    def norm(self):
        return self.re**2 - self.im**2 * self.rt

    def inverse(self):
        return self.conj() / self.norm()

    ##########################

    def __add__(self, other):
        if isinstance(other, Quadratic):
            if other.rt != self.rt:
                raise ValueError('Non-matching quadratic types')
            return Quadratic(\
                    self.re + other.re,
                    self.im + other.im,
                    self.rt,
                    self.ring,
                    self.mod    )
        else:
            return Quadratic(\
                    self.re + other,
                    self.im,
                    self.rt,
                    self.ring,
                    self.mod    )

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        if isinstance(other, Quadratic):
            if other.rt != self.rt:
                raise ValueError('Non-matching quadratic types')
            return Quadratic(\
                    self.re - other.re,
                    self.im - other.im,
                    self.rt,
                    self.ring,
                    self.mod    )
        else:
            return Quadratic(\
                    self.re - other,
                    self.im,
                    self.rt,
                    self.ring,
                    self.mod    )

    def __rsub__(self, other):
        return Quadratic(\
                other - self.re,
                -self.im,
                self.rt,
                self.ring,
                self.mod    )

    def __isub__(self, other):
        return self + other

    ##########################

    def __mul__(self, other):
        if isinstance(other, Quadratic):
            if other.rt != self.rt:
                raise ValueError('Non-matching quadratic types')
            new_re = self.re * other.re + self.im * other.im * self.rt
            new_im = self.re * other.im + self.im * other.re
            return Quadratic(\
                    new_re,
                    new_im,
                    self.rt,
                    self.ring,
                    self.mod    )
        else:
            return Quadratic(\
                    other * self.re,
                    other * self.im,
                    self.rt,
                    self.ring,
                    self.mod    )

    def __rmul__(self, other):
        return Quadratic(\
                other * self.re,
                other * self.im,
                self.rt,
                self.ring,
                self.mod    )

    def __imul__(self, other):
        return self * other

    ##########################

    def __truediv__(self, other):
        if isinstance(other, Quadratic):
            if other.rt != self.rt:
                raise ValueError('Non-matching quadratic types')
            return self * other.inverse()
        else:
            return Quadratic(\
                    self.re / other,
                    self.im / other,
                    self.rt,
                    self.ring,
                    self.mod    )

    def __rtruediv__(self, other):
        return Quadratic(\
                other,
                0,
                self.rt,
                self.ring,
                self.mod    ) / self

    def __itruediv__(self, other):
        return self / other

    ##########################

    def __floordiv__(self, other):
        if isinstance(other, Quadratic):
            if other.rt != self.rt:
                raise ValueError('Non-matching quadratic types')
            return (self * other.conj()) // other.norm()
        else:
            return Quadratic(\
                    self.re // other,
                    self.im // other,
                    self.rt,
                    self.ring,
                    self.mod    )

    def __rfloordiv__(self, other):
        return Quadratic(\
                other,
                0,
                self.rt,
                self.ring,
                self.mod    ) // self

    def __ifloordiv__(self, other):
        return self // other

    ##########################

    def __pow__(self, exp):
        if exp == 0:
            return Quadratic(1, 0, self.rt)
        elif exp == 1:
            return self
        elif exp < 0:
            return (self.conj() / self.norm())**-exp
        elif exp % 2 == 0:
            return (self * self)**(exp//2) 
        else:
            return self * (self * self)**(exp//2)

    def __ipow__(self, exp):
        return self**exp

    ##########################

    def __mod__(self, other):
        return Quadratic(\
                self.re % other,
                self.im % other,
                self.rt,
                self.ring,
                self.mod    )

    def __imod__(self, other):
        return self % other

    ##########################

    def __neg__(self):
        return Quadratic(
                -self.re,
                -self.im,
                self.rt,
                self.ring,
                self.mod    )

    def __abs__(self):
        return self.norm()

    ##########################

    def __eq__(self, other):
        if not isinstance(other, Quadratic):
            other = Quadratic(other, 0, self.rt, self.ring, self.mod)
        return (self.re == other.re)\
                and (self.im == other.im)\
                and (self.rt == other.rt)

    def __ne__(self, other):
        return not (self == other)
    
    def __gt__(self, other):
        if isinstance(other, Quadratic):
            other_norm = other.norm()
        else:
            other_norm = other**2
        return self.norm() > other_norm

    def __le__(self, other):
        return not (self > other)

    def __lt__(self, other):
        if isinstance(other, Quadratic):
            other_norm = other.norm()
        else:
            other_norm = other**2
        return self.norm() < other_norm

    def __ge__(self, other):
        return not (self < other)

############################################################

class Mod:

    def __init__(self, elem, mod):
        self.mod = mod
        self.elem = elem % self.mod

    def __repr__(self):
        return str( self.elem )

    ##########################

    def reduce(self):
        return self.elem % self.mod

    def inverse(self):
        return mod.inverse(self.elem, self.mod)

    ##########################

    def __int__(self):
        return self.elem

    ##########################

    def __add__(self, other):
        if not isinstance(other, Mod):
            other = Mod(other, self.mod)
        return (self.elem + other.elem) % self.mod

    def __radd__(self, other):
        if not isinstance(other, Mod):
            other = Mod(other, self.mod)
        return (self.elem + self.other) % self.mod

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        if not isinstance(other, Mod):
            other = Mod(other, self.mod)
        return (self.elem - other.elem) % self.mod

    def __rsub__(self, other):
        if not isinstance(other, Mod):
            other = Mod(other, self.mod)
        return (other.elem - self.elem) % self.mod

    def __isub__(self, other):
        return self - other

    ##########################

    def __mul__(self, other):
        if not isinstance(other, Mod):
            other = Mod(other, self.mod)
        return (self.elem * other.elem) % self.mod

    def __rmul__(self, other):
        if not isinstance(other, Mod):
            other = Mod(other, self.mod)
        return (self.elem * other.elem) % self.mod

    def __imul__(self, other):
        return self * other

    ##########################

    def __truediv__(self, other):
        if not isinstance(other, Mod):
            other = Mod(other, self.mod)
        return self * (other.inverse())
    
    def __rtruediv__(self, other):
        if not isinstance(other, Mod):
            other = Mod(other, self.mod)
        return self.inverse() * other

    def __itruediv__(self, other):
        return self / other

    ##########################

    def __pow__(self, exp):
        if exp < 0:
            return self.elem**(-exp)
        elif exp == 0:
            return 1
        elif exp == 1:
            return self.elem
        elif (exp % 2):
            return self.elem * (self.elem * self.elem)**(exp//2) % self.mod
        else:
            return (self.elem * self.elem)**(exp//2) % self.mod

    def __ipow__(self, exp):
        return self**exp

    ##########################

    def __mod__(self, other):
        return self.elem % int(other)

    def __imod__(self, other):
        return self.elem % other

    ##########################

    def __neg__(self):
        return (-self.elem) % self.mod

    def __abs__(self):
        return self.elem

    ##########################

    def __eq__(self, other):
        if not isinstance(other, Mod):
            other = Mod(other, self.mod)
        return (self.elem == other.elem) and (self.mod == other.mod)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (abs(self) < abs(other))

    def __ge__(self, other):
        return not (self < other)

    def __gt__(self, other):
        return (abs(self) > abs(other))

    def __le__(self, other):
        return not (self > other)

############################################################

class FFp:

    def __init__(self, mod):
        if not pr.is_prime( mod ):
            raise ValueError('Modulus is not prime')
        else:
            self.mod = mod
            self.all = self.all_elem()
            self.star = self.inv_elem()

    def __repr__(self):
        return 'Finite field with {} elements'.format(self.mod)

    ##########################

    def elem(self, number):
        return Mod(number, self.mod)

    def all_elem(self):
        return [ self.elem(x) for x in range(0, self.mod) ]

    def inv_elem(self):
        return [ self.elem(x) for x in range(1, self.mod) ]

############################################################

class Zm:

    def __init__(self, mod):
        self.mod = mod
        self.all = self.all_elem()
        self.star = self.inv_elem()

    def __repr__(self):
        return 'Ring of integers modulo {}'.format(self.mod)

    ##########################

    def elem(self, number):
        return Mod(number, self.mod)

    def all_elem(self):
        return [ self.elem(x) for x in range(0, self.mod) ]

    def inv_elem(self):
        return mod.group( self.mod )

    def populate(self):
        self.all = self.all_elem()
        self.star = self.star()

###########################################################

class FFp2:

    def __init__(self, mod):
        if not pr.is_prime( mod ):
            raise ValueError('Modulus is not prime')
        else:
            self.mod = mod
            self.find_rt()
            self.all = self.all_elem()
            self.star = self.inv_elem()

    def __repr__(self):
        return 'Finite field with {} elements'.format((self.mod)**2)

    ##########################

    def find_rt(self):
        if self.mod % 4 == 3:
            self.rt = -1
        else:
            for rt in range(2, self.mod-1):
                if mod.jacobi(rt, self.mod) == -1:
                    self.rt = rt
                    break

    def elem(self, a, b):
        return Quadratic(a, b, self.rt, 'Mod', self.mod)

    def all_elem(self):
        all_elem = []
        for a in range(self.mod):
            for b in range(self.mod):
                all_elem.append( self.elem(a, b) )
        return all_elem

    def inv_elem(self):
        return [ x for x in self.all if x != 0 ]

