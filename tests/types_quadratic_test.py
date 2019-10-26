#   tests/types_quadratic_test.py
#===========================================================
import math
import pytest
from hypothesis import assume, given, strategies as st

import env
from numth.basic import is_square
from numth.types.rational import Rational
from numth.types.quadratic import *
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

@given(quadratic(), st.integers(), st.integers())
def test_from_components(a, real, imag):
    new = a.from_components(real, imag)
    assert type(new) is Quadratic
    assert new.real == real
    assert new.imag == imag
    assert new.root == a.root

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
    assert type(a.conjugate) is Quadratic
    assert type(a.norm) is Rational
    assert a.conjugate == Quadratic(a.real, -a.imag, a.root)
    assert a.norm == a.real**2 - a.root * a.imag**2
    assert a * a.conjugate == a.norm
    assert a + a.conjugate == 2 * a.real
    assert a - a.conjugate == Quadratic(0, 2 * a.imag, a.root)

@given(quadratic_rational(nonzero=True))
def test_inverse(a):
    assert type(a.inverse) is Quadratic
    assert a * a.inverse == 1
    assert a.inverse.inverse == a

@given(quadratic_rational())
def test_round(a):
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

@given(quadratic_pair())
def test_add(pair):
    a, b = pair
    assert type(a + b) is Quadratic
    assert a + b == b + a
    assert a + b == Quadratic(a.real + b.real, a.imag + b.imag, a.root)

@given(quadratic(), st.integers())
def test_add_int(a, i):
    assert type(a + i) is Quadratic
    assert type(i + a) is Quadratic
    assert a + i == i + a
    assert a + i == Quadratic(a.real + i, a.imag, a.root)

@given(quadratic(), rational())
def test_add_Rational(a, r):
    assert type(a + r) is Quadratic
    assert a + r == r + a
    assert a + r == Quadratic(a.real + r, a.imag, a.root)

#=============================

@given(quadratic_pair())
def test_sub(pair):
    a, b = pair
    assert type(a - b) is Quadratic
    assert a - b == -(b - a) == -b + a
    assert a - b == Quadratic(a.real - b.real, a.imag - b.imag, a.root)

@given(quadratic(), st.integers())
def test_sub_int(a, i):
    assert type(a - i) is Quadratic
    assert type(i - a) is Quadratic
    assert a - i == -(i - a) == -i + a
    assert a - i == Quadratic(a.real - i, a.imag, a.root)

@given(quadratic(), rational())
def test_sub_Rational(a, r):
    assert type(a - r) is Quadratic
    assert type(r - a) is Quadratic
    assert a - r == -(r - a) == -r + a
    assert a - r == Quadratic(a.real - r, a.imag, a.root)

#=============================

@given(quadratic_pair())
def test_mul(pair):
    a, b = pair
    real = a.real * b.real + a.imag * b.imag * a.root
    imag = a.real * b.imag + a.imag * b.real
    assert type(a * b) is Quadratic
    assert a * b == b * a
    assert a * b == Quadratic(real, imag, a.root)

@given(quadratic(), st.integers())
def test_mul_int(a, i):
    assert type(a * i) is Quadratic
    assert type(i * a) is Quadratic
    assert a * i == i * a
    assert a * i == Quadratic(a.real * i, a.imag * i, a.root)

@given(quadratic(), rational())
def test_mul_Rational(a, r):
    assert type(a * r) is Quadratic
    assert type(r * a) is Quadratic
    assert a * r == r * a
    assert a * r == Quadratic(a.real * r, a.imag * r, a.root)

#=============================

@given(quadratic_pair(nonzero=True))
def test_truediv(pair):
    a, b = pair
    b_norm = b.norm
    real = (a.real * b.real - a.imag * b.imag * a.root) / b_norm
    imag = (-a.real * b.imag + a.imag * b.real) / b_norm
    assert type(a / b) is Quadratic
    assert a / b == (b / a).inverse
    assert a / b == Quadratic(real, imag, a.root)

@given(quadratic(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_truediv_int(a, i):
    assert type(a / i) is Quadratic
    assert type(i / a) is Quadratic
    assert a / i == (i / a).inverse
    assert a / i == Quadratic(a.real / i, a.imag / i, a.root)

@given(quadratic(nonzero=True), rational(nonzero=True))
def test_truediv_Rational(a, r):
    assert type(a / r) is Quadratic
    assert type(r / a) is Quadratic
    assert a / r == (r / a).inverse
    assert a / r == Quadratic(a.real / r, a.imag / r, a.root)

#=============================

@given(quadratic_pair(nonzero=True))
def test_floordiv(pair):
    a, b = pair
    b_norm = b.norm
    real = ((a.real * b.real - a.imag * b.imag * a.root) / b_norm).round_prefer_toward_zero
    imag = ((-a.real * b.imag + a.imag * b.real) / b_norm).round_prefer_toward_zero
    assert type(a // b) is Quadratic
    assert set(map(lambda x: x.denom, (a // b).components)) == set([1])
    assert a // b == Quadratic(real, imag, a.root)

@given(quadratic(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_floordiv_int(a, i):
    assert type(a // i) is Quadratic
    assert type(i // a) is Quadratic
    assert a // i == Quadratic(a.real // i, a.imag // i, a.root)
    assert i // a == Quadratic(i, 0, a.root) // a

@given(quadratic(nonzero=True), rational(nonzero=True))
def test_floordiv_Rational(a, r):
    assert type(a // r) is Quadratic
    assert type(r // a) is Quadratic
    assert a // r == Quadratic(a.real // r, a.imag // r, a.root)
    assert r // a == Quadratic(r, 0, a.root) // a

#=============================

@given(quadratic_pair(nonzero=True))
def test_mod(pair):
    a, b = pair
    assert type(a % b) is Quadratic
    assert a == (a // b) * b + (a % b)
    if a.is_complex:
        assert abs(a % b) < abs(b)

@given(quadratic(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_mod_int(a, i):
    assert type(a % i) is Quadratic
    assert type(i % a) is Quadratic
    assert a % i == Quadratic(a.real % i, a.imag % i, a.root)
    assert a == (a // i) * i + (a % i)
    assert i % a == Quadratic(i, 0, a.root) % a

@given(quadratic(nonzero=True), rational(nonzero=True))
def test_mod_Rational(a, r):
    assert type(a % r) is Quadratic
    assert type(r % a) is Quadratic
    assert a % r == Quadratic(a.real % r, a.imag % r, a.root)
    assert a == (a // r) * r + (a % r)
    assert r % a == Quadratic(r, 0, a.root) % a

#=============================

@given(
    quadratic(nonzero=True),
    st.integers(min_value=-20, max_value=20),
    st.integers(min_value=-10, max_value=10)
)
def test_pow(a, m, n):
    assert type(a**0) is Quadratic
    assert type(a**1) is Quadratic
    assert type(a**-1) is Quadratic
    assert type(a**m) is Quadratic
    assert a**0 == 1
    assert a**1 == a
    assert a**-1 == a.inverse
    assert a**2 == a * a
    assert a**(-2) == (a * a).inverse
    mth_power = a**m
    nth_power = a**n
    sum_power = a**(m + n)
    assert mth_power * nth_power == sum_power
    assert sum_power / mth_power == nth_power
    assert a**-m == mth_power.inverse

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

