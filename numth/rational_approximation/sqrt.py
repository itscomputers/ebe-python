#   numth/rational_approximation/sqrt.py
#===========================================================
from ..basic import integer_sqrt
from ..types import frac, Rational 
#===========================================================

def first_approximation(number, initial=None):
    if initial is None:
        return frac(integer_sqrt(number))
    return frac(initial)

#=============================

def babylonian_gen(number, initial=None):
    approx = first_approximation(number, initial)

    while True:
        yield approx
        approx = (approx + number / approx) / 2

#=============================

def halley_gen(number, initial=None):
    approx = first_approximation(number, initial)

    while True:
        yield approx
        approx = (approx + 8 * number * approx / (3 * approx**2 + number)) / 3

#=============================

def bakhshali_gen(number, initial=None):
    approx = first_approximation(number, initial)

    while True:
        yield approx
        a = (number / approx - approx) / 2
        b = approx + a
        approx = b - a**2 / (2 * b)

#=============================

def goldschmidt_gen(number, initial=None):
    b = number
    Y = first_approximation(number, initial)
    y = 1 / Y
    x = number * y

    while True:
        yield x, y
        b = b * Y**2
        Y = (3 - b) / 2
        x = x * Y
        y = y * Y

#=============================

def ladder_arithmetic_gen(number, initial=None):
    m = first_approximation(number, initial)
    m2 = m**2
    s0, s1 = 0, 1
    s = frac(0)
    
    while True:
        yield m + (number - m2) * s
        s = s.denom / ((number - m2) * s.numer + 2 * m * s.denom)

#=============================

def linear_fractional_transformation_gen(number, a, c):
    b = number * c
    approx = Rational(a, c)

    while True:
        yield approx
        approx = (a * approx + b) / (c * approx + a)

