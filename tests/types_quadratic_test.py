#   tests/types_quadratic_test.py
#===========================================================
import env
import itertools
import math
import pytest
from hypothesis import given, assume, strategies as st

from numth.basic import gcd, is_square
from numth.types import Rational
from numth.types.quadratic import *
from numth.types.quadratic import _round_prefer_down
#===========================================================

def root_filter(x):
    return x < 0 or not is_square(x)

#-----------------------------

def pair():
    return 2 * [st.integers()]

def coords(rmin=None, rmax=None):
    if rmin is not None and rmax is not None:
        rval = st.integers(min_value=rmin, max_value=rmax)
    elif rmin is not None:
        rval = st.integers(min_value=rmin)
    elif rmax is not None:
        rval = st.integers(max_value=rmax)
    else:
        rval = st.integers()
    return [*pair(), rval.filter(root_filter)]

def rational():
    return [st.integers(), st.integers(min_value=1)]

def rational_coords():
    return [*rational(), *rational(), st.integers().filter(root_filter)]

def double_coords():
    return [*pair(), *pair(), st.integers().filter(root_filter)]

#=============================

@given(
    st.integers(min_value=2),
    st.integers(min_value=2)
)
def test_display(a, b):
    roots = {
            -1: '\u2139',
            5: '{}{}'.format('\u221a', 5),
            frac(1, 2): '{}({})'.format('\u221a', frac(1, 2))
    }

    for d in roots.keys():
        assert repr(Quadratic(0, 0, d)) == '0'
        assert repr(Quadratic(0, 1, d)) == roots[d]
        assert repr(Quadratic(0, -1, d)) == '-{}'.format(roots[d])

        assert repr(Quadratic(a, 0, d)) == '{}'.format(a)
        assert repr(Quadratic(a, 1, d)) == '{} + {}'.format(a, roots[d])
        assert repr(Quadratic(a, -1, d)) == '{} - {}'.format(a, roots[d])
        assert repr(Quadratic(-a, 0, d)) == '-{}'.format(a)
        assert repr(Quadratic(-a, 1, d)) == '-{} + {}'.format(a, roots[d])
        assert repr(Quadratic(-a, -1, d)) == '-{} - {}'.format(a, roots[d])

        assert repr(Quadratic(0, b, d)) == '{} {}'.format(b, roots[d])
        assert repr(Quadratic(0, -b, d)) == '-{} {}'.format(b, roots[d])

        assert repr(Quadratic(a, b, d)) == '{} + {} {}'.format(a, b, roots[d])
        assert repr(Quadratic(-a, b, d)) == '-{} + {} {}'.format(a, b, roots[d])
        assert repr(Quadratic(a, -b, d)) == '{} - {} {}'.format(a, b, roots[d])
        assert repr(Quadratic(-a, -b, d)) == '-{} - {} {}'.format(a, b, roots[d])

#=============================

@given(*pair())
def test_from_complex(real, imag):
    if abs(real) < 2**53 and abs(imag) < 2**53:
        assert Quadratic(real, imag, -1) == Quadratic.from_complex(complex(real, imag))

#-----------------------------

@given(*coords())
def test_from_components(real, imag, root):
    a = Quadratic(real, imag, root)
    assert a.from_components(real, imag) == a
    assert a.from_components(real, -imag) == a.conjugate
    assert a.from_components(-real, -imag) == -a

#=============================

@given(*coords())
def test_neg(real, imag, root):
    a = Quadratic(real, imag, root)
    assert -a == Quadratic(-real, -imag, root)
    assert a + -a == -a + a == Quadratic(0, 0, root)
    assert -a == -1 * a

#-----------------------------

@given(*coords())
def test_norm_conjugate(real, imag, root):
    a = Quadratic(real, imag, root)
    assert a.conjugate == Quadratic(real, -imag, root)
    assert a.norm == a.real**2 - a.root * a.imag**2
    assert a * a.conjugate == Quadratic(a.norm, 0, a.root)
    assert a + a.conjugate == Quadratic(2*a.real, 0, a.root)
    assert a - a.conjugate == Quadratic(0, 2*a.imag, a.root)

#-----------------------------

@given(*rational_coords())
def test_inverse(real_n, real_d, imag_n, imag_d, root):
    real = frac(real_n, real_d)
    imag = frac(imag_n, imag_d)
    assume( real != 0 and imag != 0 )
    a = Quadratic(real, imag, root)
    assert a * a.inverse == Quadratic(1, 0, root)
    assert a.inverse.inverse == a

#-----------------------------

@given(*rational_coords())
def test_round(real_n, real_d, imag_n, imag_d, root):
    real = frac(real_n, real_d)
    imag = frac(imag_n, imag_d)
    a = Quadratic(real, imag, root)
    r = a.round
    diff = a - r

    if 2 * abs(diff.real) == 1:
        assert abs(r.real) < abs(a.real)
    else:
        assert 2 * abs(diff.real) < 1

    if 2 * abs(diff.imag) == 1:
        assert abs(r.imag) < abs(a.imag)
    else:
        assert 2 * abs(diff.imag) < 1

#=============================

@given(*double_coords())
def test_add(real1, imag1, real2, imag2, root):
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    s = Quadratic(real1 + real2, imag1 + imag2, root)
    assert q1 + q2 == s
    assert q2 + q1 == s

#-----------------------------

@given(*coords(), *rational())
def test_add_quadratic_and_number(real, imag, root, numer, denom):
    q = Quadratic(real, imag, root)
    r = Quadratic(real + numer, imag, root)
    s = Quadratic(real + frac(numer, denom), imag, root)
    assert q + numer == r
    assert numer + q == r
    assert q + frac(numer, denom) == s
    assert frac(numer, denom) + q == s

#=============================

@given(*double_coords())
def test_sub(real1, imag1, real2, imag2, root):
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    s = Quadratic(real1 - real2, imag1 - imag2, root)
    assert q1 - q2 == s
    assert q2 - q1 == -s
    assert q1 - q2 == -q2 + q1
    assert q2 - q1 == -q1 + q2

#-----------------------------

@given(*coords(), *rational())
def test_sub_quadratic_and_number(real, imag, root, numer, denom):
    q = Quadratic(real, imag, root)
    r = Quadratic(real - numer, imag, root)
    s = Quadratic(real - frac(numer, denom), imag, root)
    assert q - numer == r
    assert numer - q == -r
    assert q - frac(numer, denom) == s
    assert frac(numer, denom) - q == -s

#=============================

@given(*double_coords())
def test_mul(real1, imag1, real2, imag2, root):
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    real = real1 * real2 + imag1 * imag2 * root
    imag = real1 * imag2 + imag1 * real2
    s = Quadratic(real, imag, root)
    assert q1 * q2 == s
    assert q2 * q1 == s

#-----------------------------

@given(*coords(), *rational())
def test_mul_quadratic_and_number(real, imag, root, numer, denom):
    q = Quadratic(real, imag, root)
    r = Quadratic(real * numer, imag * numer, root)
    s = Quadratic(
        real * frac(numer, denom),
        imag * frac(numer, denom),
        root
    )
    assert q * numer == r
    assert numer * q == r
    assert q * frac(numer, denom) == s
    assert frac(numer, denom) * q == s

#=============================

@given(*double_coords())
def test_div(real1, imag1, real2, imag2, root):
    assume( real1 != 0 or imag1 != 0 )
    assume( real2 != 0 or imag2 != 0 )
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    q2_norm = q2.norm
    real = (real1 * real2 - imag1 * imag2 * root) / q2_norm
    imag = (-real1 * imag2 + imag1 * real2) / q2_norm
    s = Quadratic(real, imag, root)
    assert q1 / q2 == s
    assert q2 / q1 == s.inverse

#-----------------------------

@given(*coords(), *rational())
def test_div_quadratic_and_number(real, imag, root, numer, denom):
    assume( (real != 0 or imag != 0) and numer != 0 )
    q = Quadratic(real, imag, root)
    r = Quadratic(frac(real, numer), frac(imag, numer), root)
    s = Quadratic(
        real / frac(numer, denom),
        imag / frac(numer, denom),
        root
    )
    assert q / numer == r
    assert numer / q == r.inverse
    assert q / frac(numer, denom) == s
    assert frac(numer, denom) / q == s.inverse

#=============================

@given(*double_coords())
def test_floordiv(real1, imag1, real2, imag2, root):
    assume( real2 != 0 or imag2 != 0 )
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    q2_norm = q2.norm
    real = _round_prefer_down((real1 * real2 - imag1 * imag2 * root) / q2_norm)
    imag = _round_prefer_down((-real1 * imag2 + imag1 * real2) / q2_norm)
    s = Quadratic(real, imag, root)
    assert q1 // q2 == s

#-----------------------------

@given(*coords(), st.integers().filter(lambda x: x != 0))
def test_floordiv_quadratic_and_integer(real, imag, root, integer):
    assume( real != 0 or imag != 0 )
    q = Quadratic(real, imag, root)
    r = Quadratic(real // integer, imag // integer, root)
    assert q // integer == r
    assert integer // q == Quadratic(integer, 0, root) // q

#-----------------------------

@given(*double_coords())
def test_mod(real1, imag1, real2, imag2, root):
    assume( real2 != 0 or imag2 != 0 )
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    assert q1 == (q1 // q2) * q2 + (q1 % q2)
    if root == -1:
        assert q1 % q2 <= q2

#-----------------------------

@given(*coords(), st.integers(min_value=1))
def test_mod_quadratic_and_integer(real, imag, root, integer):
    assume( real != 0 or imag != 0 )
    q = Quadratic(real, imag, root)
    r = Quadratic(real % integer, imag % integer, root)
    assert q % integer == r
    assert integer % q == Quadratic(integer, 0, root) % q
    assert q == (q // integer) * integer + (q % integer)

#-----------------------------

@given(
    *coords(),
    st.integers(min_value=-20, max_value=20),
    st.integers(min_value=-10, max_value=10)
)
def test_pow(real, imag, root, m, n):
    assume( real != 0 or imag != 0 )
    q = Quadratic(real, imag, root)
    assert q**2 == q * q
    assert q**(-2) == (q * q).inverse
    mth_power = q**m
    nth_power = q**n
    sum_power = q**(m + n)
    assert mth_power * nth_power == sum_power
    assert sum_power / mth_power == nth_power

#=============================

@given(*rational_coords())
def test_rational_approx(real_n, real_d, imag_n, imag_d, root):
    real = frac(real_n, real_d)
    imag = frac(imag_n, imag_d)
    a = Quadratic(real, imag, root)
    if imag == 0:
        assert a.rational_approx(25) == real
    elif root >= 0:
        r = a.rational_approx(25)
        assert (((r - real) / imag)**2).approx_equal(root, 12)
    else:
        with pytest.raises(ValueError):
            a.rational_approx(25)

#-----------------------------

@given(
    st.integers(min_value=-10**53, max_value=10**53),
    st.integers(min_value=-10**26, max_value=10**26),
    st.integers(min_value=2, max_value=10**53)
)
def text_float(real, imag, root):
    a = Quadratic(real, imag, root)
    r = a.rational_approx(20)
    f = real_n + imag * math.sqrt(root)
    assert abs(float(r) - f) < 1 / 10**10

#=============================

def test_compatibility():
    a = Quadratic(1, 2, 3)
    b = Quadratic(4, 5, -6)
    c = Quadratic(7, 8, -1)
    
    incompatible_pairs = [
        (a, b),
        (a, c),
        (b, c),
        (c, .5),
        (c, complex(9, 10))
    ]
    for (x, y) in incompatible_pairs:
        with pytest.raises(TypeError):
            x + y
        with pytest.raises(TypeError):
            y + x
        with pytest.raises(TypeError):
            x - y
        with pytest.raises(TypeError):
            y - x
        with pytest.raises(TypeError):
            x * y
        with pytest.raises(TypeError):
            y * x
        with pytest.raises(TypeError):
            x / y
        with pytest.raises(TypeError):
            y / x
        with pytest.raises(TypeError):
            x // y
        with pytest.raises(TypeError):
            y // x
        with pytest.raises(TypeError):
            x % y
        with pytest.raises(TypeError):
            y % x
        with pytest.raises(TypeError):
            x ** y
        with pytest.raises(TypeError):
            y ** x
    
    for y in [a, 4, frac(4, 5)]:
        assert isinstance(a + y, Quadratic)
        assert isinstance(y + a, Quadratic)
        assert isinstance(a - y, Quadratic) 
        assert isinstance(y - a, Quadratic) 
        assert isinstance(a * y, Quadratic)
        assert isinstance(y * a, Quadratic)
        assert isinstance(a / y, Quadratic)
        assert isinstance(y / a, Quadratic)
        assert isinstance(a // y, Quadratic)
        assert isinstance(y // a, Quadratic)
        assert isinstance(a % y, Quadratic)
        assert isinstance(y % a, Quadratic)

    assert isinstance(a ** 4, Quadratic)
    assert isinstance(a ** -4, Quadratic)

    with pytest.raises(TypeError):
        4 ** a 
    with pytest.raises(TypeError):
        a ** frac(4, 5)
    with pytest.raises(TypeError):
        frac(4, 5) ** a

#=============================

@given(st.floats(min_value=0))
def test_round_prefer_down(number):
    assume( str(number) not in ['-inf', 'inf', 'nan'] )
    if number <= int(number) + .5:
        assert _round_prefer_down(number) == int(number)
    else:
        assert _round_prefer_down(number) == int(number) + 1
    assert _round_prefer_down(-number) == - _round_prefer_down(number)

