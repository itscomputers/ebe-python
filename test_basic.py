#   test_basic.py

from hypothesis import given, assume, strategies as st
from itertools import product
import math

from numth.basic import *

@given(
    st.integers(),
    st.integers().filter(lambda x: x != 0)
)
def test_div(a, b):
    q, r = div(a, b)
    assert( 0 <= r < abs(b) )
    assert( a == q * b + r )

#-----------------------------

@given(
    st.integers(),
    st.integers().filter(lambda x: x != 0)
)
def test_div_with_small_remainder(a, b):
    q, r = div_with_small_remainder(a, b)
    assert( -abs(b) / 2 < r <= abs(b) / 2 )
    assert( a == q * b + r )

#-----------------------------

@given(
    st.integers(),
    st.integers()
)
def test_gcd(a, b):
    assume( a != 0 or b != 0)
    d = gcd(a, b)
    assert( a % d == b % d == 0 )
    assert( gcd(a//d, b//d) == 1 )

#-----------------------------

@given(
    st.integers(),
    st.integers()
)
def test_lcm(a, b):
    assume( a != 0 and b != 0 )
    m = lcm(a, b)
    assert( m % a == m % b == 0 )
    assert( gcd(m//a, m//b) == 1 )

#-----------------------------

@given(
    st.integers(),
    st.integers()
)
def test_bezout(a, b):
    assume( a != 0 or b != 0 )
    x, y = bezout(a, b)
    d = gcd(a, b)
    assert( a*x + b*y == d )

#-----------------------------

@given(
    number = st.integers().filter(lambda x: x != 0),
    base = st.integers(min_value=2)
)
def test_padic(number, base):
    exp, rest = padic(number, base)
    assert( number == base**exp * rest )
    assert( rest % base != 0 )

#-----------------------------

@given(st.integers(min_value=0))
def test_integer_sqrt(number):
    s = integer_sqrt(number)
    assert( s**2 <= number < (s+1)**2 )

#-----------------------------

@given(st.integers())
def test_is_square(number):
    assert( is_square(number**2) )

#-----------------------------

@given(
    number = st.integers(),
    modulus = st.integers(min_value=2)
)
def test_mod_inverse(number, modulus):
    assume( gcd(number, modulus) == 1 )
    inverse = mod_inverse(number, modulus)
    assert( 0 < inverse < modulus )
    assert( (number * inverse) % modulus == 1 )

#-----------------------------

@given(
    number = st.integers(),
    exponent = st.integers(max_value=-1),
    modulus = st.integers(min_value=2)
)
def test_mod_power(number, exponent, modulus):
    assume( gcd(number, modulus) == 1 )
    value = mod_power(number, exponent, modulus)
    inverse = mod_power(number, -exponent, modulus)
    assert( mod_inverse(value, modulus) == inverse )
    assert( mod_power(number, 0, modulus) == 1 )

#-----------------------------

@given(st.integers())
def test_jacobi(a):
    for p in [
            3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
            47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        if gcd(a, p) == 1:
            assert( jacobi(a, p) == euler_criterion(a, p) ) 

