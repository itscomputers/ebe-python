#   tests/types_gaussian_integer_test.py
# ===========================================================
import pytest
from hypothesis import assume, given, strategies as st

import env
from lib.basic import gcd
from lib.types import frac, Rational, GaussianRational, Quadratic, QuadraticInteger
from lib.types.gaussian_integer import *

# ===========================================================


@st.composite
def rational(draw, nonzero=False):
    numer = draw(st.integers())
    denom = draw(st.integers(min_value=1))
    if nonzero:
        assume(numer != 0)
    return Rational(numer, denom)


@st.composite
def gaussian_integer(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume((real, imag) != (0, 0))
    return GaussianInteger(real, imag)


@st.composite
def gaussian_rational(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume((real, imag) != (0, 0))
    return GaussianRational(real, imag)


@st.composite
def quadratic(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume((real, imag) != (0, 0))
    return Quadratic(real, imag, -1)


@st.composite
def quadratic_integer(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume((real, imag) != (0, 0))
    return QuadraticInteger(real, imag, -1)


# =============================


@given(gaussian_integer())
def test_to_gaussian_rational(a):
    assert type(a.to_gaussian_rational) is GaussianRational
    assert a.to_gaussian_rational == GaussianRational(a.real, a.imag)
    assert a.to_gaussian_rational == a


# =============================


@given(gaussian_integer(), gaussian_integer())
def test_eq(a, b):
    assert a == a
    if a.components == b.components:
        assert a == b
    else:
        assert a != b


@given(gaussian_integer(), gaussian_rational())
def test_gaussian_rational(a, b):
    if a.components == b.components:
        assert a == b
    else:
        assert a != b


@given(gaussian_integer(), quadratic_integer())
def test_eq_quadratic_integer(a, b):
    if b.is_complex and a.components == b.components:
        assert a == b
    else:
        assert a != b


@given(gaussian_integer(), quadratic())
def test_eq_quadratic(a, b):
    if b.is_complex and a.components == b.components:
        assert a == b
    else:
        assert a != b


@given(gaussian_integer(), st.integers())
def test_eq_int(a, i):
    if a.imag == 0 and a.real == i:
        assert a == i
    else:
        assert a != i


@given(gaussian_integer(), rational())
def test_eq_Rational(a, r):
    if a.imag == 0 and a.real == r:
        assert a == r
    else:
        assert a != r


# =============================


@given(gaussian_integer())
def test_neg(a):
    assert type(-a) is GaussianInteger
    assert -a == -(a.to_gaussian_rational)


@given(gaussian_integer())
def test_norm_conjugate(a):
    assert type(a.conjugate) is GaussianInteger
    assert type(a.norm) is int
    assert a.conjugate == a.to_gaussian_rational.conjugate
    assert a.norm == a.to_gaussian_rational.norm


@given(gaussian_integer(nonzero=True))
def test_inverse(a):
    assert type(a.inverse) is GaussianRational
    assert a.inverse == a.to_gaussian_rational.inverse


@given(gaussian_integer())
def test_round(a):
    assert type(a.round) is GaussianInteger
    assert a.round == a.to_gaussian_rational.round


@given(gaussian_integer(), st.integers(min_value=2))
def test_mod_inverse(a, m):
    if gcd(a.norm, m) > 1:
        with pytest.raises(ValueError):
            a.mod_inverse(m)
    else:
        assert type(a.mod_inverse(m)) is GaussianInteger
        assert (a * a.mod_inverse(m)) % m == 1


# =============================


@given(gaussian_integer())
def test_canonical(a):
    z = a.canonical
    assert z.real >= abs(z.imag)


@given(gaussian_integer(), gaussian_integer(nonzero=True))
def test_gcd(a, b):
    z = a.gcd(b)
    assert a % z == b % z == 0
    assert (a // z).gcd(b // z) == 1


# =============================


@given(gaussian_integer(), gaussian_integer())
def test_add(a, b):
    assert type(a + b) is GaussianInteger
    assert a + b == a.to_gaussian_rational + b.to_gaussian_rational


@given(gaussian_integer(), quadratic_integer())
def test_add_QuadraticInteger(a, b):
    assert type(a + b) is GaussianInteger
    assert type(b + a) is GaussianInteger
    assert a + b == a.to_gaussian_rational + b
    assert b + a == b + a.to_gaussian_rational


@given(gaussian_integer(), quadratic())
def test_add_Quadratic(a, b):
    assert type(a + b) is GaussianRational
    assert type(b + a) is GaussianRational
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic


@given(gaussian_integer(), st.integers())
def test_add_int(a, b):
    assert type(a + b) is GaussianInteger
    assert type(b + a) is GaussianInteger
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic


@given(gaussian_integer(), rational())
def test_add_Rational(a, b):
    assert type(a + b) is GaussianRational
    assert type(b + a) is GaussianRational
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic


# =============================


@given(gaussian_integer(), gaussian_integer())
def test_sub(a, b):
    assert type(a - b) is GaussianInteger
    assert a - b == a.to_gaussian_rational - b.to_gaussian_rational


@given(gaussian_integer(), quadratic_integer())
def test_sub_QuadraticInteger(a, b):
    assert type(a - b) is GaussianInteger
    assert type(b - a) is GaussianInteger
    assert a - b == a.to_gaussian_rational - b
    assert b - a == b - a.to_gaussian_rational


@given(gaussian_integer(), quadratic())
def test_sub_Quadratic(a, b):
    assert type(a - b) is GaussianRational
    assert type(b - a) is GaussianRational
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic


@given(gaussian_integer(), st.integers())
def test_sub_int(a, b):
    assert type(a - b) is GaussianInteger
    assert type(b - a) is GaussianInteger
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic


@given(gaussian_integer(), rational())
def test_sub_Rational(a, b):
    assert type(a - b) is GaussianRational
    assert type(b - a) is GaussianRational
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic


# =============================


@given(gaussian_integer(), gaussian_integer())
def test_mul(a, b):
    assert type(a * b) is GaussianInteger
    assert a * b == a.to_gaussian_rational * b.to_gaussian_rational


@given(gaussian_integer(), quadratic_integer())
def test_mul_QuadraticInteger(a, b):
    assert type(a * b) is GaussianInteger
    assert type(b * a) is GaussianInteger
    assert a * b == a.to_gaussian_rational * b
    assert b * a == b * a.to_gaussian_rational


@given(gaussian_integer(), quadratic())
def test_mul_Quadratic(a, b):
    assert type(a * b) is GaussianRational
    assert type(b * a) is GaussianRational
    assert a * b == a.to_quadratic * b
    assert b * a == b * a.to_quadratic


@given(gaussian_integer(), st.integers())
def test_mul_int(a, b):
    assert type(a * b) is GaussianInteger
    assert type(b * a) is GaussianInteger
    assert a * b == a.to_quadratic * b
    assert b * a == b * a.to_quadratic


@given(gaussian_integer(), rational())
def test_mul_Rational(a, b):
    assert type(a * b) is GaussianRational
    assert type(b * a) is GaussianRational
    assert a * b == a.to_quadratic * b
    assert b * a == b * a.to_quadratic


# =============================


@given(gaussian_integer(), gaussian_integer(nonzero=True))
def test_truediv(a, b):
    assert type(a / b) is GaussianRational
    assert a / b == a.to_gaussian_rational / b.to_gaussian_rational


@given(gaussian_integer(nonzero=True), quadratic_integer(nonzero=True))
def test_truediv_QuadraticInteger(a, b):
    assert type(a / b) is GaussianRational
    assert type(b / a) is GaussianRational
    assert a / b == a.to_gaussian_rational / b
    assert b / a == b / a.to_gaussian_rational


@given(gaussian_integer(nonzero=True), quadratic(nonzero=True))
def test_truediv_Quadratic(a, b):
    assert type(a / b) is GaussianRational
    assert type(b / a) is GaussianRational
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic


@given(gaussian_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_truediv_int(a, b):
    assert type(a / b) is GaussianRational
    assert type(b / a) is GaussianRational
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic


@given(gaussian_integer(nonzero=True), rational(nonzero=True))
def test_truediv_Rational(a, b):
    assert type(a / b) is GaussianRational
    assert type(b / a) is GaussianRational
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic


# =============================


@given(gaussian_integer(), gaussian_integer(nonzero=True))
def test_floordiv(a, b):
    assert type(a // b) is GaussianInteger
    assert a // b == a.to_gaussian_rational // b.to_gaussian_rational


@given(gaussian_integer(nonzero=True), quadratic_integer(nonzero=True))
def test_floordiv_QuadraticInteger(a, b):
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == a.to_gaussian_rational // b
    assert b // a == b // a.to_gaussian_rational


@given(gaussian_integer(nonzero=True), quadratic(nonzero=True))
def test_floordiv_Quadratic(a, b):
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic


@given(gaussian_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_floordiv_int(a, b):
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic


@given(gaussian_integer(nonzero=True), rational(nonzero=True))
def test_floordiv_Rational(a, b):
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic


# =============================


@given(gaussian_integer(), gaussian_integer(nonzero=True))
def test_mod(a, b):
    assert type(a % b) is GaussianInteger
    assert a % b == a.to_gaussian_rational % b.to_gaussian_rational


@given(gaussian_integer(nonzero=True), quadratic_integer(nonzero=True))
def test_mod_QuadraticInteger(a, b):
    assert type(a % b) is GaussianInteger
    assert type(b % a) is GaussianInteger
    assert a % b == a.to_gaussian_rational % b
    assert b % a == b % a.to_gaussian_rational


@given(gaussian_integer(nonzero=True), quadratic(nonzero=True))
def test_mod_Quadratic(a, b):
    assert type(a % b) is GaussianRational
    assert type(b % a) is GaussianRational
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic


@given(gaussian_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_mod_int(a, b):
    assert type(a % b) is GaussianInteger
    assert type(b % a) is GaussianInteger
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic


@given(gaussian_integer(nonzero=True), rational(nonzero=True))
def test_mod_Rational(a, b):
    assert type(a % b) is GaussianRational
    assert type(b % a) is GaussianRational
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic


# =============================


@given(gaussian_integer(nonzero=True), st.integers(min_value=2, max_value=20))
def test_pow(a, m):
    mth_power = a ** m
    mth_inverse = a ** -m
    assert type(a ** 0) is GaussianInteger
    assert type(a ** 1) is GaussianInteger
    assert type(a ** -1) is GaussianRational
    assert type(mth_power) is GaussianInteger
    assert type(mth_inverse) is GaussianRational
    assert a ** 0 == 1
    assert a ** 1 == a
    assert a ** -1 == a.inverse
    assert mth_power == a.to_gaussian_rational ** m
    assert mth_inverse == mth_power.inverse


@given(
    gaussian_integer(nonzero=True),
    st.integers(min_value=2, max_value=20),
    st.integers(min_value=2),
)
def test_pow_mod(a, exp, mod):
    power = a ** exp
    mod_power = pow(a, exp, mod)
    assert type(power) is GaussianInteger
    assert type(mod_power) is GaussianInteger
    if gcd(a.norm, mod) > 1:
        with pytest.raises(ValueError):
            pow(a, -exp, mod)
    else:
        mod_power_inv = pow(a, -exp, mod)
        assert type(mod_power_inv) is GaussianInteger
        assert (mod_power * mod_power_inv) % mod == 1


# =============================


@given(gaussian_integer())
def test_rational_approx(a):
    if a.imag == 0:
        assert a.rational_approx(25) == a.real
    else:
        with pytest.raises(ValueError):
            a.rational_approx(25)
