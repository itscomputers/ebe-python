#   tests/types_quaternion_integer_test.py
#===========================================================
import pytest
from hypothesis import assume, given, strategies as st

import env
from numth.basic import gcd
from numth.types import Rational
from numth.types.quaternion import Quaternion
from numth.types.quaternion_integer import *
#===========================================================

@st.composite
def rational(draw, nonzero=False):
    numer = draw(st.integers())
    denom = draw(st.integers(min_value=1))
    if nonzero:
        assume( numer != 0 )
    return Rational(numer, denom)

@st.composite
def quaternion_integer(draw, nonzero=False):
    r = draw(st.integers())
    i = draw(st.integers())
    j = draw(st.integers())
    k = draw(st.integers())
    if nonzero:
        assume( (r, i, j, k) != (0, 0, 0, 0) )
    return QuaternionInteger(r, i, j, k)

@st.composite
def quaternion(draw, nonzero=False):
    r = draw(st.integers())
    i = draw(st.integers())
    j = draw(st.integers())
    k = draw(st.integers())
    if nonzero:
        assume( (r, i, j, k) != (0, 0, 0, 0) )
    return Quaternion(r, i, j, k)

@st.composite
def gaussian_rational(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume( (real, imag) != (0, 0) )
    return GaussianRational(real, imag)

@st.composite
def gaussian_integer(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume( (real, imag) != (0, 0) )
    return GaussianInteger(real, imag)

#=============================

@given(quaternion_integer())
def test_to_quaternion(a):
    result = a.to_quaternion
    assert type(result) is Quaternion
    assert result.components == a.components
    assert result == a

@given(gaussian_rational())
def test_from_gaussian_rational(a):
    result = QuaternionInteger.from_gaussian_rational(a)
    assert type(result) is Quaternion
    assert result.r == a.real
    assert result.i == a.imag
    assert result.j == result.k == 0

@given(gaussian_integer())
def test_from_gaussian_integer(a):
    result = QuaternionInteger.from_gaussian_integer(a)
    assert type(result) is QuaternionInteger
    assert result.r == a.real
    assert result.i == a.imag
    assert result.j == result.k == 0

#=============================

@given(quaternion_integer(), quaternion_integer())
def test_eq(a, b):
    assert a == a
    if a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(quaternion_integer(), quaternion())
def test_eq_Quaternion(a, b):
    assert a == a
    if a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(quaternion_integer(), st.integers())
def test_eq_int(a, i):
    if a.is_real and a.r == i:
        assert a == i
    else:
        assert a != i

@given(quaternion_integer(), rational())
def test_eq_Rational(a, r):
    if a.is_real and a.r == r:
        assert a == r
    else:
        assert a != r

#=============================

@given(quaternion_integer())
def test_neg(a):
    assert type(-a) is QuaternionInteger
    assert -a == -(a.to_quaternion)

@given(quaternion_integer())
def test_norm_conjugate(a):
    assert type(a.conjugate) is QuaternionInteger
    assert type(a.norm) is int
    assert a.conjugate == a.to_quaternion.conjugate
    assert a.norm == a.to_quaternion.norm

@given(quaternion_integer(nonzero=True))
def test_inverse(a):
    assert type(a.inverse) is Quaternion
    assert a.inverse == a.to_quaternion.inverse

@given(quaternion_integer())
def test_round(a):
    assert type(a.round) is QuaternionInteger
    assert a.round == a.to_quaternion.round

@given(quaternion_integer(), st.integers(min_value=2))
def test_mod_inverse(a, m):
    if gcd(a.norm, m) > 1:
        with pytest.raises(ValueError):
            a.mod_inverse(m)
    else:
        assert type(a.mod_inverse(m)) is QuaternionInteger
        assert (a * a.mod_inverse(m)) % m == 1

#=============================

@given(quaternion_integer(), quaternion_integer())
def test_add(a, b):
    assert type(a + b) is QuaternionInteger
    assert a + b == a.to_quaternion + b.to_quaternion

@given(quaternion_integer(), quaternion())
def test_add_quaternion(a, b):
    assert type(a + b) is Quaternion
    assert type(b + a) is Quaternion
    assert a + b == a.to_quaternion + b
    assert b + a == b + a.to_quaternion

@given(quaternion_integer(), st.integers())
def test_add_int(a, b):
    assert type(a + b) is QuaternionInteger
    assert type(b + a) is QuaternionInteger
    assert a + b == a.to_quaternion + b
    assert b + a == b + a.to_quaternion


@given(quaternion_integer(), rational())
def test_add_Rational(a, b):
    assert type(a + b) is Quaternion
    assert type(b + a) is Quaternion
    assert a + b == a.to_quaternion + b
    assert b + a == b + a.to_quaternion

#=============================

@given(quaternion_integer(), quaternion_integer())
def test_sub(a, b):
    assert type(a - b) is QuaternionInteger
    assert a - b == a.to_quaternion - b.to_quaternion

@given(quaternion_integer(), quaternion())
def test_sub_quaternion(a, b):
    assert type(a - b) is Quaternion
    assert type(b - a) is Quaternion
    assert a - b == a.to_quaternion - b
    assert b - a == b - a.to_quaternion

@given(quaternion_integer(), st.integers())
def test_sub_int(a, b):
    assert type(a - b) is QuaternionInteger
    assert type(b - a) is QuaternionInteger
    assert a - b == a.to_quaternion - b
    assert b - a == b - a.to_quaternion

@given(quaternion_integer(), rational())
def test_sub_Rational(a, b):
    assert type(a - b) is Quaternion
    assert type(b - a) is Quaternion
    assert a - b == a.to_quaternion - b
    assert b - a == b - a.to_quaternion

#=============================

@given(quaternion_integer(), quaternion_integer())
def test_mul(a, b):
    assert type(a * b) is QuaternionInteger
    assert a * b == a.to_quaternion * b.to_quaternion

@given(quaternion_integer(), quaternion())
def test_mul_quaternion(a, b):
    assert type(a * b) is Quaternion
    assert type(b * a) is Quaternion
    assert a * b == a.to_quaternion * b
    assert b * a == b * a.to_quaternion

@given(quaternion_integer(), st.integers())
def test_mul_int(a, b):
    assert type(a * b) is QuaternionInteger
    assert type(b * a) is QuaternionInteger
    assert a * b == a.to_quaternion * b
    assert b * a == b * a.to_quaternion

@given(quaternion_integer(), rational())
def test_mul_Rational(a, b):
    assert type(a * b) is Quaternion
    assert type(b * a) is Quaternion
    assert a * b == a.to_quaternion * b
    assert b * a == b * a.to_quaternion

#=============================

@given(quaternion_integer(), quaternion_integer(nonzero=True))
def test_truediv(a, b):
    assert type(a / b) is Quaternion
    assert a / b == a.to_quaternion / b.to_quaternion

@given(quaternion_integer(nonzero=True), quaternion(nonzero=True))
def test_truediv_quaternion(a, b):
    assert type(a / b) is Quaternion
    assert type(b / a) is Quaternion
    assert a / b == a.to_quaternion / b
    assert b / a == b / a.to_quaternion

@given(quaternion_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_truediv_int(a, b):
    assert type(a / b) is Quaternion
    assert type(b / a) is Quaternion
    assert a / b == a.to_quaternion / b
    assert b / a == b / a.to_quaternion

@given(quaternion_integer(nonzero=True), rational(nonzero=True))
def test_truediv_Rational(a, b):
    assert type(a / b) is Quaternion
    assert type(b / a) is Quaternion
    assert a / b == a.to_quaternion / b
    assert b / a == b / a.to_quaternion

#=============================

@given(quaternion_integer(), quaternion_integer(nonzero=True))
def test_floordiv(a, b):
    assert type(a // b) is QuaternionInteger
    assert a // b == a.to_quaternion // b.to_quaternion

@given(quaternion_integer(nonzero=True), quaternion(nonzero=True))
def test_floordiv_quaternion(a, b):
    assert type(a // b) is QuaternionInteger
    assert type(b // a) is Quaternion
    assert a // b == a.to_quaternion // b
    assert b // a == b // a.to_quaternion

@given(quaternion_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_floordiv_int(a, b):
    assert type(a // b) is QuaternionInteger
    assert type(b // a) is QuaternionInteger
    assert a // b == a.to_quaternion // b
    assert b // a == b // a.to_quaternion

@given(quaternion_integer(nonzero=True), rational(nonzero=True))
def test_floordiv_Rational(a, b):
    assert type(a // b) is QuaternionInteger
    assert type(b // a) is Quaternion
    assert a // b == a.to_quaternion // b
    assert b // a == b // a.to_quaternion

#=============================

@given(quaternion_integer(), quaternion_integer(nonzero=True))
def test_mod(a, b):
    assert type(a % b) is QuaternionInteger
    assert a % b == a.to_quaternion % b.to_quaternion

@given(quaternion_integer(nonzero=True), quaternion(nonzero=True))
def test_mod_quaternion(a, b):
    assert type(a % b) is Quaternion
    assert type(b % a) is Quaternion
    assert a % b == a.to_quaternion % b
    assert b % a == b % a.to_quaternion

@given(quaternion_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_mod_int(a, b):
    assert type(a % b) is QuaternionInteger
    assert type(b % a) is QuaternionInteger
    assert a % b == a.to_quaternion % b
    assert b % a == b % a.to_quaternion

@given(quaternion_integer(nonzero=True), rational(nonzero=True))
def test_mod_Rational(a, b):
    assert type(a % b) is Quaternion
    assert type(b % a) is Quaternion
    assert a % b == a.to_quaternion % b
    assert b % a == b % a.to_quaternion

#=============================

@given(
    quaternion_integer(nonzero=True),
    st.integers(min_value=2, max_value=20)
)
def test_pow(a, m):
    mth_power = a**m
    mth_inverse = a**-m
    assert type(a**0) is QuaternionInteger
    assert type(a**1) is QuaternionInteger
    assert type(a**-1) is Quaternion
    assert type(mth_power) is QuaternionInteger
    assert type(mth_inverse) is Quaternion
    assert a**0 == 1
    assert a**1 == a
    assert a**-1 == a.inverse
    assert mth_power == a.to_quaternion**m
    assert mth_inverse == mth_power.inverse

@given(
    quaternion_integer(nonzero=True),
    st.integers(min_value=0, max_value=20),
    st.integers(min_value=2)
)
def test_pow_mod(a, exp, mod):
    power = a**exp
    mod_power = pow(a, exp, mod)
    assert type(power) is QuaternionInteger
    assert type(mod_power) is QuaternionInteger
    assert power % mod == mod_power
    if exp > 0 and gcd(a.norm, mod) > 1:
        with pytest.raises(ValueError):
            pow(a, -exp, mod)
    else:
        mod_power_inv = pow(a, -exp, mod)
        assert type(mod_power_inv) is QuaternionInteger
        assert (mod_power * mod_power_inv) % mod == 1

