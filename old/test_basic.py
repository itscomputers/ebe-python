
#   test_basic.py

from hypothesis import given, assume, strategies as st
from itertools import product
import math

from new_numth.basic import *

@given(
    st.integers(),
    st.integers().filter(lambda x: x != 0)
    )
def test_div(a, b):
    q, r = div(a, b)
    assert( a == q * b + r )
    assert( 0 <= r < abs(b) )
    
    q, r = div(a, b, SMALL_REM=True)
    assert( a == q * b + r )
    assert( -abs(b) // 2 < r <= abs(b) // 2 )

@given(
    st.integers(),
    st.integers()
    )
def test_gcd(a, b):
    assume( a != 0 or b != 0 )
    d = gcd(a, b)
    assert( a % d == b % d == 0 )
    assert( gcd(a//d, b//d) == 1 )

@given(
    st.integers(),
    st.integers()
    )
def test_lcm(a, b):
    assume( a != 0 and b != 0 )
    m = lcm(a, b)
    assert( m % a == m % b == 0 )
    assert( gcd(m//a, m//b) == 1 )

@given(
    st.integers().filter(lambda x: x > 0),
    st.integers().filter(lambda x: x > 0)
    )
def test_bezout(a, b):
    x, y = bezout(a, b)
    d = gcd(a, b)
    assert( a*x + b*y == d )

@given(
    num=st.integers().filter(lambda x: x != 0),
    base=st.integers().filter(lambda x: x > 1)
    )
def test_padic(num, base):
    exp, rest = padic(num, base)
    assert( num == base**exp * rest )
    assert( rest % base != 0 )

@given(st.integers().filter(lambda x: x > 0))
def test_integer_sqrt(num):
    i = integer_sqrt(num)
    assert( i**2 <= num < (i+1)**2 )

@given(st.integers())
def test_is_square(num):
    assert( is_square(num**2) )

@given(st.integers().filter(lambda x: x > 0))
def test_sqrt(num):
    x = sqrt(num, 20)
    m = integer_sqrt(num)
    assert( 10**20 * abs(num - x**2) < m + 1 + x )

@given(
    num=st.integers(),
    mod=st.integers().filter(lambda x: x > 1)
    )
def test_mod_inverse(num, mod):
    assume( gcd(num, mod) == 1 )
    inv = mod_inverse(num, mod)
    assert( inv > 0 and inv < mod )
    assert( (num * inv) % mod == 1 )

@given(
    num=st.integers(),
    exp=st.integers().filter(lambda x: x < 0),
    mod=st.integers().filter(lambda x: x > 1)
    )
def test_mod_power(num, exp, mod):
    assume( gcd(num, mod) == 1 )
    answer = mod_power(num, exp, mod)
    inverse = pow(num, -exp, mod)
    assert( mod_inverse(answer, mod) == inverse )

@given(
    st.integers().filter(lambda x: 0 < abs(x) < 2**16),
    st.integers().filter(lambda x: 0 < abs(x) < 2**16),
    st.integers().filter(lambda x: x != 0)
    )
def test_rational(a, b, c):
    fla = a / 4
    flb = b / 5
    flc = 1. * c
    fra = frac(a, 4)
    frb = frac(flb)
    frc = frac(c)
    
    assert( fra + frb == frac(5*a + 4*b, 20) )
    assert( fra + frc == frac(a + 4*c, 4) )
    assert( frb + frc == frac(b + 5*c, 5) )

    assert( fra - frb == frac(5*a - 4*b, 20) )
    assert( fra - frc == frac(a - 4*c, 4) )
    assert( frb - frc == frac(b - 5*c, 5) )

    assert( fra * frb == frac(a*b, 20) )
    assert( fra * frc == frac(a*c, 4) )
    assert( frb * frc == frac(b*c, 5) )

    assert( fra / frb == frac(5*a, 4*b) )
    assert( fra / frc == frac(a, 4*c) )
    assert( frb / frc == frac(b, 5*c) )

    fl = [fla, flb, flc]
    fr = [fra, frb, frc]
    
    for frx in fr:
        assert( frx + c == frx + frc )
        assert( frx - c == frx - frc )
        assert( frx * c == frx * frc )
        assert( frx / c == frx / frc )
        assert( c + frx == frc + frx )
        assert( c - frx == frc - frx )
        assert( c * frx == frc * frx )
        assert( c / frx == frc / frx )

        assert( 3 * frx == frx * 3 == frx + frx + frx )
        assert( -3 * frx == -frx * 3 == -frx - frx - frx )
        assert( frx**3 == frx * frx * frx )
        assert( frx**(-3) == frx.inverse() * frx.inverse() * frx.inverse() )

        assert( frx.inverse() * frx == 1 )
        assert( 1 / frx == frx.inverse() )
        assert( frx / frx == 1 )
        assert( frx**7 / frx**6 == frx )
        assert( frx**3 * frx**4 == frx**7 )

        assert( abs(-frx) == abs(frx) )

    for (flx, frx) in zip(fl, fr):
        assert( float(frx) == flx )
        
    assert( int(fra) == a // 4 )
    assert( int(frb) == b // 5 )

    for (frx, fry) in product(fr, fr):
        assert( frx / fry == 1 / (fry / frx) )
        assert( 1 / frx / fry == (frx * fry).inverse() )

    assert( frac(.599).decimal(2) == '0.60' )
    assert( frac(1, 3).decimal(2) == '0.33' )
    assert( frac(a**2, b**2).sqrt() == abs(frac(a, b)) )
    assert( fra % 13 == (a * 10) % 13 )
    assert( frb % 13 == (b * 8) % 13 )

    assert( repeating_dec_to_rational(5, 142857) == frac(36, 7) )

@given(
    st.integers(),
    st.integers(),
    st.integers().filter(lambda x: x != 0)
    )
def test_quadratic(a, b, c):
    assume( a != 0 or b != 0 )
    assume( c < 0 or not is_square(c) )
    alpha = Quadratic(a, b, c)
    assert( alpha * alpha.conjugate() == alpha.norm() )
    assert( alpha.norm() * alpha.inverse() == alpha.conjugate() )
    assert( alpha * alpha.inverse() == 1 )
    assert( alpha - alpha == 0 )
    assert( alpha + alpha + alpha == 3 * alpha )
    assert( alpha * alpha * alpha == alpha**3 )
    assert( alpha / alpha == 1 )

@given(
    st.integers(),
    st.integers(),
    st.integers(),
    st.integers()
    )
def test_gcd(a, b, c, d):
    assume( a != 0 or b != 0 )
    assume( c != 0 or d != 0 )
    alpha = Quadratic(a, b, -1)
    beta = Quadratic(c, d, -1)
    delta = alpha.gcd(beta)
    assert( alpha % delta == beta % delta == 0 )
    assert( (alpha // delta).gcd(beta // delta) == 1 )

