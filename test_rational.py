#   test_rational.py
#===========================================================
from fractions import Fraction
import math
from hypothesis import given, assume, strategies as st

from numth.rational import *
#===========================================================

def test_decimal():
    a = 12837465999
    r = Rational(a, 10000000000)
    expected = [
        '1',
        '1.3',
        '1.28',
        '1.284',
        '1.2837',
        '1.28375',
        '1.283747',
        '1.2837466',
        '1.28374660',
        '1.283746600',
        '1.2837465999'
    ]
    for digits, decimal in enumerate(expected):
        assert( r.decimal(digits) == decimal )

#=============================

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0)
)
def test_int(numer, denom):
    r = Rational(numer, denom)
    int_r = int(r)
    assert( int_r <= r < int_r + 1 )

#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0)
)
def test_round(numer, denom):
    r = Rational(numer, denom)
    round_r = round(r)
    assert( round_r == int(r + Rational(1, 2)) )
    assert( True )

#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0)
)
def test_neg(numer, denom):
    r = Rational(numer, denom)
    f = Fraction(numer, denom)
    assert( -r == -f )
    assert( r == -(-r) )

#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0)
)
def test_abs(numer, denom):
    r = Rational(numer, denom)
    f = Fraction(numer, denom)
    assert( abs(r) == abs(f) )
    if r < 0:
        assert( abs(r) == -r )
    else:
        assert( abs(r) == r )

#-----------------------------

@given(
    numer = st.integers().filter(lambda x: x != 0),
    denom = st.integers().filter(lambda x: x != 0)
)
def test_inverse(numer, denom):
    r = Rational(numer, denom)
    assert( r == r.inverse().inverse() )
    assert( r * r.inverse() == 1 )

#=============================

@given(
    numer1 = st.integers(),
    denom1 = st.integers().filter(lambda x: x != 0),
    numer2 = st.integers(),
    denom2 = st.integers().filter(lambda x: x != 0)
)
def test_add(numer1, denom1, numer2, denom2):
    r1 = Rational(numer1, denom1)
    r2 = Rational(numer2, denom2)
    f1 = Fraction(numer1, denom1)
    f2 = Fraction(numer2, denom2)
    s = Rational(numer1*denom2 + denom1*numer2, denom1*denom2)
    assert( r1 + r2 == f1 + f2 )
    assert( r1 + r2 == s )
    assert( r2 + r1 == s )
    r1 += r2
    assert( r1 == s )

#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0),
    integer = st.integers()
)
def test_add_rational_and_integer(numer, denom, integer):
    r = Rational(numer, denom)
    s = Rational(numer + integer*denom, denom)
    assert( r + integer == s )
    assert( integer + r == s )
    r += integer
    assert( r == s )

#=============================

@given(
    numer1 = st.integers(),
    denom1 = st.integers().filter(lambda x: x != 0),
    numer2 = st.integers(),
    denom2 = st.integers().filter(lambda x: x != 0)
)
def test_sub(numer1, denom1, numer2, denom2):
    r1 = Rational(numer1, denom1)
    r2 = Rational(numer2, denom2)
    f1 = Fraction(numer1, denom1)
    f2 = Fraction(numer2, denom2)
    s = Rational(numer1*denom2 - denom1*numer2, denom1*denom2)
    assert( r1 - r2 == f1 - f2 )
    assert( r1 - r2 == s )
    assert( r2 - r1 == -s )
    r1 -= r2
    assert( r1 == s )

#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0),
    integer = st.integers()
)
def test_sub_rational_and_integer(numer, denom, integer):
    r = Rational(numer, denom)
    s = Rational(numer - integer*denom, denom)
    assert( r - integer == s )
    assert( integer - r == -s )
    r -= integer
    assert( r == s )

#=============================

@given(
    numer1 = st.integers(),
    denom1 = st.integers().filter(lambda x: x != 0),
    numer2 = st.integers(),
    denom2 = st.integers().filter(lambda x: x != 0)
)
def test_mul(numer1, denom1, numer2, denom2):
    r1 = Rational(numer1, denom1)
    r2 = Rational(numer2, denom2)
    f1 = Fraction(numer1, denom1)
    f2 = Fraction(numer2, denom2)
    numer = numer1 * numer2
    denom = denom1 * denom2
    d = gcd(numer, denom)
    s = Rational(numer//d, denom//d)
    assert( r1 * r2 == f1 * f2 )
    assert( r1 * r2 == s )
    assert( r2 * r1 == s )
    r1 *= r2
    assert( r1 == s )

#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0),
    integer = st.integers()
)
def test_mul_rational_and_integer(numer, denom, integer):
    r = Rational(numer, denom)
    d = gcd(integer, denom)
    s = Rational(numer * (integer//d), denom//d)
    assert( r * integer == s )
    assert( integer * r == s )
    r *= integer
    assert( r == s )

#=============================

@given(
    numer1 = st.integers().filter(lambda x: x != 0),
    denom1 = st.integers().filter(lambda x: x != 0),
    numer2 = st.integers().filter(lambda x: x != 0),
    denom2 = st.integers().filter(lambda x: x != 0)
)
def test_div(numer1, denom1, numer2, denom2):
    r1 = Rational(numer1, denom1)
    r2 = Rational(numer2, denom2)
    f1 = Fraction(numer1, denom1)
    f2 = Fraction(numer2, denom2)
    numer = numer1 * denom2
    denom = denom1 * numer2
    d = gcd(numer, denom)
    s = Rational(numer//d, denom//d)
    assert( r1 / r2 == f1 / f2 )
    assert( r1 / r2 == s )
    assert( r2 / r1 == s.inverse() )
    r1 /= r2
    assert( r1 == s )

#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0),
    integer = st.integers()
)
def test_div_rational_and_integer(numer, denom, integer):
    r = Rational(numer, denom)
    d = gcd(integer, denom)
    s = Rational(numer * (integer//d), denom//d)
    assert( r * integer == s )
    assert( integer * r == s )
    r *= integer
    assert( r == s )

#=============================

#@given(
#    numer = st.integers().filter(lambda x: x != 0),
#    denom = st.integers().filter(lambda x: x != 0),
#    integer = st.integers(min_value=0, max_value=15)
#)
#def test_pow(numer, denom, integer):
#    r = Rational(numer, denom)
#    f = Fraction(numer, denom)
#    s = Rational(numer**integer, denom**integer)
#    assert( r**integer == f**integer )
#    assert( r**integer == s )
#    assert( r**(-integer) == s.inverse() )
#    r **= integer
#    assert( r == s )
    
#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0),
    modulus = st.integers(min_value=2)
)
def test_mod(numer, denom, modulus):
    assume( gcd(denom, modulus) == 1 )
    r = Rational(numer, denom)
    s = (numer * mod_inverse(denom, modulus)) % modulus
    assert( r % modulus == s )
    r %= modulus
    assert( r == s )

#-----------------------------

@given(
    numer1 = st.integers(),
    denom1 = st.integers().filter(lambda x: x != 0),
    numer2 = st.integers(),
    denom2 = st.integers().filter(lambda x: x != 0),
    num_digits = st.integers(min_value=0, max_value=30)
)
def test_approx_equal(numer1, denom1, numer2, denom2, num_digits):
    r = Rational(numer1, denom1)
    rr = Rational(numer2, denom2)
    in_range = abs(r - rr) < Rational(1, 10**num_digits)
    assert( r.approx_equal(rr, num_digits) == in_range )

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0),
    integer = st.integers(),
    num_digits = st.integers(min_value=0, max_value=30)
)
def test_approx_equal_2(numer, denom, integer, num_digits):
    r = Rational(numer, denom)
    delta = Rational(integer, 10**(num_digits + 1))
    in_range = abs(delta) < Rational(1, 10**(num_digits))
    assert( r.approx_equal(r + delta, num_digits) == in_range )

#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers().filter(lambda x: x != 0)
)
def test_is_square(numer, denom):
    r = Rational(numer, denom)
    assert( (r**2).is_square() )

#-----------------------------

#@given(
#    numer = st.integers(min_value=0),
#    denom = st.integers(min_value=1),
#    num_digits = st.integers(min_value=10, max_value=30)
#)
#def test_sqrt(numer, denom, num_digits):
#    r = Rational(numer, denom)
#    s = r.sqrt(num_digits)
#    lhs = 10**num_digits * abs(r - s**2)
#    rhs = s + int(s) + 1
#
#    assert( lhs < rhs )

#-----------------------------

@given(
    number = st.integers()
)
def test_int_to_rational(number):
    assert( int(frac(number)) == number )

#-----------------------------

@given(
    number = st.floats()#.filter(lambda x: x != inf)
)
def test_float_to_rational(number):
    assume( str(number) not in ['inf', 'nan', '-inf'] )
    assert( float(frac(number)) == number )

#-----------------------------

@given(
    numer = st.integers(),
    denom = st.integers(min_value=1)
)
def test_str_to_rational(numer, denom):
    r = Rational(numer, denom)
    f1 = '{}/{}'.format(numer, denom)
    f2 = '{} / {}'.format(numer, denom)
    assert( frac(f1) == frac(f2) == r )
    
