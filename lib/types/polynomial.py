#   lib/types/polynomial.py
#   - class for arithmetic of polynomials

#===========================================================
from collections import defaultdict
from functools import reduce
import re

from ..basic import gcd, lcm, mod_power
from .rational import frac, Rational
#===========================================================
__all__ = [
    'polyn',
    'Polynomial',
]
#===========================================================

def polyn(*inputs):
    """Shortcut to create Polynomial from string or tuple of coeffs"""
    if len(inputs) == 1 and type(*inputs) is str:
        return _string_to_polyn(*inputs)
    if type(inputs[0]) is tuple:
        return _tuples_to_polyn(*inputs)
    return _args_to_polyn(*inputs)

#-----------------------------

def polyn_div(a, b, coeff_type=int):
    """Polynomial division with remainder."""
    q = Polynomial({0: 0})
    r = a
    while b.degree <= r.degree:
        exp = r.degree - b.degree
        if coeff_type is int:
            coeff = r.leading_coeff // b.leading_coeff
        if coeff_type is Rational:
            coeff = frac(r.leading_coeff) / frac(b.leading_coeff)
        q = q + Polynomial({exp: coeff})
        r = r - b * Polynomial({exp: coeff})
    return (q, r)

#=============================


class Polynomial:

    """Polynomial class with polynomial arithmetic"""

    def __init__(self, coeffs):
        self.coeffs = {e : c for (e, c) in coeffs.items() \
            if type(e) is int and e >= 0 and c != 0}
        self.degree = self._degree()
        self.leading_coeff = self._leading_coeff()
        self.monic = self.leading_coeff == 1

    #-------------------------

    def __repr__(self):
        if self.coeffs == dict():
            return '0'
        representation = ' + '.join(
            _exp_coeff_to_term(e, c) \
            for (e, c) in sorted(self.coeffs.items())
        )

        return representation.replace(' + -', ' - ')

    #=========================

    def __eq__(self, other):
        return self.coeffs == other.coeffs

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.degree < other.degree

    def __gt__(self, other):
        return self.degree > other.degree

    def __ge__(self, other):
        return not (self < other)

    def __le__(self, other):
        return not (self > other)

    #=========================

    def _degree(self):
        if self.coeffs == dict():
            return -1
        return max(self.coeffs.keys())

    #-------------------------

    def _leading_coeff(self):
        if self.coeffs == dict():
            return 0
        return self.coeffs[self.degree]

    #-------------------------

    def _full_coeffs(self):
        return {**{e: 0 for e in range(self.degree)}, **self.coeffs}

    #-------------------------

    def _match_coeffs(self, other):
        return {**{e : 0 for e in other.coeffs.keys()}, **self.coeffs}

    #=========================

    def __neg__(self):
        return Polynomial({e : -c for (e, c) in self.coeffs.items()})

    #-------------------------

    def canonical(self):
        if self.leading_coeff < 0:
            return -self
        return self

    #-------------------------

    def to_integer_polyn(self):
        if self == Polynomial({0: 0}) \
                or type(list(self.coeffs.values())[0]) is int:
            return self

        m = lcm(*(c.denom for c in self.coeffs.values()))
        coeffs = {e: int(c * m) for (e, c) in self.coeffs.items()}

        return Polynomial(coeffs).canonical()

    #=========================

    def __add__(self, other):
        if type(other) is int:
            return self + polyn(other)
        self_coeffs = self._match_coeffs(other)
        other_coeffs = other._match_coeffs(self)
        return Polynomial({e: self_coeffs[e] + other_coeffs[e] \
            for e in self_coeffs.keys()})

    def __radd__(self, other):
        return self + other

    #=========================

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    #=========================

    def __mul__(self, other):
        if type(other) is int:
            return Polynomial({e: c * other for (e, c) in self.coeffs.items()})
        return reduce(
            lambda x, y: x + y,
            (Polynomial({e1 + e2: c1 * c2 for (e2, c2) in other.coeffs.items()}) \
                for (e1, c1) in self.coeffs.items()),
            Polynomial({0: 0})
        )

    def __rmul__(self, other):
        return self * other

    #=========================

    def __truediv__(self, other):
        if self == Polynomial({0: 0}):
            return self

        if type(other) is int:
            if gcd(*self.coeffs.values()) % other == 0:
                return self // other
            return Polynomial({e: Rational(c, other) \
                    for (e, c) in self.coeffs.items()})

        if other == Polynomial({0: 0}):
            raise ValueError('Attempted division by zero')

    #=========================

    def __floordiv__(self, other):
        if self == Polynomial({0: 0}):
            return self

        if type(other) is int:
            return Polynomial({e: c // other for (e, c) in self.coeffs.items()})

        if other == Polynomial({0: 0}):
            raise ValueError('Attempted division by zero')

        if gcd(*self.coeffs.values()) % other.leading_coeff == 0:
            return polyn_div(self, other, int)[0]

        return polyn_div(self, other, Rational)[0]

    def __rfloordiv__(self, other):
        if type(other) is int:
            return Polynomial({0: 0})

    #=========================

    def __pow__(self, other):
        if other < 0:
            if self.degree > 0:
                raise ValueError('Polynomial is not invertible')
            return frac(repr(self)).inverse()

        if other == 0:
            return Polynomial({0: 1})
        elif other == 1:
            return self
        elif other % 2 == 0:
            return (self * self) ** (other // 2)
        else:
            return self * (self * self) ** (other // 2)

    #=========================

    def __mod__(self, other):
        if type(other) is int:
            if other < 2:
                raise ValueError('Modulus must be at least 2')
            return Polynomial({e: c % other for (e, c) in self.coeffs.items()})

        if self == Polynomial({0: 0}):
            return self

        if gcd(*self.coeffs.values()) % other.leading_coeff == 0:
            return polyn_div(self, other, int)[1]

        return polyn_div(self, other, Rational)[1]

    #=========================

    def eval(self, value):
        return sum(map(lambda x: x[1] * value**x[0], self.coeffs.items()))

    #-------------------------

    def mod_eval(self, value, modulus):
        return sum(map(
            lambda x: (x[1] * mod_power(value, x[0], modulus)) % modulus,
            self.coeffs.items()))

    #-------------------------

    def derivative(self, order=None):
        if order == 0:
            return self
        if self.degree == 0:
            return Polynomial('0')

        deriv = Polynomial({e-1: e*c for (e, c) in self.coeffs.items()})

        if order is not None and order > 1:
            return deriv.derivative(order - 1)

        return deriv

#===========================================================

def _term_pattern():
    """Pattern for polynomial string term."""
    return re.compile(r'([\+\-]?\d*)?(\*?[A-Za-z])?(\^\d+)?')

#-----------------------------

def _term_to_exp_coeff(coeff, var, exp):
    """Extract exponent and coeff from string term."""
    try:
        _coeff = int(coeff)
    except ValueError:
        _coeff = int('{}1'.format(coeff))

    if var == '' or var is None:
        _exp = 0
    elif exp == '' or exp is None:
        _exp = 1
    else:
        _exp = int(exp[1:])

    return _exp, _coeff

#-----------------------------

def _exp_coeff_to_term(exponent, coeff):
    """Convert exponent and coeff to string term."""
    if exponent == 0:
        return '{}'.format(coeff)

    if abs(coeff) == 1:
        _coeff = format(coeff).replace('1', '')
    else:
        _coeff = '{}'.format(coeff)

    if exponent == 1:
        return '{}x'.format(_coeff)

    return '{}x^{}'.format(_coeff, exponent)

#=============================

def _string_to_polyn(string):
    """Convert string to polynomial."""
    coeffs = defaultdict(int)
    for term in _term_pattern().findall(''.join(string.split())):
        if term != ('', '', ''):
            exp, coeff = _term_to_exp_coeff(*term)
            coeffs[exp] += coeff
    return Polynomial(coeffs)

#-----------------------------

def _tuples_to_polyn(*tuples):
    """Convert list of tuples to polynomial."""
    coeffs = defaultdict(int)
    for (exp, coeff) in tuples:
        coeffs[exp] += coeff
    return Polynomial(coeffs)

#-----------------------------

def _args_to_polyn(*args):
    """Convert general coeffs to polynomial."""
    coeffs = {exp: coeff for (exp, coeff) in enumerate(args)}
    return Polynomial(coeffs)

