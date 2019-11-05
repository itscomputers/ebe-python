#   tests/types_quadratic_test.py
#===========================================================
import math
import pytest
from hypothesis import assume, given, strategies as st

import env
from lib.basic import gcd, is_square
from lib.types.rational import Rational
from lib.types.quadratic import *
#===========================================================

def root_filter(x):
    return x < 0 or not is_square(x)

@st.composite
def rational(draw, nonzero=False):
    numer = draw(st.integers())
    denom = draw(st.integers(min_value=1))
    if nonzero:
        assume( numer != 0 )
    return Rational(numer, denom)

@st.composite
def quadratic(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    root = draw(st.integers().filter(root_filter))
    if nonzero:
        assume( (real, imag) != (0, 0) )
    return Quadratic(real, imag, root)

@st.composite
def quadratic_rational(draw, nonzero=False):
    r_n = draw(st.integers())
    r_d = draw(st.integers(min_value=1))
    i_n = draw(st.integers())
    i_d = draw(st.integers(min_value=1))
    root = draw(st.integers().filter(root_filter))
    if nonzero:
        assume( (r_n, i_n) != (0, 0) )
    return Quadratic(Rational(r_n, r_d), Rational(i_n, i_d), root)

@st.composite
def quadratic_pair(draw, nonzero=False):
    r1 = draw(st.integers())
    i1 = draw(st.integers())
    r2 = draw(st.integers())
    i2 = draw(st.integers())
    root = draw(st.integers().filter(root_filter))
    if nonzero:
        assume( (r1, i1) != (0, 0) )
        assume( (r2, i2) != (0, 0) )
    return (Quadratic(r1, i1, root), Quadratic(r2, i2, root))

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

@given(quadratic_pair(), quadratic())
def test_eq(pair, other):
    a, b = pair
    assert a == a
    if a.components == b.components:
        assert a == b
    else:
        assert a != b
    if a.signature == other.signature:
        assert a == other
    else:
        assert a != other

@given(quadratic(), st.integers())
def test_eq_int(a, i):
    if a.imag == 0 and a.real == i:
        assert a == i
    else:
        assert a != i

@given(quadratic(), rational())
def test_eq_rational(a, r):
    if a.imag == 0 and a.real == r:
        assert a == r
    else:
        assert a != r

#=============================

@given(quadratic())
def test_neg(a):
    assert type(-a) is Quadratic
    assert -a == Quadratic(-a.real, -a.imag, a.root)
    assert a + -a == -a + a == 0
    assert -a == -1 * a

@given(quadratic())
def test_norm_conjugate(a):
    conj = a.conjugate
    norm = a.norm
    assert type(conj) is Quadratic
    assert type(norm) is Rational
    assert conj == Quadratic(a.real, -a.imag, a.root)
    assert norm == a.real**2 - a.root * a.imag**2
    assert a * conj == norm
    assert a + conj == 2 * a.real
    assert a - conj == Quadratic(0, 2 * a.imag, a.root)

@given(quadratic_rational(nonzero=True))
def test_inverse(a):
    inv = a.inverse
    assert type(inv) is Quadratic
    assert a * inv == 1
    assert inv.inverse == a

@given(quadratic_rational())
def test_round(a):
    r = a.round
    assert type(r) is Quadratic
    assert set(map(lambda x: x.denom, r.components)) == set([1])

    for (ac, rc, dc) in zip(a.components, r.components, (a - r).components):
        if 2 * abs(dc) == 1:
            assert abs(rc) < abs(ac)
        else:
            assert 2 * abs(dc) < 1

#=============================

@given(quadratic_pair())
def test_add(pair):
    a, b = pair
    result = a + b
    reverse = b + a
    assert type(result) is Quadratic
    assert result == reverse
    assert result == Quadratic(a.real + b.real, a.imag + b.imag, a.root)

@given(quadratic(), st.integers())
def test_add_int(a, b):
    result = a + b
    reverse = b + a
    assert type(a + b) is Quadratic
    assert type(reverse) is Quadratic
    assert result == reverse
    assert result == Quadratic(a.real + b, a.imag, a.root)

@given(quadratic(), rational())
def test_add_Rational(a, b):
    result = a + b
    reverse = b + a
    assert type(result) is Quadratic
    assert result == reverse
    assert result == Quadratic(a.real + b, a.imag, a.root)

#=============================

@given(quadratic_pair())
def test_sub(pair):
    a, b = pair
    result = a - b
    reverse = b - a
    assert type(result) is Quadratic
    assert result + b == a
    assert result == -reverse == -b + a
    assert result == Quadratic(a.real - b.real, a.imag - b.imag, a.root)

@given(quadratic(), st.integers())
def test_sub_int(a, b):
    result = a - b
    reverse = b - a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert result + b == a
    assert result == -reverse == -b + a
    assert result == Quadratic(a.real - b, a.imag, a.root)

@given(quadratic(), rational())
def test_sub_Rational(a, b):
    result = a - b
    reverse = b - a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert result + b == a
    assert result == -reverse == -b + a
    assert result == Quadratic(a.real - b, a.imag, a.root)

#=============================

@given(quadratic_pair())
def test_mul(pair):
    a, b = pair
    result = a * b
    reverse = b * a
    real = a.real * b.real + a.imag * b.imag * a.root
    imag = a.real * b.imag + a.imag * b.real
    assert type(result) is Quadratic
    assert result == reverse
    assert result == Quadratic(real, imag, a.root)

@given(quadratic(), st.integers())
def test_mul_int(a, b):
    result = a * b
    reverse = b * a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert result == reverse
    assert result == Quadratic(a.real * b, a.imag * b, a.root)

@given(quadratic(), rational())
def test_mul_Rational(a, b):
    result = a * b
    reverse = b * a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert result == reverse
    assert result == Quadratic(a.real * b, a.imag * b, a.root)

#=============================

@given(quadratic_pair(nonzero=True))
def test_truediv(pair):
    a, b = pair
    result = a / b
    reverse = b / a
    b_norm = b.norm
    real = (a.real * b.real - a.imag * b.imag * a.root) / b_norm
    imag = (-a.real * b.imag + a.imag * b.real) / b_norm
    assert type(result) is Quadratic
    assert result * b == a
    assert result == reverse.inverse
    assert result == Quadratic(real, imag, a.root)

@given(quadratic(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_truediv_int(a, b):
    result = a / b
    reverse = b / a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert result * b == a
    assert result == reverse.inverse
    assert result == Quadratic(a.real / b, a.imag / b, a.root)

@given(quadratic(nonzero=True), rational(nonzero=True))
def test_truediv_Rational(a, b):
    result = a / b
    reverse = b / a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert result * b == a
    assert result == reverse.inverse
    assert result == Quadratic(a.real / b, a.imag / b, a.root)

#=============================

@given(quadratic_pair(nonzero=True))
def test_floordiv(pair):
    a, b = pair
    result = a // b
    b_norm = b.norm
    real = ((a.real * b.real - a.imag * b.imag * a.root) / b_norm).round_prefer_toward_zero
    imag = ((-a.real * b.imag + a.imag * b.real) / b_norm).round_prefer_toward_zero
    assert type(result) is Quadratic
    assert set(map(lambda x: x.denom, (result).components)) == set([1])
    assert result == Quadratic(real, imag, a.root)

@given(quadratic(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_floordiv_int(a, b):
    result = a // b
    reverse = b // a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert result == Quadratic(a.real // b, a.imag // b, a.root)
    assert reverse == Quadratic(b, 0, a.root) // a

@given(quadratic(nonzero=True), rational(nonzero=True))
def test_floordiv_Rational(a, b):
    result = a // b
    reverse = b // a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert result == Quadratic(a.real // b, a.imag // b, a.root)
    assert reverse == Quadratic(b, 0, a.root) // a

#=============================

@given(quadratic_pair(nonzero=True))
def test_mod(pair):
    a, b = pair
    result = a % b
    assert type(result) is Quadratic
    assert a == (a // b) * b + (result)
    if a.is_complex:
        assert abs(result) < abs(b)

@given(quadratic(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_mod_int(a, b):
    result = a % b
    reverse = b % a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert a == (a // b) * b + result
    assert b == (b // a) * a + reverse
    assert result == Quadratic(a.real % b, a.imag % b, a.root)
    assert reverse == Quadratic(b, 0, a.root) % a

@given(quadratic(nonzero=True), rational(nonzero=True))
def test_mod_Rational(a, b):
    result = a % b
    reverse = b % a
    assert type(result) is Quadratic
    assert type(reverse) is Quadratic
    assert a == (a // b) * b + result
    assert b == (b // a) * a + reverse
    assert result == Quadratic(a.real % b, a.imag % b, a.root)
    assert reverse == Quadratic(b, 0, a.root) % a

#=============================

@given(
    quadratic(nonzero=True),
    st.integers(min_value=-20, max_value=20),
    st.integers(min_value=-10, max_value=10)
)
def test_pow(a, m, n):
    mth_power = a**m
    nth_power = a**n
    sum_power = a**(m + n)
    assert type(a**0) is Quadratic
    assert type(a**1) is Quadratic
    assert type(a**-1) is Quadratic
    assert type(mth_power) is Quadratic
    assert a**0 == 1
    assert a**1 == a
    assert a**-1 == a.inverse
    assert a**2 == a * a
    assert a**(-2) == (a * a).inverse
    assert mth_power * nth_power == sum_power
    assert sum_power / mth_power == nth_power
    assert a**-m == mth_power.inverse

@given(
    quadratic(nonzero=True),
    st.integers(min_value=2, max_value=20),
    st.integers(min_value=2)
)
def test_pow_mod(a, exp, mod):
    power = a**exp
    mod_power = pow(a, exp, mod)
    assert type(power) is Quadratic
    assert type(mod_power) is Quadratic
    with pytest.raises(TypeError):
        pow(a, -exp, mod)

#=============================

@given(quadratic_rational())
def test_rational_approx(a):
    if a.imag == 0:
        assert a.rational_approx(25) == a.real
    elif a.root >= 0:
        r = a.rational_approx(25)
        assert (((r - a.real) / a.imag)**2).approx_equal(a.root, 12)
    else:
        with pytest.raises(ValueError):
            a.rational_approx(25)

@given(quadratic_rational())
def test_float(a):
    if abs(a.real) < 10**10 and abs(a.imag) < 10**5 and 2 <= a.root < 10**10:
        r = a.rational_approx(20)
        f = float(a.real) + float(a.imag) * math.sqrt(a.root)
        assert abs(float(r) - f) < 1 / 10**5

#=============================

def test_compatibility():
    a = Quadratic(1, 2, 3)
    b = Quadratic(1, 2, -1)
    fl = 0.5
    cx = complex(1, 2)

    for (x, y) in [(a, b), (a, fl), (a, cx), (b, cx)]:
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

    with pytest.raises(TypeError):
        5 ** a
    with pytest.raises(TypeError):
        frac(3, 2) ** a
    with pytest.raises(TypeError):
        a ** frac(3, 2)

