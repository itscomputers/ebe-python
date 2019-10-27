#   tests/types_quadratic_test.py
#===========================================================
import pytest
from hypothesis import assume, given, strategies as st

import env
from numth.basic import gcd, is_square
from numth.types import Rational, Quadratic
from numth.types.quadratic_integer import *
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
def quadratic_integer(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    root = draw(st.integers().filter(root_filter))
    if nonzero:
        assume( (real, imag) != (0, 0) )
    return QuadraticInteger(real, imag, root)

@st.composite
def quadratic_integer_pair(draw, nonzero=False):
    r1 = draw(st.integers())
    i1 = draw(st.integers())
    r2 = draw(st.integers())
    i2 = draw(st.integers())
    root = draw(st.integers().filter(root_filter))
    if nonzero:
        assume( (r1, i1) != (0, 0) )
        assume( (r2, i2) != (0, 0) )
    return (QuadraticInteger(r1, i1, root), QuadraticInteger(r2, i2, root))

@st.composite
def quadratic_integer_and_quadratic(draw, nonzero=False):
    r1 = draw(st.integers())
    i1 = draw(st.integers())
    r2 = draw(st.integers())
    i2 = draw(st.integers())
    root = draw(st.integers().filter(root_filter))
    if nonzero:
        assume( (r1, i1) != (0, 0) )
        assume( (r2, i2) != (0, 0) )
    return (QuadraticInteger(r1, i1, root), Quadratic(r2, i2, root))

#=============================

@given(quadratic_integer(), st.integers(), st.integers())
def test_from_components(a, real, imag):
    new = a.from_components(real, imag)
    assert type(new) is QuadraticInteger
    assert new.real == real
    assert new.imag == imag
    assert new.root == a.root

@given(quadratic_integer())
def test_to_quadratic(a):
    assert type(a.to_quadratic) is Quadratic
    assert a.to_quadratic == Quadratic(a.real, a.imag, a.root)
    assert a.to_quadratic == a

#=============================

@given(quadratic_integer_pair(), quadratic_integer())
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

@given(quadratic_integer_and_quadratic())
def test_eq_Quadratic(pair):
    a, b = pair
    if a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(quadratic_integer(), st.integers())
def test_eq_int(a, i):
    if a.imag == 0 and a.real == i:
        assert a == i
    else:
        assert a != i

@given(quadratic_integer(), rational())
def test_eq_Rational(a, r):
    if a.imag == 0 and a.real == r:
        assert a == r
    else:
        assert a != r

#=============================

@given(quadratic_integer())
def test_neg(a):
    assert type(-a) is QuadraticInteger
    assert -a == -(a.to_quadratic)

@given(quadratic_integer())
def test_norm_conjugateu(a):
    assert type(a.conjugate) is QuadraticInteger
    assert type(a.norm) is int
    assert a.conjugate == a.to_quadratic.conjugate
    assert a.norm == a.to_quadratic.norm

@given(quadratic_integer(nonzero=True))
def test_inverse(a):
    assert type(a.inverse) is Quadratic
    assert a.inverse == a.to_quadratic.inverse

@given(quadratic_integer())
def test_round(a):
    assert type(a.round) is QuadraticInteger
    assert a.round == a.to_quadratic.round

@given(quadratic_integer(nonzero=True), st.integers(min_value=2))
def test_mod_inverse(a, m):
    if gcd(a.norm, m) > 1:
        with pytest.raises(ValueError):
            a.mod_inverse(m)
    else:
        assert type(a.mod_inverse(m)) is QuadraticInteger
        assert (a * a.mod_inverse(m)) % m == 1

#=============================

@given(quadratic_integer_pair())
def test_add(pair):
    a, b = pair
    assert type(a + b) is QuadraticInteger
    assert a + b == a.to_quadratic + b.to_quadratic

@given(quadratic_integer_and_quadratic())
def test_add_Quadratic(pair):
    a, b = pair
    assert type(a + b) is Quadratic
    assert type(b + a) is Quadratic
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic

@given(quadratic_integer(), st.integers())
def test_add_int(a, b):
    assert type(a + b) is QuadraticInteger
    assert type(b + a) is QuadraticInteger
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic

@given(quadratic_integer(), rational())
def test_add_Rational(a, b):
    assert type(a + b) is Quadratic
    assert type(b + a) is Quadratic
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic

#=============================

@given(quadratic_integer_pair())
def test_sub(pair):
    a, b = pair
    assert type(a - b) is QuadraticInteger
    assert a - b == a.to_quadratic - b.to_quadratic

@given(quadratic_integer_and_quadratic())
def test_sub_Quadratic(pair):
    a, b = pair
    assert type(a - b) is Quadratic
    assert type(b - a) is Quadratic
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic

@given(quadratic_integer(), st.integers())
def test_sub_int(a, b):
    assert type(a - b) is QuadraticInteger
    assert type(b - a) is QuadraticInteger
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic

@given(quadratic_integer(), rational())
def test_sub_Rational(a, b):
    assert type(a - b) is Quadratic
    assert type(b - a) is Quadratic
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic

#=============================

@given(quadratic_integer_pair())
def test_mul(pair):
    a, b = pair
    assert type(a * b) is QuadraticInteger
    assert a * b == a.to_quadratic * b.to_quadratic

@given(quadratic_integer_and_quadratic())
def test_mul_Quadratic(pair):
    a, b = pair
    assert type(a * b) is Quadratic
    assert type(a * b) is Quadratic
    assert a * b == a.to_quadratic * b
    assert a * b == b * a.to_quadratic

@given(quadratic_integer(), st.integers())
def test_mul_int(a, b):
    assert type(a * b) is QuadraticInteger
    assert type(a * b) is QuadraticInteger
    assert a * b == a.to_quadratic * b
    assert a * b == b * a.to_quadratic

@given(quadratic_integer(), rational())
def test_mul_Rational(a, b):
    assert type(a * b) is Quadratic
    assert type(a * b) is Quadratic
    assert a * b == a.to_quadratic * b
    assert a * b == b * a.to_quadratic

#=============================

@given(quadratic_integer_pair(nonzero=True))
def test_truediv(pair):
    a, b = pair
    assert type(a / b) is Quadratic
    assert a / b == a.to_quadratic / b.to_quadratic

@given(quadratic_integer_and_quadratic(nonzero=True))
def test_truediv_Quadratic(pair):
    a, b = pair
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic

@given(quadratic_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_truediv_int(a, b):
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic

@given(quadratic_integer(nonzero=True), rational(nonzero=True))
def test_truediv_Rational(a, b):
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic

#=============================

@given(quadratic_integer_pair(nonzero=True))
def test_floordiv(pair):
    a, b = pair
    assert type(a // b) is QuadraticInteger
    assert a // b == a.to_quadratic // b.to_quadratic

@given(quadratic_integer_and_quadratic(nonzero=True))
def test_floordiv_Quadratic(pair):
    a, b = pair
    assert type(a // b) is QuadraticInteger
    assert type(b // a) is QuadraticInteger
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic

@given(quadratic_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_floordiv_int(a, b):
    assert type(a // b) is QuadraticInteger
    assert type(b // a) is QuadraticInteger
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic

@given(quadratic_integer(nonzero=True), rational(nonzero=True))
def test_floordiv_Rational(a, b):
    assert type(a // b) is QuadraticInteger
    assert type(b // a) is QuadraticInteger
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic

#=============================

@given(quadratic_integer_pair(nonzero=True))
def test_mod(pair):
    a, b = pair
    assert type(a % b) is QuadraticInteger
    assert a % b == a.to_quadratic % b.to_quadratic

@given(quadratic_integer_and_quadratic(nonzero=True))
def test_mod_Quadratic(pair):
    a, b = pair
    assert type(a % b) is Quadratic
    assert type(b % a) is Quadratic
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic

@given(quadratic_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_mod_int(a, b):
    assert type(a % b) is QuadraticInteger
    assert type(b % a) is QuadraticInteger
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic

@given(quadratic_integer(nonzero=True), rational(nonzero=True))
def test_mod_Rational(a, b):
    assert type(a % b) is Quadratic
    assert type(b % a) is Quadratic
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic

#=============================

@given(
    quadratic_integer(nonzero=True),
    st.integers(min_value=2, max_value=20)
)
def test_pow(a, m):
    mth_power = a**m
    mth_inverse = a**-m
    assert type(a**0) is QuadraticInteger
    assert type(a**1) is QuadraticInteger
    assert type(a**-1) is Quadratic
    assert type(mth_power) is QuadraticInteger
    assert type(mth_inverse) is Quadratic
    assert a**0 == 1
    assert a**1 == a
    assert a**-1 == a.inverse
    assert mth_power == a.to_quadratic**m
    assert mth_inverse == mth_power.inverse

@given(
    quadratic_integer(nonzero=True),
    st.integers(min_value=2, max_value=20),
    st.integers(min_value=2)
)
def test_pow_mod(a, exp, mod):
    power = a**exp
    mod_power = pow(a, exp, mod)
    assert type(power) is QuadraticInteger
    assert type(mod_power) is QuadraticInteger
    if gcd(a.norm, mod) > 1:
        with pytest.raises(ValueError):
            pow(a, -exp, mod)
    else:
        mod_power_inv = pow(a, -exp, mod)
        assert type(mod_power_inv) is QuadraticInteger
        assert (mod_power * mod_power_inv) % mod == 1

#=============================

@given(quadratic_integer())
def test_rational_approx(a):
    if a.imag == 0:
        assert a.rational_approx(25) == a.real
    elif a.root >= 0:
        assert a.rational_approx(25) == a.to_quadratic.rational_approx(25)
    else:
        with pytest.raises(ValueError):
            a.rational_approx(25)

