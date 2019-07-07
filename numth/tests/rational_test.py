#   test_rational.py
#===========================================================
from fractions import Fraction
import math
from hypothesis import given, assume, strategies as st

from ..basic import gcd, mod_inverse
from ..types import frac, Rational
#===========================================================

def coords(flag=None):
    if flag == 'nonzero':
        return [st.integers().filter(lambda x: x != 0),
                st.integers(min_value=1)]
    if flag == 'positive':
        return [st.integers(min_value=0), st.integers(min_value=1)]
    return [st.integers(), st.integers(min_value=1)]

#=============================

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
        '1.2837465999',
        '1.28374659990'
    ]
    for digits, decimal in enumerate(expected):
        assert( r.decimal(digits) == decimal )

#=============================

@given(st.integers(), st.integers(max_value=-1))
def test_negative_denominator(numer, denom):
    r = Rational(numer, denom)
    assert( r.numer * numer <= 0 )
    assert( r.denom > 0 )

#-----------------------------

@given(*coords())
def test_int(numer, denom):
    r = Rational(numer, denom)
    int_r = int(r)
    assert( int_r <= r < int_r + 1 )

#-----------------------------

@given(*coords())
def test_round(numer, denom):
    r = Rational(numer, denom)
    round_r = round(r)
    assert( round_r == int(r + Rational(1, 2)) )
    assert( True )

#-----------------------------

@given(*coords())
def test_neg(numer, denom):
    r = Rational(numer, denom)
    f = Fraction(numer, denom)
    assert( -r == -f )
    assert( r == -(-r) )

#-----------------------------

@given(*coords())
def test_abs(numer, denom):
    r = Rational(numer, denom)
    f = Fraction(numer, denom)
    assert( abs(r) == abs(f) )
    if r < 0:
        assert( abs(r) == -r )
    else:
        assert( abs(r) == r )

#-----------------------------

@given(*coords('nonzero'))
def test_inverse(numer, denom):
    r = Rational(numer, denom)
    assert( r == r.inverse().inverse() )
    assert( r * r.inverse() == 1 )

#=============================

@given(*coords(), *coords())
def test_add(numer1, denom1, numer2, denom2):
    r1 = Rational(numer1, denom1)
    r2 = Rational(numer2, denom2)
    f1 = Fraction(numer1, denom1)
    f2 = Fraction(numer2, denom2)
    s = Rational(numer1*denom2 + denom1*numer2, denom1*denom2)
    assert( r1 + r2 == f1 + f2 )
    assert( r1 + r2 == s )
    assert( r2 + r1 == s )

#-----------------------------

@given(*coords(), st.integers())
def test_add_rational_and_integer(numer, denom, integer):
    r = Rational(numer, denom)
    s = Rational(numer + integer*denom, denom)
    assert( r + integer == s )
    assert( integer + r == s )

#=============================

@given(*coords(), *coords())
def test_sub(numer1, denom1, numer2, denom2):
    r1 = Rational(numer1, denom1)
    r2 = Rational(numer2, denom2)
    f1 = Fraction(numer1, denom1)
    f2 = Fraction(numer2, denom2)
    s = Rational(numer1*denom2 - denom1*numer2, denom1*denom2)
    assert( r1 - r2 == f1 - f2 )
    assert( r1 - r2 == s )
    assert( r2 - r1 == -s )

#-----------------------------

@given(*coords(), st.integers())
def test_sub_rational_and_integer(numer, denom, integer):
    r = Rational(numer, denom)
    s = Rational(numer - integer*denom, denom)
    assert( r - integer == s )
    assert( integer - r == -s )

#=============================

@given(*coords(), *coords())
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

#-----------------------------

@given(*coords(), st.integers())
def test_mul_rational_and_integer(numer, denom, integer):
    r = Rational(numer, denom)
    d = gcd(integer, denom)
    s = Rational(numer * (integer//d), denom//d)
    assert( r * integer == s )
    assert( integer * r == s )

#=============================

@given(*coords('nonzero'), *coords('nonzero'))
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

#-----------------------------

@given(*coords(), st.integers())
def test_div_rational_and_integer(numer, denom, integer):
    r = Rational(numer, denom)
    d = gcd(integer, denom)
    s = Rational(numer * (integer//d), denom//d)
    assert( r * integer == s )
    assert( integer * r == s )

#=============================

@given(*coords('nonzero'), st.integers(min_value=0, max_value=15))
def test_pow(numer, denom, exponent):
    r = Rational(numer, denom)
    f = Fraction(numer, denom)
    s = Rational(numer**exponent, denom**exponent)
    assert( r**exponent == f**exponent )
    assert( r**exponent == s )
    assert( r**(-exponent) == s.inverse() )
    
#-----------------------------

@given(*coords(), st.integers(min_value=2))
def test_mod(numer, denom, modulus):
    assume( gcd(denom, modulus) == 1 )
    r = Rational(numer, denom)
    s = (numer * mod_inverse(denom, modulus)) % modulus
    assert( r % modulus == s )

#=============================

@given(*coords(), *coords(), st.integers(min_value=0, max_value=30))
def test_approx_equal(numer1, denom1, numer2, denom2, num_digits):
    r = Rational(numer1, denom1)
    rr = Rational(numer2, denom2)
    in_range = abs(r - rr) < Rational(1, 10**num_digits)
    assert( r.approx_equal(rr, num_digits) == in_range )

@given(*coords(), st.integers(), st.integers(min_value=0, max_value=30))
def test_approx_equal_2(numer, denom, integer, num_digits):
    r = Rational(numer, denom)
    delta = Rational(integer, 10**(num_digits + 1))
    in_range = abs(delta) < Rational(1, 10**(num_digits))
    assert( r.approx_equal(r + delta, num_digits) == in_range )

#=============================

@given(*coords('positive'), st.integers(min_value=10, max_value=20))
def test_sqrt(numer, denom, num_digits):
    r = Rational(numer, denom)
    s = r.sqrt(num_digits)
    lhs = 10**num_digits * abs(r - s**2)
    rhs = s + int(s) + 1

    assert( lhs < rhs )

#-----------------------------

@given(*coords('positive'))
def test_is_square(numer, denom):
    r = Rational(numer, denom)
    assert( (r**2).is_square() )

#=============================

@given(
    number = st.integers()
)
def test_int_to_rational(number):
    assert( int(frac(number)) == number )

#-----------------------------

@given(
    number = st.floats()
)
def test_float_to_rational(number):
    assume( str(number) not in ['inf', 'nan', '-inf'] )
    assert( float(frac(number)) == number )

#-----------------------------

@given(*coords())
def test_str_to_rational(numer, denom):
    r = Rational(numer, denom)
    f1 = '{}/{}'.format(numer, denom)
    f2 = '{} / {}'.format(numer, denom)
    assert( frac(f1) == frac(f2) == r )
    
